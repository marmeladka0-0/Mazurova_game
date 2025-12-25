import pygame

from settings import *
from button import Button
from audio import audio_manager

class OptionsMenu:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.visible = False
        self.font = pygame.font.Font(FONT_PATH, 36)
        
        self.slider_width = 200
        self.music_vol = audio_manager.music_volume
        self.sound_vol = audio_manager.sound_volume
        
        self.music_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, self.slider_width, 10)
        self.sound_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 350, self.slider_width, 10)

        
        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        self.font = pygame.font.Font(FONT_PATH, 32)
        
        btn_w, btn_h = 192, 48
        self.back_btn = Button(
            rect=(WINDOW_WIDTH // 2 - btn_w // 2, 400, btn_w, btn_h), 
            image=button_image,
            callback=self._on_back
        )
        
        self._action = None

        self.handle_image = pygame.image.load(MUSIC_REG_IMAGE_PATH).convert_alpha()
        self.handle_image = pygame.transform.scale(self.handle_image, (16, 16))

        self.map_sizes = [
            {"label": "Small", "width": 150, "height": 100},
            {"label": "Medium", "width": 200, "height": 150},
            {"label": "Large", "width": 250, "height": 200}
        ]
        self.current_size_idx = 1
        
        self.map_selector_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 200, 200, 30)

    def _on_back(self):
        self._action = "back"

    def handle_event(self, event: pygame.event.Event):
        if not self.visible:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.map_selector_rect.collidepoint(event.pos):
                    self.current_size_idx = (self.current_size_idx + 1) % len(self.map_sizes)

        if pygame.mouse.get_pressed()[0]:
            m_pos = pygame.mouse.get_pos()
            
            if self.music_rect.inflate(0, 20).collidepoint(m_pos):
                rel_x = max(0, min(m_pos[0] - self.music_rect.x, self.slider_width))
                self.music_vol = rel_x / self.slider_width
                audio_manager.set_music_volume(self.music_vol)
            
            if self.sound_rect.inflate(0, 20).collidepoint(m_pos):
                rel_x = max(0, min(m_pos[0] - self.sound_rect.x, self.slider_width))
                self.sound_vol = rel_x / self.slider_width
                audio_manager.set_sounds_volume(self.sound_vol)

        if self.back_btn.handle_event(event):
            settings_data = {
                "action": "back",
                "map_w": self.map_sizes[self.current_size_idx]["width"],
                "map_h": self.map_sizes[self.current_size_idx]["height"],
                "music_volume": self.music_vol,
                "sound_volume": self.sound_vol
            }
            # print(settings_data)
            self._action = None
            return settings_data
            
        return None

    def draw(self):
        if not self.visible:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        self.surface.blit(overlay, (0, 0))

        self._draw_map_selector()
        self._draw_slider("Music", self.music_rect, self.music_vol)
        self._draw_slider("Sounds", self.sound_rect, self.sound_vol)

        title_surf = self.font.render("Settings", True, (221, 247, 244))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.surface.blit(title_surf, title_rect)

        self.back_btn.draw(self.surface)
        btn_font = pygame.font.Font(FONT_PATH, 32)
        text_surf = btn_font.render("Back", True, (221, 247, 244))
        text_rect = text_surf.get_rect(center=self.back_btn.rect.center)
        self.surface.blit(text_surf, text_rect)

    def _draw_slider(self, label, rect, value):

        slider_font = pygame.font.Font(FONT_PATH, 28)
        label_surf = slider_font.render(f"{label}: {int(value * 100)}%", True, (221, 247, 244))
        self.surface.blit(label_surf, (rect.x, rect.y - 25))
        
        pygame.draw.rect(self.surface, (100, 100, 100), rect, border_radius=5)
        
        circle_x = rect.x + int(value * self.slider_width)
        circle_y = rect.y + rect.h // 2
        
        handle_rect = self.handle_image.get_rect(center=(circle_x, circle_y))
        
        self.surface.blit(self.handle_image, handle_rect)

    def _draw_map_selector(self):
        selector_font = pygame.font.Font(FONT_PATH, 28)
        label_surf = selector_font.render("Map Size:", True, (221, 247, 244))
        self.surface.blit(label_surf, (self.map_selector_rect.x, self.map_selector_rect.y - 30))
        
        pygame.draw.rect(self.surface, (60, 60, 60), self.map_selector_rect, border_radius=5)
        
        size_label = self.map_sizes[self.current_size_idx]["label"]
        val_surf = selector_font.render(size_label, True, (221, 247, 244))
        val_rect = val_surf.get_rect(center=self.map_selector_rect.center)
        self.surface.blit(val_surf, val_rect)