#!/usr/bin/env python
# coding: utf-8

# In[16]:


# importing and path definition
from time import time
import math
import sys
import faiss
import h5py
import csv
from functools import wraps
from time import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from tqdm import tqdm
from sklearn.manifold import TSNE
import umap



#Read the file containing fingerprints 
h5f = h5py.File(sys.argv[1], 'r') 
h5f.keys()
x = h5f['fp_list'][:]
smiles_list = h5f['smiles_list'][:]
name_list = h5f['name_list'][:]
h5f.close()


smiles_ls = []
for smiles in smiles_list:
    a = smiles[0].decode('utf-8')
    smiles_ls.append(a)


names_ls = []
for names in name_list:
    a = names[0].decode('utf-8')
    names_ls.append(a)



fp_df = pd.DataFrame.from_dict(zip(smiles_ls, names_ls, x))
fp_df.columns=['SMILES', 'ZINCID', 'FP', ]


fp_Morgan_1024 = list((fp_df['FP'].values))

#TSE using fingerprints and PCA results
pca_Morgan_1024 = PCA(n_components=100)
crds_Morgan_1024 = pca_Morgan_1024.fit_transform(fp_Morgan_1024) 
crds_Morgan_1024_embedded = TSNE(n_components=2, perplexity=40, n_iter=5000, random_state=10, init='pca').fit_transform(crds_Morgan_1024)
tsne_Morgan_1024_df = pd.DataFrame(crds_Morgan_1024_embedded,columns=["X","Y"])


tsne_Morgan_1024_df['Name'] = fp_df['ZINCID']
tsne_Morgan_1024_df['SMILES'] = fp_df['SMILES']


#fig = plt.figure(figsize=(12, 10))
#ax = sns.scatterplot(data=tsne_Morgan_1024_df,x="X",y="Y",)
#ax.set_xlabel('t-SNE1', fontsize=18)
#ax.set_ylabel('t-SNE2', fontsize=18)
#ax.legend(fontsize=14, facecolor='w', loc=4)
#plt.tight_layout()
#fig.legend(loc='upper right', bbox_to_anchor=(.75, 0.98))
#plt.show()

tsne_Morgan_1024_df.to_csv(sys.argv[2], index=False)


#UMAP using the fingerprints
clusterable_embedding = umap.UMAP(n_neighbors=25,min_dist=0.0,n_components=2).fit_transform(fp_Morgan_1024)
umap_Morgan_1024_df = pd.DataFrame(clusterable_embedding[:,:2],columns=["X","Y"])
umap_Morgan_1024_df['Name'] = fp_df['ZINCID']
umap_Morgan_1024_df['SMILES'] = fp_df['SMILES']


#fig = plt.figure(figsize=(12, 10))
#ax = sns.scatterplot(data=umap_Morgan_1024_df,x="X",y="Y",)
#ax.set_xlabel('umap1', fontsize=18)
#ax.set_ylabel('umap2', fontsize=18)
#ax.legend(fontsize=14, facecolor='w', loc=4)
#plt.tight_layout()
#fig.legend(loc='upper right', bbox_to_anchor=(.75, 0.98))
#plt.show()

umap_Morgan_1024_df.to_csv(sys.argv[3], index=False)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} infile.h5 outfile(tsne).csv outfile(umap).csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

