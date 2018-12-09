# -*- coding: utf-8 -*-
"""
Module gérant le modèle linéaire
"""

from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import linear_model
import matplotlib.pyplot as plt

def predireRidge(datas,n):
    """Prépare les données et lance une prédiction via un modèle linéaire Ridge de la semaine n
    
    Arguments :
        datas : données à traiter (DataFrame)
        n: numéro de semaine à prédire (à partir du début du fichier) (int)
    """
    histo=list(datas['Historique'].values[:n-1])
    livpass=list(datas['Livraisons réelles'].values[:n-1])
    apredire=list(datas['Historique'].values[n])
    r=ridgePredict(histo,livpass,apredire)
    return r

def ridgePredict(histo, livpass, apredire):
    """Prédit via Ridge
    
    Arguments :
        histo : historique des prévisions passées (list)
        livpass : livraisons réelles passées (list)
        apredire : historique des prévisions de la semaine à prédire (list)
    """
    regr=linear_model.Ridge()
    regr.fit(histo, livpass)
    predicto=regr.predict([apredire])[0]
    return predicto

def fullsimul(datas,mini):
    """Lance une simulation avec un minimum de x semaines
    
    Arguments :
        datas : données à traiter (DataFrame)
        mini : nombre minimum de semaines d'historique à considérer (int, devrait être > 2)
    """
    lr=list(datas['Livraisons réelles'].values)[mini:]
    total=[]
    for i in range(mini,len(datas)):
        total.append(predireRidge(datas,i))
    ecartmoy=sqrt(mean_squared_error(total,lr))
    return ecartmoy

def plotError(datas):
    """Evalue l'erreur du modèle selon le nombre de semaines d'historique minimal à disposition
    
    Argument :
        datas : données à traiter (DataFrame)
    """
    em=[]
    for i in range(2,35):
        em.append(fullsimul(datas,i))
    plt.plot(em)
    plt.show()