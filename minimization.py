from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
import os 
os.system("gmx pdb2gmx -f pdb3m5q.clean.pdb -o repair.pdb -ignh")
print('Loading...')
pdb = PDBFile('repair.pdb')
forcefield = ForceField('amber99sb.xml', 'tip3p.xml')
modeller = Modeller(pdb.topology, pdb.positions)
print('Adding hydrogens...')
modeller.addHydrogens(forcefield)
print('Adding solvent...')
modeller.addSolvent(forcefield, model='tip3p', padding=1*nanometer)
print('Minimizing...')
system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME)
force = CustomExternalForce('100*max(0, r-2)^2; r=sqrt(x*x+y*y+z*z)')
system.addForce(force)
for i in range(system.getNumParticles()):
    force.addParticle(i, [])
integrator = LangevinMiddleIntegrator(300*kelvin, 91/picosecond, 0.004*picoseconds)
simulation = Simulation(modeller.topology, system, integrator)
simulation.context.setPositions(modeller.positions)
simulation.minimizeEnergy(maxIterations=100)
simulation.reporters.append(PDBReporter('output.pdb', 1000))
print('Saving...')
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(simulation.topology, positions, open('output.pdb', 'w'))
print('Done')

os.system('grep -v -e ')