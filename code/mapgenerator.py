import numpy as np
import random
from scipy.signal import convolve2d

def generate_caves(width, height, fill_prob=0.45, smooth_steps=3):
    cave = (np.random.random((height, width)) < fill_prob).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 0

    for _ in range(smooth_steps):
        neighbors = convolve2d(cave, kernel, mode="same", boundary="fill", fillvalue=1)
        new = ((cave == 1) & (neighbors >= 4)) | ((cave == 0) & (neighbors >= 5))
        cave = new.astype(np.uint8)
    
    return cave

def find_start_position(map_data):
    empty_cells = np.argwhere(map_data == 0)
    return tuple(random.choice(empty_cells))

def populate_elements(map_data, fill_ratio=0.8):
    empty_indices = np.argwhere(map_data == 0)
    num_to_fill = int(len(empty_indices) * fill_ratio)
    
    if len(empty_indices) > 0:
        chosen_indices = empty_indices[np.random.choice(len(empty_indices), num_to_fill, replace=False)]
        
        for y, x in chosen_indices:
            chance = random.random()
            
            if chance < 0.05:      #5 gem
                map_data[y, x] = 5
            elif chance < 0.10:    #5 energy
                map_data[y, x] = 3
            elif chance < 0.20:    #10 stone
                map_data[y, x] = 4
            elif chance < 0.22:    #2 trap
                map_data[y, x] = 6
            else:                  #78 ground
                map_data[y, x] = 2
                
    return map_data


#final fuction
def generate_full_map(width, height, cave_fill=0.35, cave_smooth=6, tunnel_steps=1500, maze_regions=1):
    world = generate_caves(width, height, cave_fill, cave_smooth)

    #save position
    start_y, start_x = find_start_position(world)

    #playing elements inside
    world = populate_elements(world, fill_ratio=0.8)

    return world, (start_x, start_y)

