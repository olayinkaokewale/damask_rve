import h5py
import numpy as np
import amtplotlib.pyplot as plt

stress_list = []
strain_list = []
incs_list = []

d = damask.Result(i)

d.add_stress_Cauchy()
d.add_strain()
d.add_equivalent_Mises('sigma')
d.add_equivalent_Mises('epsilon_V^0.0(F)')
            
f = h5py.File(d.fname)
            
for path in d.get_dataset_location('sigma_vM'):
    incs_list.append(path.split('/')[0])
    stress_list.append(np.average(f[path]))
for path in d.get_dataset_location('epsilon_V^0.0(F)_vM'):
    strain_list.append(np.average(f[path]))


plt.plot(strain_list, stress_list)