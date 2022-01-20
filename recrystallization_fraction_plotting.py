import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
import matplotlib.pyplot as plt
import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

simulation_base_path = '/nethome/o.okewale/examples/sim_results'

# 0. Set the array mapping 'grain numbers' to 'cells'
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
        filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        input_file = f'{simulation_base_path}/{filename}/2000_stand/CA_files/5.0/.fractions.txt'
        plt_data = {
            'time': [],
            'fraction': [],
            'label': f'{grains} - [{cell},{cell},{cell}]',
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
        plt.plot(data['time'], data['fraction'], linestyle='-', label=data['label'], marker=data['markers'])
    plt.xlabel('$t$ (s)')
    plt.ylabel('$X$')
    plt.legend(loc='lower right')
    plt.title("RX fraction - time plot")
    plt.savefig(f'{output_folder}/rx_fractions_plot.png', bbox_inches='tight')


# 1. Create the plot directory if it doesn't exist
output_folder = 'plots/20s'
createDirectory(output_folder)

# 2. Run through the simulations
plotResults()