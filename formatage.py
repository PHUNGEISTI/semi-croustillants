# -*- coding: utf-8 -*-
"""
Fonctions permettant l'import de données xlsx
"""

import numpy as np
import pandas as pd

def reformaterHisto(df,nbsemaines):
    """Reformate l'historique de toutes les prévisions de datas

    Arguments :
        df -- données à formater (DataFrame)
        nbsemaines -- Nombre de semaines de datas (int)
    """
    
    historique=[]
    for i in range(nbsemaines): # colonnes
        hist_tmp=[]
        for j in range(nbsemaines-2,-1,-1): # lignes # pour le bon nb de lignes, nbsemaines-1
            if not(np.isnan(df.iloc[j,i+1])):
                hist_tmp.append(df.iloc[j,i+1])
        for j in range(len(hist_tmp),nbsemaines):
            hist_tmp.append(0)
        historique.append(hist_tmp[::-1])
    return historique

def formaterXLSX(nomfichier='2018-19ProjetJohnsonElectricArbitrageFeuilledecalcul.xlsx'):
    """Formate un fichier Excel en DataFrame Python utilisable par l'algorithme
    
    Argument :
        nomfichier -- nom du fichier à importer (string)
    """
  
    # Ouverture
    df = pd.read_excel(nomfichier,sheet_name='pivot demande')
    # Formatage
    df2=df.drop([0,1,2,4,(df.shape[0]-1)])
    df2=df2.iloc[:,:df2.shape[1]-1]
    
    # Reconstruction de l'index
    df3=df2.reset_index(drop=True)
    # Cohérence types
    df3['Unnamed: 1']=df3['Unnamed: 1'].astype(float)
    # Formatage
    df4=df3.drop([0,1])
    
    # Calcul du nb de semaines, construction des listes de semaines et des livraisons réelles
    nbsemaines=df3.shape[1]-1
    semaines=df3.iloc[1].values[1:]
    livraisons=df3.iloc[0].values[1:]
    
    # DataFrame final
    datas=pd.DataFrame()
    datas['Semaines']=semaines
    datas['Livraisons réelles']=livraisons
    datas['Historique']=reformaterHisto(df4,nbsemaines)
    return datas

