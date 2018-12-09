# -*- coding: utf-8 -*-
"""
Test des différents modèles linéaires
Nécessite le datas de formatage.py
"""
from formatage import datas
from sklearn.metrics import mean_squared_error
from math import sqrt

tmp2=datas
## MODELE LINEAIRE 281
from sklearn import linear_model
regr=linear_model.LinearRegression()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE RIDGE ----> 146
from sklearn import linear_model
regr=linear_model.Ridge()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE LASSO ----> 146
from sklearn import linear_model
regr=linear_model.Lasso(max_iter = 1000000)
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE ELASTIC NET ----> 146
from sklearn import linear_model
regr=linear_model.ElasticNet(max_iter = 1000000)
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE LARS ----> 165
from sklearn import linear_model
regr=linear_model.Lars()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE ORTHOGONAL MATCHING PURSUIT ----> 238
from sklearn import linear_model
regr=linear_model.OrthogonalMatchingPursuit()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE BAYESIAN RIDGE ----> 261
from sklearn import linear_model
regr=linear_model.BayesianRidge()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE ARDREGRESSION ----> 226
from sklearn import linear_model
regr=linear_model.ARDRegression()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE LOGISTIC REGRESSION ----> 353
from sklearn import linear_model
regr=linear_model.LogisticRegression()
regr.fit(list(datas['Historique'][:15].values), list(datas['Livraisons réelles'][:15].values))
predicto=regr.predict(list(datas['Historique'][15:].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'][15:].values,predicto))

## MODELE LINEAIRE ARDRegression ----> 226
from sklearn import linear_model
regr=linear_model.ARDRegression()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE SGDClassifier ----> 302
from sklearn import linear_model
regr=linear_model.SGDClassifier()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE SGDRegressor ----> 10^5
from sklearn import linear_model
regr=linear_model.SGDRegressor()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE Perceptron ----> 307
from sklearn import linear_model
regr=linear_model.Perceptron()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

## MODELE LINEAIRE PassiveAggressiveClassifier ----> 260
from sklearn import linear_model
regr=linear_model.PassiveAggressiveClassifier()
regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
predicto=regr.predict(list(datas['Historique'].values))
ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)

### MODELE LINEAIRE RANSACRegressor ----> ?
#from sklearn import linear_model
#regr=linear_model.RANSACRegressor()
#regr.fit(list(datas['Historique'].values), list(datas['Livraisons réelles'].values))
#predicto=regr.predict(list(datas['Historique'].values))
#ecartmoy=sqrt(mean_squared_error(datas['Livraisons réelles'].values, predicto))#ecartmoy=sum(abs(list(datas['Livraisons réelles'].values)-predicto))/len(predicto)
