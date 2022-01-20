import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
import matplotlib.pyplot as plt
import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

simulation_base_path = '/nethome/o.okewale/examples/sim_results'
# times_for_CA   = np.arange(0.25,2.25,0.25)
times_for_CA   = [2.0]
markers = [".","o","*","v","p",">","d","+","x","s"]

def plotResults(simulation_sample_name:str):
    plt_datas = []

    # time = '0.75'
    for index, time in enumerate(times_for_CA):
        input_file = f'{simulation_base_path}/{simulation_sample_name}/2000_stand/CA_files/{time}/.fractions.txt'
        plt_data = {
            'time': [],
            'fraction': [],
            'label': time,
            'markers': markers[index]
        }
        with open(input_file) as f:
            lines = f.readlines()
            plt_data['time'] = [round(float(line.split()[0]),2) for line in lines]
            plt_data['fraction'] = [round(float(line.split()[1]),2) for line in lines]
        plt_datas.append(plt_data)
        # print(plt_data)
        

    plt.figure()
    for data in plt_datas:
        plt.plot(data['time'], data['fraction'], linestyle='-', color='red', label=data['label'], marker=data['markers'])
    plt.xlabel('$t$ (s)')
    plt.ylabel('$X$')
    # plt.legend()
    plt.savefig(f'{output_folder}/{simulation_sample_name}_rx_fractions_plot.png', bbox_inches='tight')

# 0. Set the dictionary mapping 'grain numbers' to 'cells'
dicts = {
    '20': '18',
    '40': '22',
    '60': '25'
}

# 1. Create the plot directory if it doesn't exist
output_folder = 'plots/fractions'
createDirectory(output_folder)

# 2. Run through the simulations
# plotResults('Polycrystal_20_18x18x18')
for grain_number in dicts.keys():
    cell = dicts.get(grain_number)
    plotResults(f'Polycrystal_{grain_number}_{cell}x{cell}x{cell}')