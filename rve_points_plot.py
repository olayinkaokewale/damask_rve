import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as matcoll
from scipy import stats

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def plotData(data, output_path):
    legends = [f'{x} $\\mu m$' for x in data.keys()]
    plt.figure()
    for _id,key in enumerate(data.keys()):
        line_width = 1 * _id+1
        # x_values = [f'{x[0]}' for x in data.get(key)]
        x_values = [x[0] for x in data.get(key)]
        # y_values = [(y[1]**3)/1e5 for y in data.get(key)]
        y_values = [(y[1]**3) for y in data.get(key)]
        plt.plot(x_values, y_values, linestyle='--', linewidth=line_width) # , marker='.', linestyle='none'

    # plt.ylabel('Grid points ($\\times 10^{5}$)')
    plt.ylabel('Grid points')
    plt.legend(legends, title="Grid spacing")
    plt.xlabel('Grain numbers')
    plt.xscale('log')
    plt.yscale('log')
    plt.margins(0.1)
    plt.savefig(output_path, bbox_inches='tight')

data = {
    "8": [
        [10,7],
        [98,15],
        [310,22],
        [512,26],
        [955,32],
        [2160,42],
    ],
    "6": [
        [10,9],
        [98,19],
        [310,29],
        [512,34],
        [955,42],
        [2160,55],
    ],
    "4": [
        [10,14],
        [98,30],
        [310,44],
        [512,52],
        [955,64],
        [2160,84],
    ],
    "3": [
        [10,18],
        [98,39],
        [310,58],
        [512,69],
        [955,85],
        [2160,111],
    ]
}

output_base = 'plots/rve_point_plots'
createDirectory(output_base)
plotData(data, f'{output_base}/plot2_xylog.png')