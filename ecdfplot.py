import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sb
import math

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def ecdf(xdata):
    xdataecdf = np.sort(xdata)
    ydataecdf = np.arange(1, len(xdata) + 1) / len(xdata)
    return xdataecdf,ydataecdf

def plotECDF(data):
    sample_name = f'Polycrystal_{data[0]}_{data[1]}x{data[1]}x{data[1]}'
    simulation_folder = f'/nethome/o.okewale/examples/sim_results_1/{sample_name}/{data[2]}_stand/CA_files'
    output_folder = f'./plots/ECDF'
    createDirectory(output_folder)

    sel_seconds = ['0.0','2.5','5.0']
    plt.figure()
    for sec in sel_seconds:
        input_file = f'{simulation_folder}/{sec}/._rho.txt'
        x_values = []
        with open(input_file) as f:
            lines = f.readlines()
            x_values = [float(line) for line in lines]
        
        # import seaborn as sns
        # sns.ecdfplot(x=x_values)
        x,y = ecdf(x_values)
        #Plot the data
        # plt.figure()
        plt.plot(x, y) # , marker='.', linestyle='none'
        plt.xlabel('Dislocation density $\\rho$')
        plt.ylabel('ECDF')
        plt.margins(0.1)
        plt.title(f"{sample_name} - ECDF dislocation density plot")
        plt.legend([f'{s}s' for s in sel_seconds], title="Annealing time")
        plt.savefig(f'{output_folder}/{sample_name}_ECDF_dislocation_density_plot.png', bbox_inches='tight')

# ==
def plotECDFByTime(simulations, time, output_folder, label_index=0, label_title="", label_suffix=""):

    plt.figure()
    for _id,data in enumerate(simulations):
        sample_name = f'Polycrystal_{data[0]}_{data[1]}x{data[1]}x{data[1]}'
        simulation_folder = f'/nethome/o.okewale/examples/{data[3]}e-06_3.2e-05/sim_results_1/{sample_name}/{data[2]}_stand/CA_files'
        input_file = f'{simulation_folder}/{time}/._rho.txt'
        x_values = []
        with open(input_file) as f:
            lines = f.readlines()
            x_values = [float(line) for line in lines]
        
        # sb.ecdfplot(x_values, log_scale=10)
        # # plt.xscale('log')
        # plt.margins(0.1)
        # plt.savefig(f'{output_folder}/{time}s_{label_title}_ECDF_dislocation_density_plot.png', bbox_inches='tight')
        
        x,y = ecdf(x_values)
        #Plot the data
        line_width = 0.75 * (_id + 1)
        gradient = np.linspace(0,1,len(simulations))
        colors = plt.cm.rainbow(gradient)
        plt.plot(np.log(x), y, linestyle='--', linewidth=line_width, color=colors[_id]) # , marker='.', linestyle='none'
        # plt.xlabel('$log_{10}(\\rho)$')
        plt.xlabel('Dislocation density, $\\rho$ (log-scale)')
        # plt.xscale('log', base=10)
        plt.ylabel('ECDF')
        plt.margins(0.1)
        # plt.title(f"{sample_name} - ECDF dislocation density plot")
        plt.legend([f'{s[label_index]} {label_suffix}' for s in simulations], title=label_title)
        plt.savefig(f'{output_folder}/{time}s_{label_title}_ECDF_dislocation_density_plot.png', bbox_inches='tight')


def getCASimulationFolder(data):
    sample_name = f'Polycrystal_{data[0]}_{data[1]}x{data[1]}x{data[1]}'
    simulation_folder = f'/nethome/o.okewale/examples/sim_results_1/{sample_name}/{data[2]}_stand/CA_files'
    return simulation_folder


def getRho(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        x_values = [float(line) for line in lines]
    return x_values


def doKSTest(data1, data2, time='0.0'):
    x_val1 = getRho(f'{getCASimulationFolder(data1)}/{time}/._rho.txt')
    x_val2 = getRho(f'{getCASimulationFolder(data2)}/{time}/._rho.txt')
    result = stats.ks_2samp(x_val1,x_val2)
    return result


def plotKSTest(allData, time_array):
    # This function assumes the last value is the one being compared to.
    output_folder = f'./plots/KSTest'
    createDirectory(output_folder)
    for time in time_array:
        x_data = [f'{allData[i][0]}' for i in range(0,len(allData)-1)]
        y_data = [doKSTest(allData[len(allData)-1], allData[s], time)[1] for s in range(0,len(allData)-1)]
        # print(x_data)
        # print(y_data)
        plt.figure()
        plt.plot(x_data, y_data, marker='.', linestyle='-') # , marker='.', linestyle='none'
        # plt.legend(['avg','5.0s','0.0s'], title='Annealing time')
        plt.margins(0.1)
        plt.title(f"{time}s - dislocation density KS Test plot")
        plt.xlabel('grain no.')
        plt.ylabel('p-value')
        plt.savefig(f'{output_folder}/{time}s_KSTest_on_dislocation_density.png', bbox_inches='tight')
    


size_simulations = [
    [10,7,6000,8],
    [98,15,6000,8],
    [310,22,6000,8],
    [512,26,6000,8],
    [955,32,6000,8],
    [2160,42,6000,8],
]
res_simulations = [
    [310,22,6000,8],
    [310,29,6000,6],
    [310,44,6000,4],
    [310,58,6000,3],
]
# #One time plot
# data = [310,22,6000]
# plotECDF(data)
# for data in all_simulations:
#     plotECDF(data)

# Plot based on time
output_folder = f'./plots/ECDF'
createDirectory(output_folder)
sel_seconds = ['0.0','2.5','5.0']
for sec in sel_seconds:
    plotECDFByTime(res_simulations, sec, output_folder, label_index=3, label_title="RVE grid spacing", label_suffix='$\\mu m$')
    plotECDFByTime(size_simulations, sec, output_folder, label_index=0, label_title="RVE size", label_suffix='grains')

# times=[round(g,1) for g in np.arange(0.0,5.1,1.0)]
# plotKSTest(all_simulations,time_array=times)