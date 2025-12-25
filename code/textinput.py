import pygame
import os
import json

from settings import *

class TextInput:
    def __init__(self, x, y, width, height, font_path, font_size, default_name="Player"):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font_path, font_size)
        self.filename = "./data/settings.txt"
        
        if not os.path.exists("./data"):
            os.makedirs("./data")

        self.game_data = self.load_all_data(default_name)
        self.text = self.game_data["nickname"]
        self.active = False 

        try:
            bg_path = os.path.join('images', 'nickname_back_1.png')
            self.bg_image = pygame.image.load(bg_path).convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image, (width, height))
            self.bg_active_alpha = 100 
            self.bg_passive_alpha = 40  
        except pygame.error:
            self.bg_image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.bg_image.fill((255, 255, 255, 40))

    def load_all_data(self, default_name = "Player"):
        default_data = {
            "nickname": default_name,
            "gems": 999,
            "map_w": 100,
            "map_h": 80,
            "blocks_dug": 0,
            "max_depth": 0,
            "traps_destroyed": 0,
            "music_volume": 0.5,
            "sound_volume": 0.5,
            "skins": 3,
            "selected_skin": 0
        }
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    default_data.update(loaded)
                    return default_data
            except:
                return default_data
        return default_data

    def save_game_data(self, **params):

        self.game_data["nickname"] = self.text
        self.game_data.update(params)
        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.game_data, f, ensure_ascii=False, indent=4)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                if self.active:
                    self.active = False
                    self.save_game_data()

        if self.active and event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_RETURN:
            #     self.active = False
            #     self.save_game_data()
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 10 and event.unicode.isprintable():
                    self.text += event.unicode

    def draw(self, surface):
        alpha = self.bg_active_alpha if self.active else self.bg_passive_alpha
        self.bg_image.set_alpha(alpha)
        surface.blit(self.bg_image, self.rect.topleft)

        text_surf = self.font.render(self.text, True, (221, 247, 244))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_rect = pygame.Rect(text_rect.right + 2, text_rect.y, 2, text_rect.height)
            pygame.draw.rect(surface, (255, 255, 255), cursor_rect)