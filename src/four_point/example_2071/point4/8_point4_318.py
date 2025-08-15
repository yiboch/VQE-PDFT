#%%
import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
pdb_dir = os.path.dirname(cur_dir)
cal_dir = os.path.dirname(pdb_dir)

final_file_name='E_p4_318.pkl'
ffn = os.path.join(cur_dir, final_file_name)
if os.path.exists(ffn):
    print(f"{ffn} already exists, jumping")
    exit()

if cal_dir not in sys.path:
    sys.path.append(cal_dir)
    print("cal path added to the PYTHONPATH")
else:
    print("cal path already in the PYTHONPATH")

import singlepoint_main as SP

qmatomlist372 = range(5838, 5853, 1)  # indole ring on TrpB W372 
qmatomlist318 = range(4930, 4945, 1)  # indole ring on TrpC W318 
actregion = list(qmatomlist372) + list(qmatomlist318)

import pickle
filename = cur_dir+"/qm_charge_372.pkl"
with open(filename, 'rb') as f:
    data = pickle.load(f)

qm_charge_372 = data["qm_charge_372"]

point4_e318, _ = SP.singlepoint(filename=pdb_dir+'/optimized-372n318p.pdb',
                                qmatomlist=qmatomlist318, qm_charge=0, qm_mult=1,
                                set_atom_list=qmatomlist372, set_atom_charges=qm_charge_372,
                                act_nelec=4, act_norb=3, label='point4-318n')

print('='*35)
print("p4_318:", point4_e318)
print('='*35)

ouput_data = {
    "p4_318": point4_e318
}

with open(ffn, 'wb') as f:
    pickle.dump(ouput_data, f)