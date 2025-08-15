import ash
import openmm as opm
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(cur_dir)
xml_path = base_dir+"/system_all.xml"

def singlepoint(filename, 
                qmatomlist, qm_charge, qm_mult, 
                act_nelec, act_norb, 
                set_atom_list=None, set_atom_charges=None, 
                numcores=12, label=None):
    
    frag = ash.Fragment(pdbfile=filename)
    
    openmmobject = ash.OpenMMTheory(fragment=frag, pdbfile=filename, xmlsystemfile=xml_path, xmlfiles=["charmm36.xml","charmm36/water.xml"], 
                                periodic=True, autoconstraints=None, rigidwater=False, numcores=numcores)
    
    openmmobject.remove_all_constraints()

    if set_atom_list is not None:
        
        system = openmmobject.system
        for force in system.getForces():
            if isinstance(force, opm.NonbondedForce):
                nonbounded_force = force
                break
        
        for i, charge in zip(set_atom_list, set_atom_charges):
            _, sigma, epsilon = nonbounded_force.getParticleParameters(i)
            nonbounded_force.setParticleParameters(i, charge, sigma, epsilon)

    pyscfobject = ash.PySCFTheory(numcores=numcores, scf_type='UKS', 
                            basis="631G", functional='B3LYP', gridlevel=2,
                            CAS=True, CASSCF=False, active_space=[act_nelec, act_norb], 
                            mcpdft=True, mcpdft_functional='tPBE',
                            tencirchem=True, label=label, ansatz='HEA', 
                            engine="tensornetwork")

    qmmmobject = ash.QMMMTheory(qm_theory=pyscfobject, mm_theory=openmmobject,
        fragment=frag, embedding="Elstat", qmatoms=qmatomlist, printlevel=2, qm_charge=qm_charge, qm_mult=qm_mult)

    ash.Singlepoint(theory=qmmmobject, fragment=frag)
    energy = qmmmobject.QMenergy
    return energy, qmmmobject