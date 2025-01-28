#!/usr/bin/env python
# coding: utf-8

import os
import glob
import pandas as pd
from pathlib import Path


import numpy as np
import matplotlib.pyplot as mlt

from rdkit.Chem import PandasTools
from rdkit import DataStructs
from rdkit.Chem import Draw

fmask = '*smi'
outdir = '/media/arma/DATA/Proje_3501/LIBRARY/CommerciallyAvailable/H0/UNIQUES/'

for files in glob.glob(fmask):
    fileName = files.rsplit('.', 1)[0]
    print(fileName)
    print("-------------------------------------------------------------------")
    df = pd.read_csv(files, sep='\t', header=None)
    df = pd.read_csv(files, sep='\t', header=None)
    df.columns=['SMILES', 'ZINCID', 'CatalogName', 'Supplier']
    df.sort_values(by = 'ZINCID', inplace=True)
    df.groupby(by=["ZINCID"]).nunique()
    molecule_zinc_id = df["ZINCID"]
    dupMols = df[molecule_zinc_id.isin(molecule_zinc_id[molecule_zinc_id.duplicated()])]
    dupMols.groupby('ZINCID').nunique()
    indexToRemove = dupMols.index
    NoDuplicate = df[~df.index.isin(indexToRemove)]
    NoInformerSupplier = NoDuplicate[(NoDuplicate['Supplier'] != 'informer2') & (NoDuplicate['Supplier'] != 'informer')]

    InformerSupplier = NoDuplicate[(NoDuplicate['Supplier']== 'informer2') | (NoDuplicate['Supplier']== 'informer')]
    SuppInformerDup = dupMols[(dupMols['Supplier'] == 'informer2') | (dupMols['Supplier'] == 'informer')]
    ID = SuppInformerDup.ZINCID
    mask = dupMols['ZINCID'].isin(ID)
    NoInformerSupp_Dup = dupMols[~mask]
    NoInformerSupp_Dup= NoInformerSupp_Dup.drop_duplicates(subset=['ZINCID'])
    InformerSupp_Dup = dupMols[mask]
    InformerSupp_Dup.groupby(['ZINCID']).nunique()['Supplier'] == 1
    InformerSupp_Dup.groupby(['ZINCID', 'Supplier']).sum()
    # Now check whether any of the compounds with informer2 supplier has only that supplier or more
    a = InformerSupp_Dup.groupby('ZINCID')['Supplier'].agg(MyCount='count')['MyCount']
    b = a[a == 1]
    len(b)
    if len(b) != 0:
            print("Warning")
    #Now drop duplicates from the dataframe of molecules with informer2 supplier
    Dupp_SuppInf_checked = InformerSupp_Dup.drop_duplicates(subset='ZINCID')
    unique_checked = pd.concat([NoInformerSupplier, NoInformerSupp_Dup, Dupp_SuppInf_checked])
    unique_checked.drop_duplicates(subset=['CatalogName'], inplace=True)
    unique_checked.drop_duplicates(subset=['ZINCID'], inplace=True)
    unique_checked.drop_duplicates(subset=['SMILES'], inplace=True)
    print(f'There are {len(df)} number of molecules in initial files')
    #Check the number of unique SMILES
    print(f'Unique SMILES in the initial smi file is', len(df.groupby('ZINCID')) )
    print(f'Molecules with Informer2 as the only supplier is', len(InformerSupplier) + len(b))
    print(f'In total the unique molecule number in stock is', len(df.groupby('ZINCID')) - len(InformerSupplier)- len(b))
    print(f'The number of molecules in final concatenated file is', len(unique_checked))
    #After check save the file to UNIQUES folder
    p = Path(outdir).joinpath(f"{fileName}_unique.smi")
    #print(p)
    unique_checked.to_csv(p,index=False)

    print("-------------------------------------------------------------------")










