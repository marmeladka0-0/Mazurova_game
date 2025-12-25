import pygame

from settings import *
from button import Button

class StatsMenu:
    def __init__(self, surface: pygame.Surface):

        self.surface = surface
        self.visible = False
        self.font = pygame.font.Font(FONT_PATH, 28)
        self.title_font = pygame.font.Font(FONT_PATH, 42)
        
        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        btn_w, btn_h = 160, 40
        self.back_btn = Button(
            rect=(WINDOW_WIDTH // 2 - btn_w // 2, WINDOW_HEIGHT - 80, btn_w, btn_h),
            image=pygame.transform.scale(button_image, (btn_w, btn_h)),
            callback=self.hide
        )

    def draw(self, stats_data):

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        self.surface.blit(overlay, (0, 0))

        title_surf = self.title_font.render("STATISTICS", True, (221, 247, 244))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.surface.blit(title_surf, title_rect)

        display_info = [
            ("Nickname", stats_data.get("nickname", "Player")),
            ("Gems", stats_data.get("gems", 0)),
            ("Blocks dug", stats_data.get("blocks_dug", 0)),
            ("Max depth", f"{stats_data.get('max_depth', 0)} m"),
            ("Traps destroyed", stats_data.get("traps_count", 0))
        ]

        start_y = 150
        spacing = 45
        
        for i, (label, value) in enumerate(display_info):

            label_surf = self.font.render(label, True, (221, 247, 244))
            self.surface.blit(label_surf, (WINDOW_WIDTH // 2 - 180, start_y + i * spacing))
            
            val_surf = self.font.render(str(value), True, (221, 247, 244))
            val_rect = val_surf.get_rect(midright=(WINDOW_WIDTH // 2 + 180, start_y + i * spacing + 15))
            self.surface.blit(val_surf, val_rect)
            
            line_y = start_y + i * spacing + 35
            pygame.draw.line(self.surface, (40, 60, 50), (WINDOW_WIDTH // 2 - 180, line_y), (WINDOW_WIDTH // 2 + 180, line_y), 1)

        self.back_btn.draw(self.surface)
        back_text = self.font.render("Back", True, (221, 247, 244))
        self.surface.blit(back_text, (self.back_btn.rect.centerx - back_text.get_width() // 2, self.back_btn.rect.centery - 12))

    def show(self): self.visible = True
    def hide(self): self.visible = False

    def handle_event(self, event):
        if self.back_btn.handle_event(event):
            return "back"
        return None