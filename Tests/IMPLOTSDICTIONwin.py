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

def getHistorique(datas,nbsemaines):
    """Get the historic datas

    Keyword arguments:
    datas -- Dataframe
    nbsemaines -- Number of weeks
    """
    
    historique=[]
    for i in range(nbsemaines): # colonnes
        hist_tmp=[]
        for j in range(nbsemaines-2,-1,-1): # lignes # pour le bon nb de lignes, nbsemaines-1
            if not(np.isnan(df4.iloc[j,i+1])):
                hist_tmp.append(df4.iloc[j,i+1])
        for j in range(len(hist_tmp),nbsemaines):
            hist_tmp.append(0)
        historique.append(hist_tmp[::-1])
    return historique



    
"""Build the dataframes"""
df = pd.read_excel('2018-19ProjetJohnsonElectricArbitrageFeuilledecalcul.xlsx',sheet_name='pivot demande')
"""Delete useless datas of the dataframe"""
df2=df.drop([0,1,2,4,(df.shape[0]-1)])
df2=df2.iloc[:,:df2.shape[1]-1]

"""Reset the index for the dataframe"""
df3=df2.reset_index(drop=True)
"""Convert datas type in float"""
df3['Unnamed: 1']=df3['Unnamed: 1'].astype(float)
"""Delete useless columns"""
df4=df3.drop([0,1])


"""Build the datas,lists for the number of weeks,dates of the weeks, number of deliveries"""
nbsemaines=df3.shape[1]-1
semaines=df3.iloc[1].values[1:]
livraisons=df3.iloc[0].values[1:]


historique=getHistorique(df4,nbsemaines)
""""""
datas=pd.DataFrame()
datas['Semaines']=semaines
datas['Livraisons réelles']=livraisons
datas['Historique']=historique



#predictnaiv=[]
#for i in range(len(historique)):
#    predictnaiv.append((historique[i][-1]))
#errquadnaiv=sqrt(mean_squared_error(predictnaiv,livraisons)) 

predict=[]
for i in range(len(historique)):
    predict.append(np.mean(historique[i][-i-1:]))
errquadmoy=sqrt(mean_squared_error(predict,livraisons))

regr=linear_model.Ridge()
regr.fit(historique, livraisons)
predictregr=regr.predict(historique)
ecartmoyregr=sqrt(mean_squared_error(livraisons, predictregr))    

#Exponential Moving Average
ema=[]
for i in range(len(historique)):
    ema.append(pd.DataFrame(historique[i]).ewm(alpha=0.045,adjust=False).mean())
predictewma=[]
for i in range(len(historique)):
    predictewma.append(ema[i].iloc[35,0])
errquadmewma=sqrt(mean_squared_error(predictewma,livraisons))



#Holter's Winter
listlivraison=livraisons.tolist()

sm.tsa.seasonal_decompose(listlivraison,freq=5,model='additive').plot()
resultat = sm.tsa.stattools.adfuller(datas['Livraisons réelles'])
plt.show()
modelholter = ExponentialSmoothing(listlivraison,seasonal_periods=35,trend='add',seasonal='add').fit()
predictwinter = modelholter.forecast(len(listlivraison))

#PLOTING
r= list(range(1,len(semaines)+1))
rw= list(range(1,len(semaines)+2))
for i in range(len(semaines)):
        for j in range(len(historique[i])):
            #Shistorique.append(historique[i][j])
           plt.scatter(r[i],historique[i][j],s=2, c="green")          
#plt.figure(figsize=(10,10))
#plt.rcParams["figure.figsize"] = [16,9]  
           
plt.figure()     
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
plt.show()

livraisons=np.insert(livraisons,35,livraisons[35])
predictwinter=np.insert(predictwinter,0,predictwinter[0]) 
errquadwinter=sqrt(mean_squared_error(predictwinter,livraisons))   
plt.figure()
plt.plot(rw,livraisons,label="Livraisons réelles")
plt.plot(rw,predictwinter,label="prédiction holtwinter")
plt.show() 




