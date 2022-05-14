import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def extract_ori(simulation, sim_no=1, tension_file='tensionX'):
    grains = simulation[0]
    cell = simulation[1]
    stand = simulation[3]
    simulation_base_path = f'/nethome/o.okewale/examples/{simulation[2]}e-06_3.2e-05/sim_results_{sim_no}'
    filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
    input_file = f'{simulation_base_path}/{filename}/simulation/postProc/remesh_{filename}_{tension_file}_inc{stand}.txt'
    # /nethome/o.okewale/examples/sim_results/Polycrystal_10_14x14x14/2000_stand/CA_files
    output_base = f'{simulation_base_path}/{filename}/{stand}_stand/CA_files/0.0'
    createDirectory(output_base)
    output_file = f'{output_base}/..ang'
    rho_output_file = f'{output_base}/._rho.txt'

    orientations = []
    rho = []
    with open(input_file) as f:
        next(f)
        lines = f.readlines()
        orientations = [f'{line.split()[7]} {line.split()[8]} {line.split()[9]}' for line in lines]
        rho = [f'{line.split()[5]}' for line in lines]

    with open(output_file,'w') as fx:
        fx.writelines('\n'.join(orientations))
    
    with open(rho_output_file,'w') as rfx:
        rfx.writelines('\n'.join(rho))

all_simulations = [
    [10,7,8,6000],
    [98,15,8,6000],
    [955,32,8,6000],
    [2160,42,8,6000],
    [512,26,8,6000]
]

all_simulations_2 = [
    [10,14,4,6000],
    [98,30,4,6000],
    [310,44,4,6000]
]

tension_file = 'tensionX'
# for simu in all_simulations_2:
#     extract_ori(simu, simulation_base_path)
extract_ori([200,18,8,6000], tension_file=tension_file)
# for i in range(1,4):
#     simulation_base_path = f'/nethome/o.okewale/examples/4e-06_3.2e-05/sim_results_{i}'
#     extract_ori([955,32,8,6000], sim_no=i)