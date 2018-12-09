# -*- coding: utf-8 -*-
"""
Modèle linéaire - tests & templates (dev only)
"""

from formatage import datas
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import linear_model
#from sklearn.preprocessing import StandardScaler

## FULL RIDGE, LES ENFANTS -- TEMPLATE
regr=linear_model.Ridge()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))

## TEST DE L'INFLUENCE DES PARAMETRES
# ALPHA TESTING
alpha=[0.01,0.1,0.5,1,5,10,50,100]
X=list(datas['Historique'].values)
Y=list(datas['Livraisons réelles'].values)
ecarts=[]
#X=StandardScaler().fit_transform(X) -- LES RESULTATS NORMALISES SONT PIRES
for a in alpha:
    regr=linear_model.Ridge(alpha=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto)))
ecarts # VAGUEMENT MIEUX
ecarts=[]
tolist = [0.00001,0.0001,0.001,0.01,0.1,1,10]
for a in tolist:
    regr=linear_model.Ridge(tol=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto)))
ecarts # INUTILE
solist=['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
ecarts=[]
for a in solist:
    regr=linear_model.Ridge(solver=a)
    regr.fit(X, Y)
    predicto=regr.predict(X)
    ecarts.append(sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto)))
ecarts # SVD/CHOLESKY