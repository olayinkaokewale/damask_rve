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

# 0. Set the dictionary mapping 'grain numbers' to 'cells'
simulations = [
    [20,14],
    [20,18],
    [20,24]
]

markers = [".","o","*","v","p",">","d","+","x","s"]

def plotResults():
    plt_datas = []

    for index,simulation in enumerate(simulations):
        grains = simulation[0]
        cell = simulation[1]
        file_name = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        plt_data = {
            'stress': [],
            'strain': [],
            'incs': [],
            'label': f'{grains} - [{cell},{cell},{cell}]',
            'markers': markers[index]
        }

        input_file = f'{simulation_base_path}/{file_name}/simulation/{file_name}_{fname_suffix}.hdf5'

        d = damask.Result(input_file)

        d.add_stress_Cauchy()
        d.add_strain()
        d.add_equivalent_Mises('sigma')
        d.add_equivalent_Mises('epsilon_V^0.0(F)')
                    
        f = h5py.File(d.fname)
                    
        for path in d.get_dataset_location('sigma_vM'):
            plt_data['incs'].append(path.split('/')[0])
            plt_data['stress'].append(np.average(f[path]))
        for path in d.get_dataset_location('epsilon_V^0.0(F)_vM'):
            plt_data['strain'].append(np.average(f[path]))
        
        plt_datas.append(plt_data)

    plt.figure()
    # plt.plot(strain_list, stress_list, linestyle="-.")
    for data in plt_datas:
        plt.plot(data['strain'], data['stress'], linestyle='-', label=data['label'], marker=data['markers'])
    plt.ylabel('$\sigma$ (MPa)')
    plt.xlabel('$\epsilon$')
    plt.legend(loc='lower right')
    plt.title("stress-strain plot")
    plt.savefig(f'{output_folder}/stress_strain_plot.png', bbox_inches='tight')



# 1. Create the plot directory if it doesn't exist
output_folder = 'plots/20s'
createDirectory(output_folder)

# 2. Run through the simulations
plotResults()