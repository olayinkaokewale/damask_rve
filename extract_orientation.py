import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def extract_ori(simulation):
    grains = simulation[0]
    cell = simulation[1]
    simulation_base_path = '/nethome/o.okewale/examples/sim_results'
    filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
    input_file = f'{simulation_base_path}/{filename}/simulation/postProc/remesh_{filename}_tensionX_inc2000.txt'
    # /nethome/o.okewale/examples/sim_results/Polycrystal_10_14x14x14/2000_stand/CA_files
    output_base = f'{simulation_base_path}/{filename}/2000_stand/CA_files/0.0'
    createDirectory(output_base)
    output_file = f'{output_base}/..ang'

    orientations = []
    with open(input_file) as f:
        next(f)
        lines = f.readlines()
        orientations = [f'{line.split()[7]} {line.split()[8]} {line.split()[9]}' for line in lines]

    with open(output_file,'w') as fx:
        fx.writelines('\n'.join(orientations))

all_simulations = [
    [10,14,4],
    [98,30,4],
    [955,64,4]
]

for simu in all_simulations:
    extract_ori(simu)