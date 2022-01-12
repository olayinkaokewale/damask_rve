import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
from damask import Grid
from damask import seeds


dx = 4E-06    # grid spacing - 4 microns

d = 32E-06    # diameter of the grain - 32 microns

r = d/2.0

grain_vol = (4.0/3.0)*np.pi*(r**(1.0/3.0)) # vol of a grain - 4/3 * PI * cuberoot(r)
# grain_vol = 2*np.pi*(r) # circumference of a grain

print("Grain Volume =>", grain_vol)

cells_per_grain = grain_vol/dx    # need to keep this number constant
print("Cells per grain =>", round(cells_per_grain))

cells_per_grain_int = round(cells_per_grain)  # rounding it off

# cells for the geometry

number_of_grains = 50

total_cells_needed = number_of_grains*cells_per_grain_int

cells_x = round((total_cells_needed)**(1.0/3.0))

cells = np.array([cells_x,cells_x,cells_x])
size = cells*dx

print(size, cells)

# creating the actual geometry
seeds = seeds.from_random(size,number_of_grains,cells)
grid  = Grid.from_Voronoi_tessellation(cells,size,seeds,periodic=True)    #always make periodic
grid.save(f'rves/Polycrystal_{number_of_grains}_{cells[0]}x{cells[1]}x{cells[2]}')