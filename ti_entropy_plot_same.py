import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as matcoll
from scipy import stats

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def getData(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        x_values = [[float(d) for d in line.split(", ")] for line in lines]
    grain = [f'{int(r[0])}' for r in x_values]
    texture_index = [r[1] for r in x_values]
    entropy = [r[2] for r in x_values]
    return grain, texture_index, entropy

def plotData(input_paths):
    grains = []
    texture_indexes = []
    entropies = []
    legends = []
    for input_path in input_paths:
        grain, texture_index, entropy = getData(f'data/{input_path}.data')
        grains.append(grain)
        texture_indexes.append(texture_index)
        entropies.append(entropy)
        legends.append(f'{input_path.split(":")[0]}s')
    # ======================================== 
    # print(grain)
    # print(texture_index)
    # print(entropy)
    # ========================================
    y_labels = ["Texture Index", "Entropy"]
    y_lims = [[-0.2,5.2],[-0.05,0.85]]
    y_values = [texture_indexes, entropies]
    for i,label in enumerate(y_labels):
        plt.figure()
        for x,ti  in enumerate(y_values[i]):
            plt.plot(grains[x], ti, marker='.') # , marker='.', linestyle='none'
        plt.ylabel(label)
        plt.legend(legends, title="Annealling time")
        plt.xlabel('Grid spacing ($\mu m$)')
        plt.ylim(bottom=y_lims[i][0],top=y_lims[i][1])
        # plt.margins(0.1)
        # plt.title(graph_title)
        output = f'{output_folder}/{input_paths[0].split(":")[-1]}_{label}_plot.png'
        plt.savefig(output, bbox_inches='tight')

output_folder = './plots/texture_index'
createDirectory(output_folder)
suffix = 'texture_index_entropy'
# input_files = ['4micron_0.0','4micron_5.0','8micron_0.0','8micron_5.0']
# input_files = ['0.0:8micron_2160_diff', '5.0:8micron_2160_diff']
input_files = ['0.0:310 grains (3micron-others)_ti_entropy', '5.0:310 grains (3micron-others)_ti_entropy']
# input_files = ['4micron-8micron_0.0', '4micron-8micron_5.0']
# input_files = ['310 grains 5.0 (3micron-others)', '310 grains']

plotData(input_files)