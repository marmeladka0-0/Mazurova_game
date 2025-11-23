# data_panel.py

import pygame
from settings import *

class DataPanel:
    def __init__(self, font_size=24):

        try:
            self.font = pygame.font.SysFont('Arial', font_size, bold=True)
        except pygame.error:
            self.font = pygame.font.Font(None, font_size)

        #position
        self.x_position = 10
        self.y_position = FRAME_THICKNESS + 10 

    def draw(self, surface, player):
        
        #resources
        res_text = f"Ресурси: {player.resources_collected}"
        res_surf = self.font.render(res_text, True, 'white')
        
        #depth
        depth_text = f"Глибина: {player.current_depth_meters} м"
        depth_surf = self.font.render(depth_text, True, 'white')
        
        #visualisation
        surface.blit(res_surf, (self.x_position, self.y_position))
        surface.blit(depth_surf, (self.x_position, self.y_position + res_surf.get_height() + 5))