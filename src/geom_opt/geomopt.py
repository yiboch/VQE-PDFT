import ash
import os
 
curdir = os.getcwd()
 
qmatomlist372 = range(5838, 5853, 1)  # indole ring on TrpB W372 
qmatomlist318 = range(4930, 4945, 1)  # indole ring on TrpC W318 
actregion = list(qmatomlist372) + list(qmatomlist318)

basisset = '631G*'

def gopt(filename, qmatomlist, qm_charge, qm_mult, optimized_filename, numcores=16):

    if 'pdb' in filename:
        frag = ash.Fragment(pdbfile=filename)
    else:
        frag = ash.Fragment(xyzfile=filename)

    openmmobject = ash.OpenMMTheory(pdbfile=filename, xmlsystemfile="system_all.xml", xmlfiles=["charmm36.xml","charmm36/water.xml"], 
                                periodic=True, autoconstraints=None, rigidwater=False, numcores=numcores)
    
    openmmobject.remove_all_constraints()

    pyscfobject = ash.PySCFTheory(numcores=numcores, scf_type='UKS', 
                            basis=basisset, functional='CAM_B3LYP', gridlevel=2)

    qmmmobject = ash.QMMMTheory(qm_theory=pyscfobject, mm_theory=openmmobject,
        fragment=frag, embedding="Elstat", qmatoms=qmatomlist, printlevel=2, qm_charge=qm_charge, qm_mult=qm_mult)
    
    ash.geomeTRICOptimizer(theory=qmmmobject, 
                           fragment=frag, 
                           ActiveRegion=True, 
                           actatoms=actregion, 
                           maxiter=250, 
                           optimized_filename=optimized_filename)

for frame in os.listdir(curdir):
    folder_path = os.path.join(curdir, frame)
    if os.path.isdir(folder_path) and frame.isdigit():
        
        pdb_file = os.path.join(folder_path, f"{frame}.pdb")
        fn1 = folder_path + '/optimized-372p318n'
        fn = fn1+'.pdb'
        if not os.path.exists(fn):
            print(f'\033[1;32mOptimizing: {fn}\033[0m')
            gopt(filename=pdb_file, qmatomlist=qmatomlist372, qm_charge=1, qm_mult=0, optimized_filename=fn1)
        else:
            print(f'\033[1;32mIgnore optimizing: {fn}\033[0m')
        
        fn2 = folder_path + '/optimized-372n318p'
        fn = fn2+'.pdb'
        if not os.path.exists(fn):
            print(f'\033[1;32mOptimizing: {fn}\033[0m')
            gopt(filename=fn1+'.pdb', qmatomlist=qmatomlist318, qm_charge=1, qm_mult=0, optimized_filename=fn2)
        else:
            print(f'\033[1;32mIgnore optimizing: {fn}\033[0m')