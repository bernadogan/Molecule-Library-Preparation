#!/usr/bin/env python
# coding: utf-8


import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as mlt

from rdkit.Chem import PandasTools
from rdkit import DataStructs
from rdkit.Chem import Draw
from rdkit.Chem import RemoveStereochemistry
from rdkit.Chem import MolToSmiles
from rdkit.Chem import MolFromSmiles



def smiles_noChiral(smiles):
    #remove the chirality from SMILES codes
    mol = MolFromSmiles(smiles)
    RemoveStereochemistry(mol)
    #print( MolToSmiles(mol))
    return MolToSmiles(mol)


df = pd.read_csv(sys.argv[1],  )
print(df.info())
df.drop_duplicates(subset=["ZINCID"], inplace=True)
df.drop_duplicates(subset=["CatalogName"], inplace=True)
df.drop_duplicates(subset=["SMILES"], inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)


df['SMILES_noChiral'] = df['SMILES'].apply(smiles_noChiral)
df["all_SMILES"]=df.groupby(by="SMILES_noChiral", )['SMILES'].transform(lambda x: ','.join(x))
df["all_ZINCID"]=df.groupby(by="SMILES_noChiral", )['ZINCID'].transform(lambda x: ','.join(x))
df["all_CatalogName"]=df.groupby(by="SMILES_noChiral", )['CatalogName'].transform(lambda x: ','.join(x))
df["all_Supplier"]=df.groupby(by="SMILES_noChiral", )['Supplier'].transform(lambda x: ','.join(x))
df = df[(df['Supplier'] != 'zinc20-stock-rev-1') & (df['Supplier'] != 'zinc20-instock')]


df_new = df.drop(["SMILES", "ZINCID", "CatalogName", "Supplier"], axis=1)
df_new.rename(columns={"SMILES_noChiral": "SMILES"}, inplace=True)
df_new.drop_duplicates("SMILES", inplace=True)

print(f'Unique CatalogName in the final file is', len(df_new.groupby('SMILES')) )

df_new['ZINCID'] = df_new['all_ZINCID'].str.split(",", expand=True)[0]
df_new=df_new[['SMILES', 'ZINCID', 'all_SMILES', 'all_ZINCID', 'all_CatalogName', 'all_Supplier']]
df_new.to_csv(sys.argv[2], index=False)






