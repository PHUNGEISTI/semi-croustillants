# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:22:59 2018

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

df = pd.read_excel('2018-19ProjetJohnsonElectricArbitrageFeuilledecalcul.xlsx',sheet_name='pivot demande')
print(df)
print(df.iloc[3,1])
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
errquadmoy=sqrt(mean_squared_error(predict,livraisons))

regr=linear_model.Ridge()
regr.fit(caraibes, livraisons)
predictregr=regr.predict(caraibes)
ecartmoyregr=sqrt(mean_squared_error(livraisons, predictregr))    

#Exponential Moving Average
ema=[]
for i in range(len(caraibes)):
    ema.append(pd.DataFrame(caraibes[i]).ewm(alpha=0.045,adjust=False).mean())
predictewma=[]
for i in range(len(caraibes)):
    predictewma.append(ema[i].iloc[35,0])
errquadmewma=sqrt(mean_squared_error(predictewma,livraisons))



#Holter's Winter
listlivraison=livraisons.tolist()

sm.tsa.seasonal_decompose(listlivraison,freq=5,model='additive').plot()
resultat = sm.tsa.stattools.adfuller(wonderframe['Livraisons réelles'])
plt.show()
modelholter = ExponentialSmoothing(listlivraison,seasonal_periods=35,trend='add',seasonal='add').fit()
predictwinter = modelholter.forecast(len(listlivraison))
errquadwinter=sqrt(mean_squared_error(predictwinter,livraisons))
#PLOTING
r= list(range(1,len(semaines)+1))
for i in range(len(semaines)):
        for j in range(len(caraibes[i])):
            #Scaraibes.append(caraibes[i][j])
           plt.scatter(r[i],caraibes[i][j],s=2, c="green")          
#plt.figure(figsize=(10,10))
#plt.rcParams["figure.figsize"] = [16,9]  
plt.figure()     
plt.plot(r,livraisons,label="Livraisons réelles")
plt.plot(r,predictwinter,label="prédiction holtwinter")
#plt.plot(r,predictnaiv,label="prédiction naive")
plt.plot(r,predict,label="prédiction moyenne")
plt.plot(r,predictewma,label="prédiction exp.moving.average")
plt.plot(r,predictregr,label="prédiction rég. lin.")
plt.ylabel("Historique des Prévisions")
plt.xlabel('Semaines')
plt.title("Première vue d'ensemble")
plt.legend()
plt.show()
    
  




