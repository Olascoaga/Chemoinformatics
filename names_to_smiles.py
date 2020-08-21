# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 22:59:49 2020

@author: olask
"""

import pandas as pd
from urllib.request import urlopen
import csv

molecules = []
with open('DrugAgeDB.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        molecules.append(row[0])
del inputfile

df = pd.DataFrame(columns = ['Name', 'SMILES'])

def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'

for molecule in molecules:
    new_row = {'Name': molecule, 'SMILES': CIRconvert(molecule)}
    df = df.append(new_row, ignore_index=True)

df.to_csv(r'molecules_smiles.csv', index = False, header=True)
