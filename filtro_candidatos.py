# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:49:56 2020

@author: olask
"""

import glob
import pandas as pd
import numpy as np

reference = int(input("Numero de moleculas de referencia: "))
top = int(input("Numero de moleculas que quieres como candidatas: "))

csv_files = glob.glob('*.csv') # Especificamos un patron de busqueda de archivos
dfs = [] # Lista vacia en donde guardaremos los df
for filename in csv_files: # Recorremos los archivos y guardamos cada uno en la lista dfs[]
    data = pd.read_csv(filename,  index_col=[0])
    dfs.append(data)
del data, filename, csv_files

max_similarity = []
for i in range(len(dfs)): # Pre-procesamiento de los data frames
    dfs[i] = dfs[i].where(np.tril(np.ones(dfs[i].shape), -1).astype(np.bool)) # Obtenemos el triangulo superior de la matriz
    dfs[i].drop(dfs[i].iloc[:, :reference], inplace = True, axis = 0) # Nos quedamos con las columnas de nuestras moleculas de referencia
    dfs[i].drop(dfs[i].iloc[:, reference:], inplace = True, axis = 1) # Nos quedamos con las columnas de nuestras moleculas de referencia
    max_similarity.append(dfs[i].max(axis = 1, skipna = True))
del dfs

max_similarity = pd.DataFrame(max_similarity).transpose()
max_similarity['average'] = max_similarity.mean(axis=1)
max_similarity= max_similarity.loc[max_similarity['average'] < 1].sort_values(by=['average'], ascending=False)
molecules = max_similarity['average'].head(top)
molecules = molecules.index.tolist()

candidates = []
for elemento in molecules:
    b = [k for k in elemento if k.isdigit()]
    n = ""
    n = n.join(b)
    elemento = "Compound " + n
    candidates.append(elemento)
    
df = pd.read_csv('lib\quimioteca.csv')
candidates = df[df.Name.isin(candidates)]
candidates.to_csv(r'lib\candidates.csv', index = False, header=True)
