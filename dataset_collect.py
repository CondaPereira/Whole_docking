from Bio.PDB import *
from biopandas.pdb import PandasPdb
import Bio
from Bio.PDB import PDBList
ppdb0 = []
ppdb1 = []
pdbl = PDBList()
PDBlist2 = ['1aki', '3m5q']
for i in PDBlist2:
    ppdb0.append(pdbl.retrieve_pdb_file(i,pdir='.', file_format ='pdb'))
    ppdb1.append(PandasPdb().fetch_pdb(i))
import os
def renaming(file):
    
    ext = os.path.splitext(file)   
 
    if ext[1] == '.ent':                    
        new_name = ext[0] + '.pdb'        
        os.rename(file, new_name)        
    elif ext[1] == '.pdb':
        new_name = ext[0] + '.ent'
        os.rename(file, new_name)
 
 
def tree(path):
    
    files = os.listdir(path)   
    for file in files:
        file_path = os.path.join(path, file) 
        if os.path.isdir(file_path):   
            tree(file_path)    
        else:
            os.chdir(path)      
            renaming(file)      
 
 
this_path = os.getcwd()   
tree(this_path)

os.system('rm -rf obsolete')
os.system('ls')
os.system('mkdir proteindatabank')
os.system('mv *.pdb /home/szk/scripts/proteindatabank')
os.system('chmod a+x -R *')
