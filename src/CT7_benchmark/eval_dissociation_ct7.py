#%%
import numpy as np
import pyscf.mcpdft
np.set_printoptions(linewidth=250)
import pyscf
import basis_set_exchange as bse


def get_jul_cc_pvtz_from_bse(atom_symbol):
    aug_basis = bse.api.get_basis("aug-cc-pVTZ", elements=atom_symbol)
    jul_basis = bse.manip.truhlar_calendarize(aug_basis, 'jul')
    jul_basis_str = bse.writers.write_formatted_basis_str(jul_basis, fmt='nwchem')
    jul = pyscf.gto.parse(jul_basis_str)
    return jul

dimmerdict = {'NH3-ClF':4, 
              'NH3-Cl2':4, 
              'NH3-F2':4, 
              'HCN-ClF':2, 
              'H2O-ClF':3, 
              'C2H2-ClF':4, 
              'C2H4-F2':6,
              }

spindict = {'NH3-ClF':(0,0),
            'NH3-Cl2':(0,0),
            'NH3-F2':(0,0),
            'HCN-ClF':(0,0),
            'H2O-ClF':(0,0), 
            'C2H2-ClF':(0,0), 
            'C2H4-F2':(0,0),
            }

as_dict = {'NH3-ClF':[(10,10), (8,8), (2,2)],
           'NH3-Cl2':[(10,10), (8,8), (2,2)],
           'NH3-F2':[(10,10), (8,8), (2,2)],
           'HCN-ClF':[(8,8), (2,2), (6,6)],
           'H2O-ClF':[(10,10), (8,8), (2,2)],
           'C2H2-ClF':[(10,10), (10,10), (2,2)],
           'C2H4-F2':[(10,10), (10,10), (2,2)],
           }

elem_dict = {'NH3-ClF':['N','H','Cl','F'],
             'NH3-Cl2':['N','H','Cl'],
             'NH3-F2':['N','H','F'],
             'HCN-ClF':['H','C','N','Cl','F'],
             'H2O-ClF':['H','O','Cl','F'],
             'C2H2-ClF':['C','H','Cl','F'],
             'C2H4-F2':['C','H','F']
             }

def seperate_atom(dimmer, dimmername):
    elements = dimmer.elements
    coords = dimmer.atom_coords(unit=dimmer.unit)
    n_atom = len(elements)
    sep = dimmerdict[dimmername]
    atoms1 = [[elements[i],coords[i]] for i in range(sep)]
    atoms2 = [[elements[i],coords[i]] for i in range(sep, n_atom)]
    return atoms1, atoms2

dimmername = 'NH3-ClF'
dimmerfile = f'./mol_all/{dimmername}.xyz'

basis = {elem:get_jul_cc_pvtz_from_bse(elem) for elem in elem_dict[dimmername]}

dimmer = pyscf.M(atom=dimmerfile, basis=basis, spin=0)

atoms1, atoms2 = seperate_atom(dimmer, dimmername)
spins = spindict[dimmername]
AS = as_dict[dimmername]
mol1 = pyscf.M(atom=atoms1, basis=basis, spin=spins[0])
mol2 = pyscf.M(atom=atoms2, basis=basis, spin=spins[1])

#%%
mf_as = AS[0]  # n_cas, n_elec
mf = pyscf.scf.RHF(dimmer)
mf.run()
mc = pyscf.mcpdft.CASCI(mf, 'tPBE', mf_as[0], mf_as[1])
mc.run()

m1_as = AS[1]  # n_cas, n_elec
mf1 = pyscf.scf.RHF(mol1)
mf1.run()
mc1 = pyscf.mcpdft.CASCI(mf1, 'tPBE', m1_as[0], m1_as[1])
mc1.run()

m2_as = AS[2]  # n_cas, n_elec
mf2 = pyscf.scf.RHF(mol2)
mf2.run()
mc2 = pyscf.mcpdft.CASCI(mf2, 'tPBE', m2_as[0], m2_as[1])
mc2.run()


e1 = mc1.e_tot
e2 = mc2.e_tot
e12 = mc.e_tot

dis_e = (e1 + e2 - e12) * 27.2114 * 23.0605
print(dis_e)
