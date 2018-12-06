# -*- coding: utf-8 -*-
"""
Code permettant d'importer des données xlsl en format DataFrame
"""

import pandas as pd
import numpy as np


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


""""""
datas=pd.DataFrame()
datas['Semaines']=semaines
datas['Livraisons réelles']=livraisons
datas['Historique']=getHistorique(df4,nbsemaines)

