import pygame

from settings import *
from button import Button

class DataPanel:
    def __init__(self, font_size=24):

        #text 
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.x_position = 10
        self.y_position = FRAME_THICKNESS + 10 

        #pause button
        pause_btn_size = 40
        pause_x = WINDOW_WIDTH - pause_btn_size - 10
        pause_y = FRAME_THICKNESS + 10
        pause_icon = pygame.image.load(PAUSE_ICON_PATH).convert_alpha()
        pause_icon = pygame.transform.scale(pause_icon, (pause_btn_size, pause_btn_size))
        
        self.pause_button = Button(
            rect=(pause_x, pause_y, pause_btn_size, pause_btn_size),
            image=pause_icon,
            callback=self._on_pause
        )
        
        self._pause_triggered = False

    def _on_pause(self):
        self._pause_triggered = True

    def handle_event(self, event):
        if self.pause_button.handle_event(event):
            res = self._pause_triggered
            self._pause_triggered = False
            return "pause" if res else None
        return None

    def draw(self, surface, player):

        res_text = f"Energy: {player.resources_collected}"
        res_surf = self.font.render(res_text, True, (221, 247, 244))
        
        depth_text = f"Depth: {player.current_depth_meters} м"
        depth_surf = self.font.render(depth_text, True, (221, 247, 244))

        gems_text = f"Gems: {player.gems_collected} м"
        gems_surf = self.font.render(gems_text, True, (221, 247, 244))
        
        surface.blit(res_surf, (self.x_position, self.y_position))
        surface.blit(depth_surf, (self.x_position, self.y_position + res_surf.get_height() + 5))
        surface.blit(gems_surf, (self.x_position, self.y_position + res_surf.get_height() + 5 + depth_surf.get_height() + 5))
        
        self.pause_button.draw(surface)