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

def ecdf(xdata, min_rho=0):
    xdataecdf = np.sort(xdata)
    ydataecdf = np.arange(1, len(xdata) + 1) / len(xdata)
    if min_rho == 0:
        return xdataecdf,ydataecdf
    newX = []
    newY = []
    for _i,x in enumerate(xdataecdf):
        if x > min_rho:
            newX.append(x)
            newY.append(ydataecdf[_i])
    return newX,newY
    

def getRho(input_file, min_value=0):
    with open(input_file) as f:
        lines = f.readlines()
        x_values = [float(line) for line in lines if float(line) > min_value]
    return x_values

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
def getDistinctLabels(all_data, _id=0):
    distinct_data = []
    for x in all_data:
        if x[_id] not in distinct_data:
            distinct_data.append(x[_id])
    return distinct_data

def plotECDFByTime(simulations, time, output_folder, label_index=0, label_title="", label_suffix="", min_rho=0, xlim=None, pre_ecdf=False, cmap='rainbow',cmap_adjust=0):

    plt.figure()
    # distinct_data = getDistinctLabels(all_data=simulations, _id=label_index)
    for _id,data in enumerate(simulations):
        # Set up lines and colors
        line_width = 1 * (_id + 1)
        gradient = np.linspace(0,1,len(simulations)+cmap_adjust)
        colors = plt.cm.get_cmap(cmap)(gradient)

        start = data[4] if len(data) > 4 else 1
        end = data[5] if len(data) > 5 else 1
        line = None
        x_val = []
        fill_x = []
        fill_y = []
        # fig,subplt = plt.subplots()
        for _cid in range(start,end+1):
            new_data = [data[0],data[1],data[2],data[3],_cid]
            input_file = f'{getCASimulationFolder(new_data)}/{time}/._rho.txt'
            if pre_ecdf:
                x_values = getRho(input_file, min_value=min_rho)
                x,y = ecdf(x_values)
            else:
                x_values = getRho(input_file)
                x,y = ecdf(x_values,min_rho=min_rho)
            fill_x.append(x)
            fill_y.append(y)
            x_val = x
            #Plot the data
            # line, = plt.plot(x, y, linestyle='--', linewidth=line_width, color=colors[_id]) # , marker='.', linestyle='none'
        xmean = []
        ymean = []
        # ystd = []
        if (len(fill_x) > 1 and len(fill_y) > 1):
            for _ix,_ in enumerate(fill_y[0]):
                x_m = np.mean([fill_x[_i][_ix] for _i in range(start-1,end)])
                y_m = np.mean([fill_y[_i][_ix] for _i in range(start-1,end)])
                # y_s = np.std([fill_y[_i][_ix] for _i in range(start-1,end)])
                ymean.append(y_m)
                xmean.append(x_m)
                # ystd.append(y_s)
        else:
            ymean = fill_y[0]
            xmean = fill_x[0]
        # print(len(ymean), len(xmean))
        # return
        # if line:
        xmean = np.array(xmean)
        ymean = np.array(ymean)
        # ystd = np.array(ystd)
        line, = plt.plot(x_val, ymean, linestyle='--', linewidth=line_width, color=colors[_id]) # , marker='.', linestyle='none'
        # yhigh = np.max(fill_y)
        # print(len(fill_x), len(fill_y[0]), len(fill_y[1]))
        # plt.fill_between(x=x_val, y1=ymean - ystd, y2=ymean + ystd, color=colors[_id], alpha=0.2)
        line.set_label(f'{data[label_index]} {label_suffix}')

    plt.legend(title=label_title)
    plt.xlabel('Dislocation density, $\\rho$ (log-scale)')
    if xlim and len(xlim) == 2:
        plt.xlim(left=xlim[0],right=xlim[1])
    plt.xscale('log', base=10)
    plt.ylabel('ECDF')
    plt.margins(0.1)
    # plt.title(f"{sample_name} - ECDF dislocation density plot")
    
    min_rho_label = f'_{min_rho}' if min_rho > 0 else ""
    plt.savefig(f'{output_folder}/{time}s_{label_title}{min_rho_label}_ECDF_dislocation_density_plot.png', bbox_inches='tight')


