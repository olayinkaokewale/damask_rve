import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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
    


all_simulations = [
    [10,7,6000],
    [98,15,6000],
    [512,26,6000],
    [955,32,6000],
    [2160,42,6000],
]
# #One time plot
data = [310,22,6000]
plotECDF(data)
# for data in all_simulations:
#     plotECDF(data)

# times=[round(g,1) for g in np.arange(0.0,5.1,1.0)]
# plotKSTest(all_simulations,time_array=times)