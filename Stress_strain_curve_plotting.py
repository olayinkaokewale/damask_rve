import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import damask
import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

simulation_base_path = '/nethome/o.okewale/examples/sim_results'
fname_suffix = 'tensionX'

def plotResults(simulation_sample_name:str):
    stress_list = []
    strain_list = []
    incs_list = []

    input_file = f'{simulation_base_path}/{simulation_sample_name}/simulation/{simulation_sample_name}_{fname_suffix}.hdf5'

    d = damask.Result(input_file)

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

    plt.figure()
    plt.plot(strain_list, stress_list)
    plt.savefig(f'plots/{simulation_sample_name}_stress_strain_plot.png', bbox_inches='tight')

# 0. Set the dictionary mapping 'grain numbers' to 'cells'
dicts = {
    '20': '18',
    '40': '22',
    '60': '25'
}

# 1. Create the plot directory if it doesn't exist
createDirectory('plots')

# 2. Run through the simulations
for grain_number in dicts.keys():
    # print(key, dicts.get(key))
    cell = dicts.get(grain_number)
    plotResults(f'Polycrystal_{grain_number}_{cell}x{cell}x{cell}')