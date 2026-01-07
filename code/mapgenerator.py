import numpy as np
import random
from scipy.signal import convolve2d
from collections import deque
# deque - двобічна черга

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


#--------------------------------------------------------------------------------------------------------

def generate_caves_for_old_version(width, height, fill_prob=0.45, smooth_steps=3):
    cave = (np.random.random((height, width)) < fill_prob).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 0

    for _ in range(smooth_steps):
        neighbors = convolve2d(cave, kernel, mode="same", boundary="fill", fillvalue=1)
        new = ((cave == 1) & (neighbors >= 4)) | ((cave == 0) & (neighbors >= 5))
        cave = new.astype(np.uint8)
    return cave

# Random Walk випадкове блукання
def carve_tunnels(map_data, steps=3000):
    h, w = map_data.shape
    x, y = w // 2, h // 2
    for _ in range(steps):
        map_data[y, x] = 0
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x = max(1, min(w - 2, x + dx))
        y = max(1, min(h - 2, y + dy))
    return map_data

# BFS пошук у ширину
def get_connected_regions(map_data):
    h, w = map_data.shape
    visited = np.zeros_like(map_data, dtype=bool)
    regions = []

    for y in range(h):
        for x in range(w):
            if map_data[y, x] == 0 and not visited[y, x]:
                region = []
                queue = deque([(y, x)])
                visited[y, x] = True
                while queue:
                    cy, cx = queue.popleft()
                    region.append((cy, cx))
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ny, nx = cy+dy, cx+dx
                        if 0<=ny<h and 0<=nx<w and map_data[ny,nx]==0 and not visited[ny,nx]:
                            visited[ny,nx] = True
                            queue.append((ny,nx))
                regions.append(region)
    return regions


def connect_regions(map_data, main_region):
    regions = get_connected_regions(map_data)
    other_regions = [r for r in regions if r != main_region]
    for region in other_regions:
        y1, x1 = random.choice(region)
        y2, x2 = main_region[0]
        for y in range(min(y1,y2), max(y1,y2)+1): map_data[y, x1] = 0
        for x in range(min(x1,x2), max(x1,x2)+1): map_data[y2, x] = 0

def populate_elements_for_old_version(map_data, fill_ratio=0.8):
    empty_indices = np.argwhere(map_data == 0)
    num_to_fill = int(len(empty_indices) * fill_ratio)
    
    if len(empty_indices) > 0:
        chosen_indices = empty_indices[np.random.choice(len(empty_indices), min(num_to_fill, len(empty_indices)), replace=False)]
        
        for y, x in chosen_indices:
            chance = random.random()
            if chance < 0.03:    
                map_data[y, x] = 5
            elif chance < 0.08:  
                map_data[y, x] = 3
            elif chance < 0.15:  
                map_data[y, x] = 4
            elif chance < 0.18:  
                map_data[y, x] = 6
            else:                
                map_data[y, x] = 2
    return map_data

def generate_full_map_old_version(width=206, height=156, cave_fill=0.45, cave_smooth=5):
    world = generate_caves_for_old_version(width, height, cave_fill, cave_smooth)
    world = carve_tunnels(world, steps=2000)

    cx, cy = width // 2, height // 2
    world[cy-2:cy+3, cx-2:cx+3] = 0
    # діапазон від до - можно через цикл було

    regions = get_connected_regions(world)
    if regions:
        main_region = min(regions, key=lambda r: (r[0][0]-cy)**2 + (r[0][1]-cx)**2)
        connect_regions(world, main_region)

    world = populate_elements_for_old_version(world, fill_ratio=0.7)

    return world



