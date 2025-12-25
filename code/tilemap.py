import pygame
from settings import *
from mapgenerator import generate_full_map
import numpy as np

#generated_map, start_pos, exit_pos = generate_full_map(200, 150)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, type_value):
        super().__init__()
        #original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type_value   # 1, 2, 3

class TileMap:
    def __init__(self):
        generated_map, start_pos, exit_pos = generate_full_map(200, 150)
        self.map_data = self.expand_map_with_border(generated_map)
        self.tiles = self._create_tilemap()
        self.offset = pygame.Vector2(0, 0)

        self.start_pos = start_pos 
        self.exit_pos = exit_pos

    def _create_tilemap(self):
        tile_group = pygame.sprite.Group()

        #dict
        tile_images = {
            1: TILE_IMAGE_PATH,
            2: DIRT_IMAGE_PATH,
            3: BLUE_SPHERE_PATH
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

    def save_map_to_file(self, filename="map_data.txt", delimiter=' ', header_info=None):

        if header_info is None:

            h, w = self.map_data.shape
            header = (f"Map Size (H x W): {h} x {w}\n"
                      f"Start Position (original index): {self.start_pos}\n"
                      f"Exit Position (original index): {self.exit_pos}\n"
                      f"--- Map Data Below ---")
        else:
            header = header_info
            
        try:
            np.savetxt(
                filename, 
                self.map_data, 
                fmt='%d',       #format int
                delimiter=delimiter,
                header=header,  
                comments='# '
            )
            print(f"Saved map: {filename}")
        except Exception as e:
            print(f"Exeption when downloading map: {e}")

    def apply_gravity(self, player):
        """
        Гравитация падает только для блоков 3 (BLUE_SPHERE) внутри зоны видимости игрока
        """
        h, w = self.map_data.shape
        changed = False

        # Вычисляем границы зоны видимости в тайлах
        buffer_tiles = 3  # чтобы блоки сразу за границей экрана тоже падали
        start_x = max(0, int((player.rect.left + self.offset.x) // TILE_SIZE) - buffer_tiles)
        end_x   = min(w, int((player.rect.right + self.offset.x) // TILE_SIZE) + buffer_tiles)
        start_y = max(0, int((player.rect.top + self.offset.y) // TILE_SIZE) - buffer_tiles)
        end_y   = min(h, int((player.rect.bottom + self.offset.y) // TILE_SIZE) + buffer_tiles)

        # Проходим снизу вверх по зоне видимости
        for y in range(end_y-2, start_y-1, -1):
            for x in range(start_x, end_x):
                tile = self.map_data[y, x]
                if tile == 3 and self.map_data[y + 1, x] == 0:
                    # Блок падает
                    self.map_data[y + 1, x] = tile
                    self.map_data[y, x] = 0
                    changed = True

        if changed:
            self.tiles = self._create_tilemap()
