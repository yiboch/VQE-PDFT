#%%
import pickle as pkl
import os
import numpy as np

cwd = os.getcwd()

res_318 = dict()
res_372 = dict()
for indole in [372,318]:
    for i in range(1,5):
        dir = os.path.join(cwd, f"point{i}")
        fn = os.path.join(dir, f"E_p{i}_{indole}.pkl")
        with open(fn, 'rb') as f:
            data = pkl.load(f)
            if indole == 372:
                res_372.update(data)
            else:
                res_318.update(data)

def reorg_E(res_dict, indole):
    lam_1 = abs(res_dict[f"p4_{indole}"] - res_dict[f"p1_{indole}"])
    lam_2 = abs(res_dict[f"p2_{indole}"] - res_dict[f"p3_{indole}"])
    return lam_1, lam_2

lam_318_1, lam_318_2 = reorg_E(res_318, 318)
lam_372_1, lam_372_2 = reorg_E(res_372, 372)

lam_318 = lam_318_1 + lam_318_2
lam_372 = lam_372_1 + lam_372_2

lam_tot = lam_318 + lam_372

delta_G0 = abs(res_318["p1_318"]+res_372["p1_372"] - res_318["p3_318"] - res_372["p3_372"])

hbar = 6.582119514e-16  # eV * s
kb = 8.617333262145e-5  # eV / K
T = 300  # K
pi = np.pi

H_DA = -2.02745953133272/1000
Delta_G0 = delta_G0 * 27.211
Lam_tot = lam_tot * 27.211

k = (2*pi/hbar) * (H_DA**2/np.sqrt(4*pi*Lam_tot*kb*T)) * np.exp(-(Delta_G0 + Lam_tot)**2/(4*Lam_tot*kb*T))

print(f'electron transfer rate: {k}/s')

print("="*4, "cloud local", "="*4)
print("point-1-372:", res_372['p1_372'])
print("point-1-318:", res_318['p1_318'])
print("point-2-372:", res_372['p2_372'])
print("point-2-318:", res_318['p2_318'])
print("point-3-372:", res_372['p3_372'])
print("point-3-318:", res_318['p3_318'])
print("point-4-372:", res_372['p4_372'])
print("point-4-318:", res_318['p4_318'])
print("="*20)
print("lam-1-372:", lam_372_1)
print("lam-2-372:", lam_372_2)
print("lam-372:", lam_372)
print("lam-1-318:", lam_318_1)
print("lam-2-318:", lam_318_2)
print("lam-318:", lam_318)
print("lam-tot:", lam_tot)
print("="*20)
print('Delta G0:', delta_G0)
# %%