def plotECDFByTime_v2(simulations, time, output_folder, label_index=0, label_title="", label_suffix="", min_rho=0, xlim=None, pre_ecdf=False):

    plt.figure()
    # distinct_data = getDistinctLabels(all_data=simulations, _id=label_index)
    for _id,data in enumerate(simulations):
        # Set up lines and colors
        line_width = 0.75 * (_id + 1)
        gradient = np.linspace(0,1,len(simulations))
        colors = plt.cm.rainbow(gradient)

        start = data[4] if len(data) > 4 else 1
        end = data[5] if len(data) > 5 else 1
        line = None
        fill_x = []
        # fig,subplt = plt.subplots()
        for _cid in range(start,end+1):
            new_data = [data[0],data[1],data[2],data[3],_cid]
            input_file = f'{getCASimulationFolder(new_data)}/{time}/._rho.txt'
            x_values = getRho(input_file, min_value=min_rho) if pre_ecdf else getRho(input_file)
            fill_x.append(x_values)
            
        xmean = []
        for _ix,_ in enumerate(fill_x[0]):
            x_m = np.mean([fill_x[_i][_ix] for _i in range(start-1,end)])
            xmean.append(x_m)
        
        x,y = ecdf(xmean) if pre_ecdf else ecdf(xmean,min_rho=min_rho)
        line, = plt.plot(x, y, linestyle='--', linewidth=line_width, color=colors[_id]) # , marker='.', linestyle='none'
        # yhigh = np.max(fill_y)
        # print(len(fill_x), len(fill_y[0]), len(fill_y[1]))
        # plt.fill_between(x=fill_x, y1=ymean + ystd, y2=ymean - ystd, color=colors[_id], alpha=0.2)
        line.set_label(f'{data[label_index]} {label_suffix}')

    plt.legend(title=label_title)
    plt.xlabel('Dislocation density, $\\rho$ (log-scale)')
    if xlim and len(xlim) == 2:
        plt.xlim(left=xlim[0],right=xlim[1])
    plt.xscale('log', base=10)
    plt.ylabel('ECDF')
    plt.margins(0.1)
    # plt.title(f"{sample_name} - ECDF dislocation density plot")
    
    min_rho_label = f'_{min_rho}' if min_rho > 0 else ""
    plt.savefig(f'{output_folder}/{time}s_{label_title}{min_rho_label}_ECDF_dislocation_density_plot.png', bbox_inches='tight')


def getCASimulationFolder(data):
    sample_name = f'Polycrystal_{data[0]}_{data[1]}x{data[1]}x{data[1]}'
    simulation_no = data[4] if len(data)>4 else 1
    simulation_folder = f'/nethome/o.okewale/examples/{data[3]}e-06_3.2e-05/sim_results_{simulation_no}/{sample_name}/{data[2]}_stand/CA_files'
    return simulation_folder


# def getRho(input_file, min=0):
#     with open(input_file) as f:
#         lines = f.readlines()
#         x_values = [float(line) for line in lines if line > min]
#     return x_values


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
    

size_simulations_minrho = [
    [10,7,6000,8],
    [98,15,6000,8],
    [310,22,6000,8],
    [512,26,6000,8],
    [955,32,6000,8],
    [2160,42,6000,8],
]

size_simulations = [
    [10,7,6000,8,1,5],
    [98,15,6000,8,1,5],
    [310,22,6000,8,1,5],
    [512,26,6000,8,1,3],
    [955,32,6000,8,1,3],
    [2160,42,6000,8,1,1],
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
output_folder = f'./plots/ECDF_8'
createDirectory(output_folder)
sel_seconds = ['5.0','2.5','0.0']
# min_rho = 0
min_rho = 1.21e13
# xlim = None
xlim = [0.8e13,3e15]
for sec in sel_seconds:
    # plotECDFByTime(res_simulations, sec, output_folder, label_index=3, label_title="RVE grid spacing", label_suffix='$\\mu m$', xlim=xlim, cmap='viridis',cmap_adjust=2)
    # plotECDFByTime(res_simulations, sec, output_folder, label_index=3, label_title="RVE grid spacing", label_suffix='$\\mu m$', min_rho=min_rho, xlim=xlim, cmap='viridis',cmap_adjust=2)
    plotECDFByTime(size_simulations, sec, output_folder, label_index=0, label_title="RVE size", label_suffix='grains', xlim=xlim, pre_ecdf=True, cmap='magma', cmap_adjust=4)
    plotECDFByTime(size_simulations_minrho, sec, output_folder, label_index=0, label_title="RVE size", label_suffix='grains',  min_rho=min_rho, xlim=xlim, pre_ecdf=True, cmap='magma', cmap_adjust=4)

# times=[round(g,1) for g in np.arange(0.0,5.1,1.0)]
# plotKSTest(all_simulations,time_array=times)