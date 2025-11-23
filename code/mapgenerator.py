import numpy as np
import random
from scipy.signal import convolve2d
from collections import deque

def generate_caves(width, height, fill_prob=0.45, smooth_steps=3):
    cave = (np.random.random((height, width)) < fill_prob).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 0

    for _ in range(smooth_steps):
        neighbors = convolve2d(cave, kernel, mode="same", boundary="fill", fillvalue=1)
        new = ((cave == 1) & (neighbors >= 4)) | ((cave == 0) & (neighbors >= 5))
        cave = new.astype(np.uint8)

    #cave = remove_lonely_walls(cave)
    return cave

def carve_tunnels(map_data, steps=3000):
    h, w = map_data.shape
    x, y = w // 2, h // 2
    for _ in range(steps):
        map_data[y, x] = 0
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x = max(1, min(w - 2, x + dx))
        y = max(1, min(h - 2, y + dy))
    return map_data

def generate_maze(width, height):
    maze = np.ones((height, width), dtype=np.uint8)
    stack = [(1, 1)]
    while stack:
        x, y = stack.pop()
        maze[y, x] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny, nx] == 1:
                maze[y + dy//2, x + dx//2] = 0
                stack.append((nx, ny))
    return maze

def remove_lonely_walls(cave):
    h, w = cave.shape
    new_cave = cave.copy()
    for y in range(1, h-1):
        for x in range(1, w-1):
            if cave[y, x] == 1:
                neighbors = cave[y-1:y+2, x-1:x+2]
                if np.sum(neighbors) <= 2:
                    new_cave[y, x] = 0
    return new_cave

def find_start_position(map_data):
    #h, w = map_data.shape
    empty_cells = np.argwhere(map_data == 0)
    return tuple(random.choice(empty_cells))#random empty cell

def populate_elements(map_data, fill_ratio=0.8, element_value_common=2, element_value_rare=3, rare_chance=0.02):
    empty_indices = np.argwhere(map_data == 0)
    num_to_fill = int(len(empty_indices) * fill_ratio)
    chosen_indices = empty_indices[np.random.choice(len(empty_indices), num_to_fill, replace=False)]
    for y, x in chosen_indices:
        if random.random() < rare_chance:
            map_data[y, x] = element_value_rare
        else:
            map_data[y, x] = element_value_common
    return map_data

def get_connected_regions(map_data):
    h, w = map_data.shape
    visited = np.zeros_like(map_data, dtype=bool)
    regions = []

    for y in range(h):
        for x in range(w):
            if map_data[y, x] == 0 and not visited[y, x]:
                region = []
                queue = deque()
                queue.append((y, x))
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
        y2, x2 = random.choice(main_region)
        for y in range(min(y1,y2), max(y1,y2)+1):
            map_data[y, x1] = 0
        for x in range(min(x1,x2), max(x1,x2)+1):
            map_data[y2, x] = 0

#final fuction
def generate_full_map(width, height, cave_fill=0.45, cave_smooth=5, tunnel_steps=1500, maze_regions=1):
    world = generate_caves(width, height, cave_fill, cave_smooth)
    world = carve_tunnels(world, tunnel_steps)

    for _ in range(maze_regions):
        mw, mh = 31, 31
        maze = generate_maze(mw, mh)
        x0 = random.randint(0, width - mw - 1)
        y0 = random.randint(0, height - mh - 1)
        world[y0:y0+mh, x0:x0+mw] = maze

    #main cave in center
    exit_x, exit_y = width // 2, height // 2
    world[exit_y-1:exit_y+2, exit_x-1:exit_x+2] = 0

    #save position
    start_y, start_x = find_start_position(world)

    #all in one
    regions = get_connected_regions(world)
    for region in regions:
        if (start_y, start_x) in region:
            main_region = region
            break
    connect_regions(world, main_region)

    #playing elements inside
    world = populate_elements(world, fill_ratio=0.8, element_value_common=2, element_value_rare=3, rare_chance=0.02)

    return world, (start_x, start_y), (exit_x, exit_y)

