# -*- coding: utf-8 -*-
"""
Modèle linéaire, mais propre
"""

from formatage import wonderframe
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import linear_model
#from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

## FULL RIDGE, LES ENFANTS -- TEMPLATE
regr=linear_model.Ridge()
regr.fit(list(wonderframe['Historique'].values), list(wonderframe['Livraisons réelles'].values))
predicto=regr.predict(list(wonderframe['Historique'].values))
ecartmoy=sqrt(mean_squared_error(wonderframe['Livraisons réelles'].values, predicto))

## TEST DE L'INFLUENCE DES PARAMETRES
# ALPHA TESTING
alpha=[0.01,0.1,0.5,1,5,10,50,100]
X=list(wonderframe['Historique'].values)
Y=list(wonderframe['Livraisons réelles'].values)
ecarts=[]
#X=StandardScaler().fit_transform(X) -- LES RESULTATS NORMALISES SONT PIRES
for a in alpha:
    regr=linear_model.Ridge(alpha=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(wonderframe['Livraisons réelles'].values, predicto)))
ecarts # VAGUEMENT MIEUX
ecarts=[]
tolist = [0.00001,0.0001,0.001,0.01,0.1,1,10]
for a in tolist:
    regr=linear_model.Ridge(tol=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(wonderframe['Livraisons réelles'].values, predicto)))
ecarts # INUTILE
solist=['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
ecarts=[]
for a in solist:
    regr=linear_model.Ridge(solver=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(wonderframe['Livraisons réelles'].values, predicto)))
ecarts # SVD/CHOLESKY

def preproc(wonderframe,n):
    histo=list(wonderframe['Historique'].values[:n-1])
    livpass=list(wonderframe['Livraisons réelles'].values[:n-1])
    apredire=list(wonderframe['Historique'].values[n])
    r=ridgePredict(histo,livpass,apredire)
    return r

def ridgePredict(histo, livpass, apredire):
    regr=linear_model.Ridge()
    regr.fit(histo, livpass)
    predicto=regr.predict([apredire])[0]
    return predicto

def fullsimul(wonderframe,mini):
    lr=list(wonderframe['Livraisons réelles'].values)[mini:]
    total=[]
    for i in range(mini,len(wonderframe)):
        total.append(preproc(wonderframe,i))
    ecartmoy=sqrt(mean_squared_error(total,lr))
    return ecartmoy

def plotError(wonderframe):
    em=[]
    for i in range(2,35):
        em.append(fullsimul(wonderframe,i))
    plt.plot(em)
    plt.show()