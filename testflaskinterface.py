# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 12:04:04 2018

@author: Admin
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from math import sqrt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import statsmodels.api as sm

from flask import  Flask,render_template,request,redirect
from io import BytesIO
#from pandas.compat import StringIO
import base64
#import urllib
from urllib.parse import quote
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    df = pd.read_excel('2018-19ProjetJohnsonElectricArbitrageFeuilledecalcul.xlsx',sheet_name='pivot demande')
    #print(df)
    #print(df.iloc[3,1])
    df2=df.drop([0,1,2,4,(df.shape[0]-1)])
    df2=df2.iloc[:,:df2.shape[1]-1]
    df3=df2.reset_index(drop=True)
    df3['Unnamed: 1']=df3['Unnamed: 1'].astype(float)
    nbsemaines=df3.shape[1]-1
    semaines=df3.iloc[1].values[1:]
    livraisons=df3.iloc[0].values[1:]
    
    df4=df3.drop([0,1])
    caraibes=[]
    for i in range(nbsemaines): # colonnes
        martinique=[]
        for j in range(nbsemaines-2,-1,-1): # lignes # pour le bon nb de lignes, nbsemaines-1
            if not(np.isnan(df4.iloc[j,i+1])):
                martinique.append(df4.iloc[j,i+1])
        for j in range(len(martinique),nbsemaines):
            martinique.append(0)
        caraibes.append(martinique[::-1])
        
    wonderframe=pd.DataFrame()
    wonderframe['Semaines']=semaines
    wonderframe['Livraisons réelles']=livraisons
    wonderframe['Historique']=caraibes
    
    
    #predictnaiv=[]
    #for i in range(len(caraibes)):
    #    predictnaiv.append((caraibes[i][-1]))
    #errquadnaiv=sqrt(mean_squared_error(predictnaiv,livraisons)) 
    
    predict=[]
    for i in range(len(caraibes)):
        predict.append(np.mean(caraibes[i][-i-1:]))
    errquadmoy=round(sqrt(mean_squared_error(predict,livraisons)),2)
    
    regr=linear_model.Ridge()
    regr.fit(caraibes, livraisons)
    predictregr=regr.predict(caraibes)
    ecartmoyregr=round(sqrt(mean_squared_error(livraisons, predictregr)),2)    
    
    #Exponential Moving Average
    ema=[]
    for i in range(len(caraibes)):
        ema.append(pd.DataFrame(caraibes[i]).ewm(alpha=0.045,adjust=False).mean())
    predictewma=[]
    for i in range(len(caraibes)):
        predictewma.append(ema[i].iloc[35,0])
    errquadmewma=round(sqrt(mean_squared_error(predictewma,livraisons)),2)
    
    
    
    #Holter's Winter
    listlivraison=livraisons.tolist()
    
    #sm.tsa.seasonal_decompose(listlivraison,freq=5,model='additive').plot()
    resultat = sm.tsa.stattools.adfuller(wonderframe['Livraisons réelles'])
    #plt.show()
    modelholter = ExponentialSmoothing(listlivraison,seasonal_periods=35,trend='add',seasonal='add').fit()
    predictwinter = modelholter.forecast(len(listlivraison))

    img = BytesIO() 
    plt.figure()

    r= list(range(1,len(semaines)+1))
    rw= list(range(1,len(semaines)+2))
    for i in range(len(semaines)):
            for j in range(len(caraibes[i])):
                #Scaraibes.append(caraibes[i][j])
               plt.scatter(r[i],caraibes[i][j],s=2, c="green")          
    #plt.figure(figsize=(10,10))
    #plt.rcParams["figure.figsize"] = [16,9]       
    plt.plot(r,livraisons,label="Livraisons réelles")
    #plt.plot(rw,predictwinter,label="prédiction holtwinter")
    #plt.plot(r,predictnaiv,label="prédiction naive")
    plt.plot(r,predict,label="prédiction moyenne")
    plt.plot(r,predictewma,label="prédiction exp.moving.average")
    plt.plot(r,predictregr,label="prédiction rég. lin.")
    plt.ylabel("Historique des Prévisions")
    plt.xlabel('Semaines')
    plt.title("Première vue d'ensemble")
    plt.legend()

    
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data = quote(base64.b64encode(img.read()).decode())
    
#    img2 = BytesIO() 
    livraisons=np.insert(livraisons,35,livraisons[35])
    predictwinter=np.insert(predictwinter,0,predictwinter[0]) 
    errquadwinter=round(sqrt(mean_squared_error(predictwinter,livraisons)),2)   
#    plt.figure()
#    plt.plot(rw,livraisons,label="Livraisons réelles")
#    plt.plot(rw,predictwinter,label="prédiction holtwinter")
#    plt.legend()
#    plt.savefig(img2, format='png')
#    img2.seek(0) 
    
#    plot_data2 = quote(base64.b64encode(img2.read()).decode())

    return render_template("index.html",plot_url=plot_data,err1=errquadmoy,err2=ecartmoyregr,err3=errquadmewma,err4=errquadwinter)

@app.route('/telechargerlexcel', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['inputFile']
        f.save(secure_filename(f.filename))
    return redirect('/')
	
    
app.run(debug=True,port=8085)