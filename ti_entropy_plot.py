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

def plotData(input_path, output_path, graph_title=""):
    grain, texture_index, entropy = getData(input_path)
    # ======================================== 
    # print(grain)
    # print(texture_index)
    # print(entropy)
    # ========================================
    plt.figure()
    plt.plot(grain, texture_index, marker='.') # , marker='.', linestyle='none'
    # plt.ylabel('Texture Index')
    plt.plot(grain, entropy, marker='.') # , marker='.', linestyle='none'
    # plt.ylabel('Entropy')
    plt.legend(['Texture index','Entropy'])
    plt.xlabel('Grain numbers')
    # plt.margins(0.1)
    plt.title(graph_title)
    plt.savefig(output_path, bbox_inches='tight')

output_folder = './plots/texture_index'
createDirectory(output_folder)
suffix = 'texture_index_entropy'
# input_files = ['4micron_0.0','4micron_5.0','8micron_0.0','8micron_5.0']
# input_files = ['8micron_2160_diff_0.0', '8micron_2160_diff_5.0']
input_files = ['4micron-8micron_0.0', '4micron-8micron_5.0']

for x in input_files:
    plotData(f'data/{x}_{suffix}.data', f'{output_folder}/{x}_{suffix}_plot.png', f'{x} TI & Entropy plot')