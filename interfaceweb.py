# -*- coding: utf-8 -*-
"""
Interface web
"""
from formatage import formaterXLSX
from modele_lin import predireRidge, fullSimul
from win32com.client import Dispatch
import os,os.path
import matplotlib.pyplot as plt

from flask import  Flask,render_template,request,redirect
from io import BytesIO
import base64
from urllib.parse import quote
from werkzeug import secure_filename
import pythoncom

app = Flask(__name__)

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from math import sqrt
from statsmodels.tsa.api import ExponentialSmoothing

nomfichierXLS = "" # Nom du fichier Excel coté serveur à traiter (global)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Page d'index
    """
    return render_template("index.html")

@app.route('/telechargerlexcel', methods = ['GET', 'POST'])
def upload_file():
    """
    Téléchargement des données pour traitement
    """
    if request.method == 'POST':
        # Enregistrement du fichier
        f = request.files['inputFile']
        f.save(secure_filename(f.filename))
        # Changement du produit
        prod = int(request.form['prod'])
        pythoncom.CoInitialize()
        xl = Dispatch("Excel.Application")
        xl.Workbooks.Open(os.getcwd()+'/'+f.filename)
        xl.ActiveWorkbook.Worksheets('pivot demande').Cells(4,2).Value=prod
        xl.ActiveWorkbook.Close(SaveChanges=1)
        # Enregistrement du nom de fichier
        global nomfichierXLS
        nomfichierXLS=f.filename
        return redirect('/comparaison')

@app.route('/comparaison')
def cmp():
    """
    Comparaison des performances 'absolues' des différents algorithmes
    """
    # Chargement des données
    global nomfichierXLS
    datas=formaterXLSX(nomfichierXLS)
    histo=list(datas['Historique'].values)
    livraisons=list(datas['Livraisons réelles'].values)
    semaines=list(datas['Semaines'].values)

    #Average
    predict=[]
    for i in range(len(histo)):
        predict.append(np.mean(histo[i][-i-1:]))
    errquadmoy=round(sqrt(mean_squared_error(predict,livraisons)))
    
    #Regression linéaire de Ridge
    regr=linear_model.Ridge()
    regr.fit(histo, livraisons)
    predictregr=regr.predict(histo)
    ecartmoyregr=round(sqrt(mean_squared_error(livraisons, predictregr)))    
    
    #Exponential Moving Average
    ema=[]
    for i in range(len(histo)):
        ema.append(pd.DataFrame(histo[i]).ewm(alpha=0.045,adjust=False).mean())
    predictewma=[]
    for i in range(len(histo)):
        predictewma.append(ema[i].iloc[35,0])
    errquadmewma=round(sqrt(mean_squared_error(predictewma,livraisons)),2)
    
    #Holter's Winter
    modelholter = ExponentialSmoothing(livraisons,seasonal_periods=35,seasonal='add').fit()
    predictwinter = modelholter.forecast(len(livraisons))
    predictwinter2 = predictwinter[:35]
    livraisons2=livraisons[1:]
    errquadwinter=round(sqrt(mean_squared_error(predictwinter2,livraisons2))) 
    
    # Graphique
    plt.figure()
    
    r= list(range(1,len(semaines)+1))
    for i in range(len(semaines)):
            for j in range(len(histo[i])):
               plt.scatter(r[i],histo[i][j],s=2, c="green")           
    plt.plot(r,livraisons,label="Livraisons réelles")
    plt.plot(r,predict,label="Moyenne")
    plt.plot(r,predictewma,label="Exponential moving average")
    plt.plot(r,predictregr,label="Régression linéaire Ridge")
    plt.plot(list(range(2,len(semaines)+1)),predictwinter2, label="Time Series Holt-Winter")
    plt.ylabel("Quantités")
    plt.xlabel('Semaines')
    plt.title("Comparaison des algorithmes")
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data = quote(base64.b64encode(img.read()).decode())
    
    return render_template("comparaison.html",plot_url=plot_data,err1=errquadmoy,err2=ecartmoyregr,err3=errquadmewma,err4=errquadwinter,prevholt=round(predictwinter2[34]))

@app.route('/miniup', methods = ['GET', 'POST'])
def mu():
    """
    Recalcul avec un nombre de semaines différent
    """
    if request.method == 'POST':
        m = int(request.form['mini'])
    return graphe(m)

@app.route('/graphe')
def graphe(mini=31):
    """
    Graphe des prévisions et tableau
    """
    # Données
    global nomfichierXLS
    datas=formaterXLSX(nomfichierXLS)
    livraisons=list(datas['Livraisons réelles'].values)
    
    mini=mini-1
    img = BytesIO() 
    plt.figure()
    
    nbsemaines=len(datas)
    livraisons=datas['Livraisons réelles'].values
    nomsem=list(datas['Semaines'].values)
    histo=list(datas['Historique'].values)
    demandes=[]
    for k in range(len(histo)):
        demandes.append(histo[k])
        
    r= list(range(1,nbsemaines+1))
    # Ecarts moyens ridge/nb d'historique
    em=[]
    for i in range(2,len(histo)-1):
        em.append(fullSimul(datas,i))
    
    # Arbitrage Série Temporelle
    for i in range(3,len(histo)):
        #Holter's Winter
        modelholter = ExponentialSmoothing(livraisons[:i],seasonal_periods=i-1,seasonal='add').fit()
        predictwinter = list(modelholter.forecast(len(livraisons[:i])))
    predictwinter.insert(0,0)
    
    # Arbitrage Modèle Linéaire
    predR=[]
    for i in range(mini,nbsemaines):
        predR.append(predireRidge(datas,i))   
    
    # Graphique d'arbitrage
    plt.plot(r,livraisons,label="Livraisons réelles")
    plt.plot(r[mini:],predR,label='Modèle linéaire Ridge')
    plt.plot(r,predictwinter,label='Modèle Holt-Winters')
    plt.ylabel("Quantité")
    plt.xlabel('Semaines')
    plt.title("Prédictions du modèle contre livraisons réelles")
    plt.legend()
    
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data = quote(base64.b64encode(img.read()).decode())
    
    # Graphique fiabilité modèle linéaire
    img = BytesIO() 
    plt.figure()
    plt.title("Erreur du modèle en fonction du nombre de semaines d'historique")
    plt.ylabel("Erreur moyenne")
    plt.xlabel("Nombre de semaines d'historique")
    plt.plot(em)
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data2 = quote(base64.b64encode(img.read()).decode())
    return render_template("graphe.html",plot_url=plot_data,plot2_url=plot_data2,maxhist=nbsemaines,liv=list(livraisons),pred=[int(i) for i in predR],sem=nomsem, dem=demandes, prevwinterr=predictwinter)

app.run(debug=True,port=8085)