# -*- coding: utf-8 -*-
"""
Interface web
"""
from formatage import formaterXLSX
from modele_lin import predireRidge, fullSimul

import matplotlib.pyplot as plt

from flask import  Flask,render_template,request,redirect
from io import BytesIO
import base64
from urllib.parse import quote
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/miniup', methods = ['GET', 'POST'])
def mu():
    if request.method == 'POST':
        m = int(request.form['mini'])
    return graphe(m)

@app.route('/graphe')
def graphe(mini=31):
    datas=formaterXLSX()
    
    
    img = BytesIO() 
    plt.figure()
    
    nbsemaines=len(datas)
    livraisons=datas['Livraisons réelles'].values
    
    r= list(range(1,nbsemaines+1))
    
    em=[]
    for i in range(2,35):
        em.append(fullSimul(datas,i))
    
    predR=[]
    for i in range(mini,nbsemaines):
        predR.append(predireRidge(datas,i))   
    plt.plot(r,livraisons,label="Livraisons réelles")
    plt.plot(r[mini:],predR,label='Modèle linéaire Ridge')
    plt.ylabel("Quantité")
    plt.xlabel('Semaines')
    plt.title("Prédictions du modèle contre livraisons réelles")
    plt.legend()

    
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data = quote(base64.b64encode(img.read()).decode())
    
    img = BytesIO() 
    plt.figure()
    plt.title("Erreur du modèle en fonction du nombre de semaines d'historique")
    plt.ylabel("Erreur moyenne")
    plt.xlabel("Nombre de semaines d'historique")
    plt.plot(em)
    plt.savefig(img, format='png')
    img.seek(0)
    
    plot_data2 = quote(base64.b64encode(img.read()).decode())
    return render_template("graphe.html",plot_url=plot_data,plot2_url=plot_data2,maxhist=nbsemaines-2,liv=list(livraisons),pred=list(predR))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/telechargerlexcel', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['inputFile']
        f.save(secure_filename(f.filename))
    return redirect('/graphe')

@app.route('/comparer')
def lancercmp():
    return render_template("index.html",bcmp='True')

app.run(debug=True,port=8085)