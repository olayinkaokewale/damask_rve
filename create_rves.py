import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
# print(sys.path)
import os
import damask
import numpy

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def createRVE(start:int, grains:int, path:str='rves/'):
    size = numpy.ones(3)*1e-5
    cells = [pow(2,start),pow(2,start),pow(2,start)]
    N_grains = grains
    

    # Create the first RVE with grain
    seeds = damask.seeds.from_random(size, N_grains, cells)
    grid = damask.Grid.from_Voronoi_tessellation(cells,size,seeds)
    grid.material = grid.material + 1
    grid.save(f'{path}Polycrystal_{N_grains}_{cells[0]}x{cells[1]}x{cells[2]}')

    # Rescale the previously created grid
    for x in range(start-1,3,-1):
        new_cells = [pow(2,x), pow(2,x), pow(2,x)]
        output_file = f'{path}Polycrystal_{N_grains}_{new_cells[0]}x{new_cells[1]}x{new_cells[2]}'
        scaled = grid.scale(new_cells)
        scaled.save(output_file)


# loop through range of grains and increment by 20
for y in range(20,200,20):
    path = f'rves/{y}_grains/'
    createDirectory(path)
    createRVE(5,y,path)