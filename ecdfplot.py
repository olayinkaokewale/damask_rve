import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def ecdf(xdata):
    xdataecdf = np.sort(xdata)
    ydataecdf = np.arange(1, len(xdata) + 1) / len(xdata)
    return xdataecdf,ydataecdf

def plotECDF(data):
    sample_name = f'Polycrystal_{data[0]}_{data[1]}x{data[1]}x{data[1]}'
    simulation_folder = f'/nethome/o.okewale/examples/sim_results/{sample_name}/{data[2]}_stand/CA_files'
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

all_simulations = [
    [10,7,6000],
    [98,15,6000],
    [512,26,6000],
    [955,32,6000],
    [2160,42,6000],
]
# #One time plot
# data = [98,15,6000]
# plotECDF(data)
for data in all_simulations:
    plotECDF(data)