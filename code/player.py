import pygame
from settings import *
from tilemap import TileMap

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, tilemap):
        super().__init__()
        
        self.image = pygame.image.load(image_path).convert_alpha()
        new_size = (TILE_SIZE, TILE_SIZE)
        self.image = pygame.transform.scale(self.image, new_size)
        self.tilemap = tilemap

        self.rect = self.image.get_frect(topleft = (0, 0 + FRAME_THICKNESS))
        
        self.tile_step = TILE_SIZE

    def update(self):
        pass

    def _is_walkable_at(self, x_pixel, y_pixel):
        
        map_data = getattr(self.tilemap, 'map_data', None)
        if not map_data:
            return False

        # Convert to tile indices
        tile_x = int(x_pixel // TILE_SIZE)
        tile_y = int((y_pixel - FRAME_THICKNESS) // TILE_SIZE)

        if tile_y < 0 or tile_x < 0:
            return False

        if tile_y >= len(map_data) or tile_x >= len(map_data[0]):
            return False
        return map_data[tile_y][tile_x] == 0
        
    #Movement handler
    def handle_move_event(self, event):

        direction_x, direction_y = 0, 0
        
        #Key presses
        if event.key == pygame.K_d:
            direction_x = 1
        elif event.key == pygame.K_a:
            direction_x = -1
        elif event.key == pygame.K_w:
            direction_y = -1
        elif event.key == pygame.K_s:
            direction_y = 1
        
        if direction_x != 0 or direction_y != 0:
            
            new_x = self.rect.x + direction_x * self.tile_step
            new_y = self.rect.y + direction_y * self.tile_step
            
            #Check borders
            
            max_x = WINDOW_WIDTH - self.tile_step
            max_y = WINDOW_HEIGHT + FRAME_THICKNESS - self.tile_step
            
            is_within_bounds = (
                new_x >= 0 and new_x <= max_x and
                new_y >= 0 and new_y <= max_y
            )
            
            #Check inside borders
            can_step = self._is_walkable_at(new_x, new_y)

            #Move player only if inside bounds and target tile is walkable
            if is_within_bounds and can_step:
                self.rect.topleft = (new_x, new_y)

    def draw(self, surface):
        #Draw player
        surface.blit(self.image, self.rect)
