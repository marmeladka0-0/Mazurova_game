import pygame
import numpy as np

from settings import *
from mapgenerator import generate_full_map, find_start_position
from audio import audio_manager

#generated_map, start_pos, exit_pos = generate_full_map(200, 150)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, type_value):
        super().__init__()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type_value   # 1, 2, 3, 5, 6

class TileMap:
    def __init__(self, width = 200, height = 150, map_data=None):
        # print(width, height)
        if map_data is not None:
            self.map_data = self.expand_map_with_border(map_data)
            start_pos = find_start_position(self.map_data)
        else:
            generated_map, start_pos = generate_full_map(width, height)
            self.map_data = self.expand_map_with_border(generated_map)
        self.settle_map()
        self.tiles = self._create_tilemap()
        self.offset = pygame.Vector2(0, 0)

        self.start_pos = start_pos 
        self.fall_delay = 200
        self.last_fall_time = pygame.time.get_ticks()
        self.falling_stones = set()


    def _create_tilemap(self):
        tile_group = pygame.sprite.Group()

        #dict
        tile_images = {
            1: TILE_IMAGE_PATH,
            2: DIRT_IMAGE_PATH,
            3: BLUE_SPHERE_PATH,
            4: STONE_ROCK_PATH,
            5: GEM_IMAGE_PATH,
            6: TRAP_IMAGE_PATH
        }

        loaded_images = {k: pygame.transform.scale(pygame.image.load(v).convert_alpha(),
                                                (TILE_SIZE, TILE_SIZE))
                        for k, v in tile_images.items()}

        for y_index, row in enumerate(self.map_data):
            for x_index, tile_value in enumerate(row):
                if tile_value in loaded_images:
                    x = x_index * TILE_SIZE
                    y = y_index * TILE_SIZE + FRAME_THICKNESS

                    tile = Tile((x, y), loaded_images[tile_value], tile_value)
                    tile_group.add(tile)
        return tile_group

    def draw(self, surface):
        for tile in self.tiles:
            offset_rect = tile.rect.copy()
            offset_rect.topleft -= self.offset
            surface.blit(tile.image, offset_rect)

    def expand_map_with_border(self, map_data, border_size=3):
        h, w = map_data.shape
        bordered_map = np.ones((h + 2*border_size, w + 2*border_size), dtype=np.uint8)
        bordered_map[border_size:border_size+h, border_size:border_size+w] = map_data
        return bordered_map
    
    def partition_draw(self, surface):
        screen_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        buffer = 2

        for tile in self.tiles:
            offset_rect = tile.rect.copy()
            offset_rect.topleft -= self.offset

            extended_rect = screen_rect.inflate(buffer * TILE_SIZE * 2, buffer * TILE_SIZE * 2)

            if extended_rect.colliderect(offset_rect):
                surface.blit(tile.image, offset_rect)

    def save_map_to_file(self, filename="./data/map_data.txt", header_info=None):
        if header_info is None:
            h, w = self.map_data.shape
            header = (f"Map Size (H x W): {h} x {w}")
        else:
            header = header_info
                
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {header}\n")
                
                for row in self.map_data:
                    visual_row = ""
                    for cell in row:
                        if cell == 1:
                            visual_row += "1"
                        else:
                            visual_row += " "
                    
                    f.write(visual_row + "\n")
                    
        except Exception as e:
            print(e)

    def save_full_map_to_file(self, filename="./data/from_game.txt", header_info=None):
        if header_info is None:
            h, w = self.map_data.shape
            header = (f"Map Size (H x W): {h} x {w}")
        else:
            header = header_info
                
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {header}\n")
                
                for row in self.map_data:
                    visual_row = "".join(map(str, row))
                    
                    f.write(visual_row + "\n")
                    
        except Exception as e:
            print(e)


    def apply_gravity(self, player):

        traps_broken_this_tick = 0
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time < self.fall_delay:
            return False, traps_broken_this_tick

        self.last_fall_time = current_time

        h, w = self.map_data.shape
        changed = False

        next_falling_stones = set()

        player_tile_x = (player.target_x) // TILE_SIZE
        player_tile_y = (player.target_y - FRAME_THICKNESS) // TILE_SIZE

        falling_types = [3, 4, 5]

        for y in range(h - 2, -1, -1):
            for x in range(w):
                tile_type = self.map_data[y, x]
                
                if tile_type in falling_types:
                    is_empty_below = (self.map_data[y + 1, x] == 0)
                    target_type = self.map_data[y + 1, x]
                    is_player_below = (x == player_tile_x and (y + 1) == player_tile_y)

                    if target_type == 6 and tile_type in [3, 4, 5]:
                        self.map_data[y + 1, x] = 0
                        count_radius = 5 
                        dist_x = abs(x - player_tile_x)
                        dist_y = abs((y + 1) - player_tile_y)
                        
                        if dist_x <= count_radius and dist_y <= count_radius:
                            traps_broken_this_tick += 1

                        for tile in self.tiles:
                            t_x = tile.rect.x // TILE_SIZE
                            t_y = (tile.rect.y - FRAME_THICKNESS) // TILE_SIZE
                            if t_x == x and t_y == y + 1:
                                tile.kill()
                                break
                        changed = True

                    if is_player_below:
                        if (x, y) in self.falling_stones:
                            if tile_type in [4]:
                                audio_manager.play_sound('bump')
                                player.is_dead = True

                    if is_empty_below and not is_player_below:
                        self.map_data[y + 1, x] = tile_type
                        self.map_data[y, x] = 0
                        changed = True

                        next_falling_stones.add((x, y + 1))
                        
                        for tile in self.tiles:
                            tile_x = tile.rect.x // TILE_SIZE
                            tile_y = (tile.rect.y - FRAME_THICKNESS) // TILE_SIZE
                            if tile_x == x and tile_y == y:
                                tile.rect.y += TILE_SIZE
                                break 

        self.falling_stones = next_falling_stones                       
        return changed, traps_broken_this_tick
    
    def settle_map(self):
        h, w = self.map_data.shape
        falling_types = [3, 4, 5]

        map_settled = False
        while not map_settled:
            changed_this_step = False
            for y in range(h - 2, -1, -1):
                for x in range(w):
                    tile_type = self.map_data[y, x]
                    if tile_type in falling_types:
                        if self.map_data[y + 1, x] == 0:
                            self.map_data[y + 1, x] = tile_type
                            self.map_data[y, x] = 0
                            changed_this_step = True
            
            if not changed_this_step:
                map_settled = True

    def try_push_stone(self, stone_x, stone_y, direction_x):

        target_x = stone_x + direction_x
        
        if 0 <= target_x < self.map_data.shape[1]:
            if self.map_data[stone_y, target_x] == 0:
                tile_type = self.map_data[stone_y, stone_x]
                self.map_data[stone_y, target_x] = tile_type
                self.map_data[stone_y, stone_x] = 0
                
                for tile in self.tiles:
                    t_x = tile.rect.x // TILE_SIZE
                    t_y = (tile.rect.y - FRAME_THICKNESS) // TILE_SIZE
                    if t_x == stone_x and t_y == stone_y:
                        tile.rect.x += direction_x * TILE_SIZE
                        break
                return True
        return False