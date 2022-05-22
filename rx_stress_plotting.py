import sys
from turtle import color
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import damask
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
],
[
    [955,32,8],
    [955,64,4]
],
[
    [955,32,8,4900],
    [512,26,8,5100],
    [98,15,8,6000],
    [10,7,8,5900]
],
[
    [10,7,8,6000],
    [98,15,8,6000],
    [512,26,8,6000],
    [955,32,8,6000],
    [2160,42,8,6000]
],
[
    [2160,42,8,6000],
    [955,32,8,6000],
    [512,26,8,6000],
    [98,15,8,6000],
    [10,7,8,6000]
],
[
    [310,44,4,6000],
    [310,22,8,6000],
],
[
    [10,7,8,3000]
],
[
    [10,7,8,6000],
    [98,15,8,6000],
    [310,22,8,6000],
    [512,26,8,6000],
    [955,32,8,6000],
    [2160,42,8,6000]
],
[
    [98,15,8,6000],
    [98,30,4,6000],
    [98,60,2,6000]
],
[
    [310,22,8,6000,'tensionX'],
    [310,29,6,6000,'tensionX'],
    [310,44,4,6000,'tensionX'],
    [310,58,3,6000,'tensionX2',4000]
],
[
    [310,22,8,6000],
    [310,29,6,6000],
    [310,44,4,6000],
    [310,58,3,6000,'tensionX2',4000],
],
[
    [310,44,4,6000],
    [98,30,4,6000],
    [10,14,4,6000]
],
[
    [10,7,8,6000],
    [98,15,8,6000],
    [310,22,8,6000],
    [512,26,8,6000],
    [955,32,8,6000],
    [2160,42,8,6000]
],
[
    [310,22,8,6000],
    [310,29,6,6000],
    [310,44,4,6000],
    [310,58,3,6000,'tensionX2',4000],
],
]

def checkSameSimulations(simulations):
    prev_number = 0
    for simu in simulations:
        if prev_number == 0:
            prev_number = simu[0]
        else:
            if (prev_number != simu[0]):
                return False
    return True

def checkSameResolution(simulations):
    prev_number = 0
    for simu in simulations:
        if prev_number == 0:
            prev_number = simu[2]
        else:
            if (prev_number != simu[2]):
                return False
    return True

# print(checkSameSimulations(all_simulations[6]))

def plotRXTimeResults(simulations, cmap='viridis', cmap_adjust=0):
    markers = [".","o","*","v","p",">","d","+","x","s"]
    label_prefix = ""
    is_same_grains = False
    is_same_resolutions = checkSameResolution(simulations)
    if (checkSameSimulations(simulations)):
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
        stand_number = 2000 if len(simulation) < 4 else simulation[3]

        out_file_name_prefix = f'{out_file_name_prefix}{grains}-{cell}_'

        simulation_base_path = f'/nethome/o.okewale/examples/{dx_spacing}e-06_3.2e-05/sim_results_1'
        filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        input_file = f'{simulation_base_path}/{filename}/{stand_number}_stand/CA_files/5.0/.fractions.txt'

        # if not is_same_grains:
        #     legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]'
        # else:
        #     legend_label = f'{dx_spacing} $\mu$m'
        
        legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]' if (not is_same_grains) else f'{dx_spacing} $\mu$m'

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
        
    gradient = np.linspace(0,1,len(plt_datas)+cmap_adjust)
    colors = plt.cm.get_cmap(cmap)(gradient)
    plt.figure()
    for _id,data in enumerate(plt_datas):
        if is_same_grains and is_same_resolutions:
            plt.plot(data['time'], data['fraction'], linestyle='-', label=data['label'], marker=data['markers'])
        else:
            line_width = 1 * _id+1
            line_styles = ['-','-', '-.', '-.', '--', '--']
            plt.plot(data['time'], data['fraction'], linestyle=line_styles[-1], color=colors[_id], label=data['label'], linewidth=line_width)
    plt.xlabel('$t_a$ (s)')
    plt.ylabel('$X$')
    plt.legend(loc='lower right')
    # plt.title(f"{label_prefix}RX fraction - time plot")
    plt.savefig(f'{output_folder}/{out_file_name_prefix}rx_fractions_plot.png', bbox_inches='tight')


