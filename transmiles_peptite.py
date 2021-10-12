from rdkit import Chem
from rdkit.Chem import Draw 
from rdkit.Chem.Draw import IPythonConsole
IPythonConsole.ipython_useSVG = True

peptide_smiles = Chem.MolToSmiles(Chem.MolFromFASTA("RGDfK"))

#here you can define much more fasta file format to the smiles format which by Christopher
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import AllChem
from rdkit.Chem import rdFreeSASA

mol1 = Chem.MolFromSmiles(peptide_smiles)
mol2 = Chem.MolFromSmiles('Oc1ccncc1')

#add H atoms
hmol1 = Chem.AddHs(mol1)
hmol2 = Chem.AddHs(mol2)

AllChem.EmbedMolecule(hmol1)
AllChem.EmbedMolecule(hmol2)

radii1 = rdFreeSASA.classifyAtoms(hmol1)
radii2 = rdFreeSASA.classifyAtoms(hmol2)
#Here we can calculate the sasa of the micromolecule
rdFreeSASA.CalcSASA(hmol1, radii1)
rdFreeSASA.CalcSASA(hmol2, radii2)

atoms1 = hmol1.GetAtoms()
atoms2 = hmol2.GetAtoms()

for i in range(len(atoms1)):
    print(atoms1[i].GetSymbol(), atoms1[i].GetProp('SASAClassName'), atoms1[i].GetProp("SASA"))
    
sum(float(a.GetProp("SASA")) for a in atoms1)

for i in range(len(atoms2)):
    print(atoms2[i].GetSymbol(), atoms2[i].GetProp('SASAClassName'), atoms2[i].GetProp("SASA"))
     
sum(float(a.GetProp("SASA")) for a in atoms2)