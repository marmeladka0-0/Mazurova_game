import pygame
import random

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FRAME_THICKNESS

class LightManager:
    def __init__(self):
        self.dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
        self.base_radius = 180
        self.light_texture = self._create_gradient_texture(self.base_radius)

    def update(self):
        self.flicker_radius = self.base_radius + random.randint(-2, 2)
  
    def _create_gradient_texture(self, radius):
        surf = pygame.Surface((radius * 2, radius * 2))
        surf.fill((0, 0, 0))
        
        for i in range(radius, 0, -1):
            brightness = int(255 * (1 - (i / radius)**0.8))
            
            color = (brightness, brightness, int(brightness * 0.9))
            pygame.draw.circle(surf, color, (radius, radius), i)
        
        return surf

    def draw(self, screen, player):

        self.dark_surface.fill((20, 20, 25)) 
        
        screen_pos_x = player.world_x + 32 - player.tilemap.offset.x
        screen_pos_y = player.world_y + 32 - player.tilemap.offset.y
        
        light_rect = self.light_texture.get_rect(center=(screen_pos_x, screen_pos_y))
        self.dark_surface.blit(self.light_texture, light_rect, special_flags=pygame.BLEND_RGB_ADD)
        
        screen.blit(self.dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)