def plotStressStrainResults(simulations, cmap='viridis', cmap_adjust=0):
    markers = [".","o","*","v","p",">","d","+","x","s"]
    label_prefix = ""
    is_same_grains = False
    is_same_resolutions = checkSameResolution(simulations)
    if (checkSameSimulations(simulations)):
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
        fname_suffix = simulation[4] if len(simulation)>4 else 'tensionX'
        regrid_N = simulation[5] if len(simulation)==6 else None

        simulation_base_path = f'/nethome/o.okewale/examples/{dx_spacing}e-06_3.2e-05/sim_results_1'
        out_file_name_prefix = f'{out_file_name_prefix}{grains}-{cell}_'
        file_name = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        
        if not is_same_grains:
            legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]'
        else:
            legend_label = f'{dx_spacing} $\mu$m'

        plt_data = {
            'stress': [],
            'strain': [],
            'incs': [],
            'label': legend_label,
            'markers': markers[index]
        }

        input_file = f'{simulation_base_path}/{file_name}/simulation/{file_name}_{fname_suffix}.hdf5'

        d = damask.Result(input_file)
        ds_sigma = d.get_dataset_location('sigma_vM')
        ds_epsilon = d.get_dataset_location('epsilon_V^0.0(F)_vM')

        if (len(ds_sigma) == 0):
            d.add_stress_Cauchy()
            d.add_equivalent_Mises('sigma')
        
        if (len(ds_epsilon) == 0):
            d.add_strain()
            d.add_equivalent_Mises('epsilon_V^0.0(F)')
                    
        f = h5py.File(d.fname)
                    
        for path in d.get_dataset_location('sigma_vM'):
            # plt_data['incs'].append(path.split('/')[0])
            plt_data['stress'].append(np.average(f[path])/1e6)
        # for path in d.get_dataset_location('epsilon_V^0.0(F)_vM'):
        #     plt_data['strain'].append(np.average(f[path]))
        lastStrain = 0
        for path in d.get_dataset_location('epsilon_V^0.0(F)_vM'):
            plt_data['strain'].append(lastStrain + np.average(f[path]))
            inc = path.split('/')[0]
            if (regrid_N is not None and inc == f'inc{regrid_N}'):
                lastStrain = np.average(f[path])
        
        # plt_data['stress'] = [np.average(s) for s in d.get('sigma_vM').values()]
        # plt_data['strain'] = [np.average(e) for e in d.get('epsilon_V^0.0(F)_vM').values()]
        
        plt_datas.append(plt_data)

    plt.figure()
    gradient = np.linspace(0,1,len(plt_datas)+cmap_adjust)
    colors = plt.cm.get_cmap(cmap)(gradient)
    for _id,data in enumerate(plt_datas):
        if is_same_grains and is_same_resolutions:
            plt.plot(data['strain'], data['stress'], linestyle='-', label=data['label'], marker=data['markers'])
        else:
            line_width = 1 * _id+1
            cl = colors[_id]
            plt.plot(data['strain'], data['stress'], linestyle='--', color=cl, label=data['label'], linewidth=line_width)
    plt.ylabel('$\sigma$ (MPa)')
    plt.xlabel('$\epsilon$')
    plt.legend(loc='lower right')
    # plt.title(f"{label_prefix}stress-strain plot")
    plt.savefig(f'{output_folder}/{out_file_name_prefix}stress_strain_plot.png', bbox_inches='tight')


# 1. Create the plot directory if it doesn't exist
output_folder = 'plots/results/cm'
createDirectory(output_folder)

# # 2. Run through the simulations
# for simul in all_simulations:
#     plotRXTimeResults(simul)
#     plotStressStrainResults(simul)

# # 2b. Run just one
# # RVE resolution plot
# plotRXTimeResults(all_simulations[-1],cmap_adjust=2)
# plotStressStrainResults(all_simulations[-1],cmap_adjust=2)
# RVE size plot
plotRXTimeResults(all_simulations[-2],cmap='magma',cmap_adjust=4)
plotStressStrainResults(all_simulations[-2],cmap='magma',cmap_adjust=4)


# # Tests =======================================
# sx = all_simulations[len(all_simulations)-1][2]
# sr = sx[4] if len(sx)>4 else None
# print(sr)