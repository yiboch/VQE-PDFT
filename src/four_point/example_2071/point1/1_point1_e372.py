#%%
import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
pdb_dir = os.path.dirname(cur_dir)
cal_dir = os.path.dirname(pdb_dir)

final_file_name='E_p1_372.pkl'
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

point1_e372, qmmmobject = SP.singlepoint(filename=pdb_dir+'/optimized-372p318n.pdb',
                                qmatomlist=qmatomlist372, qm_charge=1, qm_mult=2, 
                                act_nelec=3, act_norb=3, label='point1-372p')

qm_charge_372 = qmmmobject.qm_theory.qm_mulliken_charge[:-1]


print('='*35)
print("p1_372:", point1_e372)
print('='*35)

ouput_energy_372 = {
    "p1_372": point1_e372,
}
import pickle

with open(ffn, 'wb') as f:
    pickle.dump(ouput_energy_372, f)

output_charge_372 = {
    "qm_charge_372": qm_charge_372,
}
charge_file_name=cur_dir+'/qm_charge_372.pkl'
with open(charge_file_name, 'wb') as f:
    pickle.dump(output_charge_372, f)
