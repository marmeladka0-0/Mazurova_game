import pygame
from settings import *
import numpy as np
from menu import show_game_over_screen

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path: str = None, tilemap=None, start_pos=None):
        super().__init__()
        if image_path is None:
            self.resources_collected = 20
            return
            
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
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

    def update(self):
        self.world_x += (self.target_x - self.world_x) * self.speed * 0.05
        self.world_y += (self.target_y - self.world_y) * self.speed * 0.05

        self.rect.x = self.world_x - self.tilemap.offset.x
        self.rect.y = self.world_y - self.tilemap.offset.y

        #dead zone 
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
        self.current_depth_meters = max(0, current_y_index - self.initial_y_offset)

    def _is_walkable_at(self, x_pixel, y_pixel):
        map_data = self.tilemap.map_data
        tile_x = int(x_pixel // TILE_SIZE)
        tile_y = int((y_pixel - FRAME_THICKNESS) // TILE_SIZE)
        if 0 <= tile_y < map_data.shape[0] and 0 <= tile_x < map_data.shape[1]:
            return map_data[tile_y, tile_x] != 1
        return False

    def _dig_or_collect(self, x_pixel, y_pixel):
        tilemap = self.tilemap
        tile_x = int(x_pixel // TILE_SIZE)
        tile_y = int((y_pixel - FRAME_THICKNESS) // TILE_SIZE)

        if 0 <= tile_y < tilemap.map_data.shape[0] and 0 <= tile_x < tilemap.map_data.shape[1]:
            if tilemap.map_data[tile_y, tile_x]== 2:
                tilemap.map_data[tile_y, tile_x] = 0
                self.collect_resource(-1)
            elif tilemap.map_data[tile_y, tile_x] == 3:
                tilemap.map_data[tile_y, tile_x] = 0
                self.collect_resource(20)
                
            for tile in tilemap.tiles:
                if tile.rect.topleft == (tile_x * TILE_SIZE, tile_y * TILE_SIZE + FRAME_THICKNESS):
                    tile.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    break

    def handle_move_event(self, event):
        direction_x, direction_y = 0, 0
        if event.key == pygame.K_d: direction_x = 1
        elif event.key == pygame.K_a: direction_x = -1
        elif event.key == pygame.K_w: direction_y = -1
        elif event.key == pygame.K_s: direction_y = 1

        if direction_x != 0 or direction_y != 0:
            new_target_x = self.target_x + direction_x * self.tile_step
            new_target_y = self.target_y + direction_y * self.tile_step
            if self._is_walkable_at(new_target_x, new_target_y):
                self._dig_or_collect(new_target_x, new_target_y)
                self.target_x = new_target_x
                self.target_y = new_target_y

    def collect_resource(self, amount=-1):
        if amount < 0:
            self.resources_collected += amount
        else:
            self.resources_collected = amount
        #print(f"Зібрано {amount} ресурсів. Всього: {self.resources_collected}")


    def draw(self, surface):
        surface.blit(self.image, self.rect)
