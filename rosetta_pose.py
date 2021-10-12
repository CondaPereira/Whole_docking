from pyrosetta import *
import os 
init()
pose = pose_from_pdb("pdb3m5q.pdb")
pose.sequence()
from pyrosetta.toolbox import cleanATOM
cleanATOM("pdb3m5q.pdb")
pose_clean = pose_from_pdb("pdb3m5q.clean.pdb")
pose_clean.sequence()
pose.annotated_sequence()
pose_clean.annotated_sequence()
os.system("chmod a+x -R *")