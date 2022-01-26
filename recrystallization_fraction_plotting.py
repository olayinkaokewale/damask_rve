import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
import matplotlib.pyplot as plt
import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)



# 0. Set the array mapping 'grain numbers' to 'cells'
all_simulations = [
[
    [20,14,5],
    [20,18,4],
    [20,24,3]
],
[
    [40,18,5],
    [40,22,4],
    [40,30,3]
],
[
    [60,20,5],
    [60,26,4],
    [60,34,3]
],
[
    [20,14,5],
    [40,18,5],
    [60,20,5]
],
[
    [20,18,4],
    [40,22,4],
    [60,26,4]
],
[
    [20,24,3],
    [40,30,3],
    [60,34,3]
],
[
    [20,70,1],
    [20,36,2],
    [20,18,4],
    [20,9,8]
],
[
    [10,14,4],
    [98,30,4],
    [955,64,4]
]
]



def plotResults(simulations):
    simulation_base_path = '/nethome/o.okewale/examples/sim_results'
    markers = [".","o","*","v","p",">","d","+","x","s"]
    label_prefix = ""
    is_same_grains = False
    if (simulations[0][0] == simulations[1][0] == simulations[2][0]):
        label_prefix = f'{simulations[0][0]} grains: '
        is_same_grains = True
    else:
        label_prefix = f'{simulations[0][2]} $\mu$m grid spacing: '

    plt_datas = []

    out_file_name_prefix = ''
    for index,simulation in enumerate(simulations):
        grains = simulation[0]
        cell = simulation[1]
        dx_spacing = simulation[2]

        out_file_name_prefix = f'{out_file_name_prefix}{grains}-{cell}_'

        filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        input_file = f'{simulation_base_path}/{filename}/2000_stand/CA_files/5.0/.fractions.txt'

        if not is_same_grains:
            legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]'
        else:
            legend_label = f'{dx_spacing} $\mu$m'

        plt_data = {
            'time': [],
            'fraction': [],
            'label': legend_label,
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
    plt.title(f"{label_prefix}RX fraction - time plot")
    plt.savefig(f'{output_folder}/{out_file_name_prefix}rx_fractions_plot.png', bbox_inches='tight')


# 1. Create the plot directory if it doesn't exist
output_folder = 'plots'
createDirectory(output_folder)

# # 2. Run through the simulations
# for simul in all_simulations:
#     plotResults(simul)

#2b. Run just one
plotResults(all_simulations[len(all_simulations)-1])