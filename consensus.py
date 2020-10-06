# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:58:20 2020

@author: olask
"""

import pandas as pd
import glob
from scipy.stats import zscore
import os
import numpy as np

os.makedirs('results', exist_ok=True)

csv_files = glob.glob('*.csv') # Especificamos un patron de busqueda de archivos
dfs = [] # Lista vacia en donde guardaremos los df
for filename in csv_files: # Recorremos los archivos y guardamos cada uno en la lista dfs[]
    data = pd.read_csv(filename)
    dfs.append(data)

def df_processing(df):
    df = df[pd.to_numeric(df['Affinity'], errors='coerce').notnull()]
    df['Ligand'] = df['Ligand'].str.split('_', expand=True)[1].tolist()
    df.sort_values(by=['Affinity'], axis=0, ascending=True, inplace=False, kind='quicksort')
    df['Z score'] = zscore(df['Affinity'].astype(float)) * -1
    df = df.drop_duplicates(subset=['Ligand'])
    df.sort_values(by=['Ligand'], axis=0, ascending=True, inplace=True, kind='quicksort')
    return df

procesados = []    
for df in dfs:
    df = df_processing(df)
    procesados.append(df)
del data, df, filename

for i in range(len(procesados)):
    procesados[i].to_csv('results/' + csv_files[i], index=False)    

if len(procesados[0]) < len(procesados[1]):
    farmacos = procesados[0]['Ligand'].tolist()
    #df = df[df['Gene Symbol'].isin(content)]
    procesados[1] = procesados[1][procesados[1]['Ligand'].isin(farmacos)]
else:
    farmacos = procesados[1]['Ligand'].tolist()
    #df = df[df['Gene Symbol'].isin(content)]
    procesados[0] = procesados[0][procesados[0]['Ligand'].isin(farmacos)]
    
consenso = pd.DataFrame()
consenso['Ligand'] = farmacos
v1 = procesados[0]['Z score'].to_numpy()
v2 = procesados[1]['Z score'].to_numpy()
consenso['Z Mean'] = (v1 + v2) / 2
consenso.to_csv('results/consenso.csv', index=False)    
