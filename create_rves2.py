import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
# print(sys.path)
import os
import damask
import numpy

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def createRVE(cell:int, grains:int, path:str='rves/'):
    size = numpy.ones(3)*1e-5
    cells = [cell,cell,cell]
    N_grains = grains
    

    # Create the first RVE with grain
    seeds = damask.seeds.from_random(size, N_grains, cells)
    grid = damask.Grid.from_Voronoi_tessellation(cells,size,seeds)
    grid.material = grid.material + 1
    grid.save(f'{path}Polycrystal_{N_grains}_{cells[0]}x{cells[1]}x{cells[2]}')
    

path = f'rves/method4/'
createDirectory(path)

for no_of_grains in range(20,61,20):
    createRVE(20,no_of_grains,path)