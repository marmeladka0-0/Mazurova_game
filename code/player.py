import os
import pygame
import numpy as np

from settings import *
from audio import audio_manager

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path: str = None, tilemap=None, start_pos=None):
        super().__init__()
        if image_path is None:
            self.resources_collected = 20
            return
        # print(image_path)
        # print(PLAYER_IMAGE_PATH2)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (TILE_SIZE, TILE_SIZE))
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.tilemap = tilemap


        #start position
        if start_pos is None:
            free_cells = list(zip(*np.where(self.tilemap.map_data == 0)))
            start_pos = free_cells[0]  #1st free
        self.world_x = start_pos[1] * TILE_SIZE
        self.world_y = start_pos[0] * TILE_SIZE + FRAME_THICKNESS

        self.target_x = self.world_x
        self.target_y = self.world_y

        self.rect = self.image.get_rect(topleft=(self.world_x, self.world_y))
        self.tile_step = TILE_SIZE
        self.speed = 5

        self.resources_collected = 20
        self.current_depth_meters = 0
        self.initial_y_offset = 6
        
        
        if image_path == PLAYER_IMAGE_PATH2:
            self.idle_frames = self.load_animation('images/player2_idle')
            self.idle_order = [0, 1, 1,  1, 1, 2, 2, 2, 2, 1, 1, 0, 0, 0] 
            self.move_frames = self.load_animation('images/player2_move')
            self.move_order = [0]
            # print("Player skin 2 loaded")
        elif image_path == PLAYER_IMAGE_PATH3:
            self.idle_frames = self.load_animation('images/player3_idle')
            self.idle_order = [0, 1, 2, 1] 
            self.move_frames = self.load_animation('images/player3_move')
            self.move_order = [0]
            # print("Player skin 3 loaded")
        else:
            self.idle_frames = self.load_animation('images/player_idle')
            self.idle_order = [0, 1, 2, 1] 
            self.move_frames = self.load_animation('images/player_move')
            self.move_order = [0, 0, 1, 1, 0, 0] #1 2 1
            
        self.current_frame_index = 0
        self.animation_speed = 0.2 
        self.state = 'idle'
        
        if self.idle_frames:
            self.image = self.idle_frames[0]
        self.dir_x = -1

        self.gems_collected = 0
        self.is_dead = False
        self.death_timer = 0 
        self.death_delay = 20 

        self.blocks_dug_now = 0
        self.max_depth_reached = 0

    def load_animation(self, folder, /):
        frames = []

        for file_name in sorted(os.listdir(folder)):
            if file_name.endswith('.png'):
                path = os.path.join(folder, file_name)
                img = pygame.image.load(path).convert_alpha()
                
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                frames.append(img)
        return frames

    def update(self):
        self.world_x += (self.target_x - self.world_x) * self.speed * 0.03
        self.world_y += (self.target_y - self.world_y) * self.speed * 0.03

        self.animate()

        self.rect.x = self.world_x - self.tilemap.offset.x
        self.rect.y = self.world_y - self.tilemap.offset.y

        #not moving zone 
        screen_center_x = SCREEN_CENTER_X
        dead_zone_right = screen_center_x + DEAD_ZONE_WIDTH // 2
        dead_zone_left = screen_center_x - DEAD_ZONE_WIDTH // 2
        if self.rect.centerx > dead_zone_right:
            self.tilemap.offset.x += self.rect.centerx - dead_zone_right
        elif self.rect.centerx < dead_zone_left:
            self.tilemap.offset.x += self.rect.centerx - dead_zone_left

        screen_center_y = SCREEN_CENTER_Y
        dead_zone_bottom = screen_center_y + DEAD_ZONE_HEIGHT // 2
        dead_zone_top = screen_center_y - DEAD_ZONE_HEIGHT // 2
        if self.rect.centery > dead_zone_bottom:
            self.tilemap.offset.y += self.rect.centery - dead_zone_bottom
        elif self.rect.centery < dead_zone_top:
            self.tilemap.offset.y += self.rect.centery - dead_zone_top

        #current depth
        current_y_index = int((self.target_y - FRAME_THICKNESS) // TILE_SIZE)
        self.current_depth_meters = int(max(0, current_y_index - self.initial_y_offset))
        self.max_depth_reached = max(self.max_depth_reached, self.current_depth_meters)

        if self.is_dead:

            self.death_timer += 1

            if (self.death_timer // 5) % 2 == 0:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
                
            if self.death_timer > self.death_delay:
                return "game_over"
            return None
        
    def _is_walkable_at(self, x_pixel, y_pixel):
        map_data = self.tilemap.map_data
        tile_x = int(x_pixel // TILE_SIZE)
        tile_y = int((y_pixel - FRAME_THICKNESS) // TILE_SIZE)
        if 0 <= tile_y < map_data.shape[0] and 0 <= tile_x < map_data.shape[1]:
            return map_data[tile_y, tile_x] != 1 and map_data[tile_y, tile_x] != 4
        return False

    def _dig_or_collect(self, x_pixel, y_pixel):
        tilemap = self.tilemap
        tile_x = int(x_pixel // TILE_SIZE)
        tile_y = int((y_pixel - FRAME_THICKNESS) // TILE_SIZE)

        if 0 <= tile_y < tilemap.map_data.shape[0] and 0 <= tile_x < tilemap.map_data.shape[1]:
            tile_value = tilemap.map_data[tile_y, tile_x]
            
            if tile_value == 2: 
                tilemap.map_data[tile_y, tile_x] = 0
                self.collect_resource(amount=-1)
                self.blocks_dug_now += 1
            elif tile_value == 3: 
                tilemap.map_data[tile_y, tile_x] = 0
                self.collect_resource(amount=20)
            elif tile_value == 5: 
                tilemap.map_data[tile_y, tile_x] = 0
                self.collect_gem(amount=1) 
            elif tile_value == 6: 
                audio_manager.play_sound('bump')
                self.is_dead = True
                return
            elif tile_value == 4:
                return

            for tile in tilemap.tiles:
                if tile.rect.topleft == (tile_x * TILE_SIZE, tile_y * TILE_SIZE + FRAME_THICKNESS):
                    tile.kill()
                    break

    def handle_move_event(self, event):
        if abs(self.target_x - self.world_x) > 20 or abs(self.target_y - self.world_y) > 20:
            return

        direction_x, direction_y = 0, 0
        if event.key == pygame.K_d: direction_x = 1
        elif event.key == pygame.K_a: direction_x = -1
        elif event.key == pygame.K_w: direction_y = -1
        elif event.key == pygame.K_s: direction_y = 1
        if direction_x != 0:
            self.dir_x = direction_x

        if direction_x != 0 or direction_y != 0:
            new_target_x = self.target_x + direction_x * self.tile_step
            new_target_y = self.target_y + direction_y * self.tile_step

            if self._is_walkable_at(new_target_x, new_target_y):
                self._dig_or_collect(new_target_x, new_target_y)
                self.target_x = new_target_x
                self.target_y = new_target_y

            elif direction_x != 0:
                tile_x = int(new_target_x // TILE_SIZE)
                tile_y = int((new_target_y - FRAME_THICKNESS) // TILE_SIZE)
                
                #stone push
                if 0 <= tile_y < self.tilemap.map_data.shape[0] and self.tilemap.map_data[tile_y, tile_x] == 4:
                    if self.tilemap.try_push_stone(tile_x, tile_y, direction_x):
                        self.target_x = new_target_x
                        
        
        if direction_x != 0:
            if direction_x < 0:
                self.image = self.original_image
            else:
                self.image = self.flipped_image

    def collect_resource(self, *, amount=-1):
        if amount < 1:
            self.resources_collected += amount
        else:
            audio_manager.play_sound('jump')
            self.resources_collected = amount

    def collect_gem(self, amount=1):
        self.gems_collected += amount

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def animate(self):

        is_moving = abs(self.target_x - self.world_x) > 1 or abs(self.target_y - self.world_y) > 1
        
        new_state = 'move' if is_moving else 'idle'
        if new_state != self.state:
            self.state = new_state
            self.current_frame_index = 0
        
        if self.state == 'move':
            current_frames_list = self.move_frames
            current_order = self.move_order
        else:
            current_frames_list = self.idle_frames
            current_order = self.idle_order

        if current_frames_list:
            self.current_frame_index += self.animation_speed
            if self.current_frame_index >= len(current_order):
                self.current_frame_index = 0
                
            frame_idx = current_order[int(self.current_frame_index)]
            temp_image = current_frames_list[frame_idx]
            
            if self.dir_x == 1:
                self.image = pygame.transform.flip(temp_image, True, False)
            else:
                self.image = temp_image

