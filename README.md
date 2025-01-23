# ZINC22_LibraryPrep
This is a repository about virtual library preparation. 
- First, the 2D structures of molecules that could be purchashed were downloaded in SMILES formats. (Hevay atom number 17-25, logP values -5 to 3.4)
- Obtained molecules were cleaned up as they contained duplicates in terms of ZINCID, Catalog ID and Supplier Information.
- There were filtering of molecules also based on the structural alerts (such as PAINS) (rd_filters script of Pat Walkers were used)
- From around 13 billion SMILES obtained, a subset were required to be selected:
      - In this case, the priority was given to molecules existing in ZINC20 library that are small world molecules. All of these small word molecules were selected.
      - To select diverse set of molecules, the obtained SMILES which were isomeric were converted to canonical ones. Then, randomly SMILES were selected based on their heavy             atom number.
      - In total, over 13 million molecules were selected as a diverse subset and the SMILES were reverted back to isomeric ones.
- Openeye OMEGA was utilized to generate 3D structures from selected SMILES codes of molecules. Firstly, filter utility of OMEGA was used and the protonation states were assigned in addition to remoing some molecules with undesired properties again. Then Openeye tautomers were utilized to obtain the possible tautomeric states of molecules that can exist. After that, OMEGA was used to generate single conformer for each molecule. There were problematic molecules for which 3D structres could not be obtained. Other approached such as using rdkit library also did not generate 3D structures. The analysis reviewed problems with the assigned chiralities of some atoms especially for macromolecules in SMILES codes. But seen it is not clear whether the generated 3D structure with chiralities different than the assigned one could be purchashed, these molecules are ignored/filtered out. 
