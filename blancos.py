# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:03:25 2020

@author: olask
"""

import glob
import pandas as pd
from pypdb import *
import urllib.parse
import urllib.request

csv_files = glob.glob('*.csv') # Especificamos un patron de busqueda de archivos

mol_names = [] 
for filename in csv_files:
    mol_names.append(filename.split(".csv")[0]) # Separamos el nombre de la extensión .csv

dfs = [] # Lista vacia en donde guardaremos los df
columnas = ['zscore', 'Uniplot']
for filename in csv_files: # Recorremos los archivos y guardamos cada uno en la lista dfs[]
    data = pd.read_csv(filename, skiprows=[0], usecols=columnas)
    data = data.sort_values(by=['zscore'], ascending=False)
    data = data.loc[data['zscore'] > 1.96]
    dfs.append(data)

moleculas = []
for i in range(len(dfs)):
    molecula = [mol_names[i]] * len(dfs[i])
    for elemento in molecula:
        moleculas.append(elemento)
df = pd.concat(dfs)
df['Molecule'] = moleculas 


uniplot_ids = df['Uniplot'].tolist()
uniplot_ids = list(dict.fromkeys(uniplot_ids))
url = 'https://www.uniprot.org/uploadlists/'

genes = []
for id in uniplot_ids:
    params = {
        'from': 'ACC+ID',
        'to': 'GENENAME',
        'format': 'list',
        'query': id
        }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
        genes.append(response.decode('utf-8').strip())
        
zip_iterator = zip(uniplot_ids, genes)
diccionario = dict(zip_iterator)      
uniplot = df['Uniplot'].tolist()
genes = []
for id in uniplot:
    genes.append(diccionario[id])
df['Gen name'] = genes

df.to_csv('resultados.csv', index=False)
