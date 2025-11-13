import pygame
from settings import *
from os.path import join

LEVEL_MAP_NUMBERS = [
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
]


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image_path):
        super().__init__()
        
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (TILE_SIZE, TILE_SIZE))
        
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass

class TileMap:
    def __init__(self):
        self.map_data = LEVEL_MAP_NUMBERS 
        self.tiles = self._create_tilemap()

    def _create_tilemap(self):
        tile_group = pygame.sprite.Group() 
        
        for y_index, row in enumerate(self.map_data):
            for x_index, tile_value in enumerate(row):
                
                if tile_value == 1:
                    x = x_index * TILE_SIZE
                    y = y_index * TILE_SIZE + FRAME_THICKNESS
                    
                    tile = Tile((x, y), TILE_IMAGE_PATH) 
                    tile_group.add(tile)
                    
        return tile_group

    def draw(self, surface):
        self.tiles.draw(surface)