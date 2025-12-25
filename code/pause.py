import pygame

from settings import *
from button import Button

class PauseMenu:
    def __init__(self, surface):
        self.surface = surface
        self.visible = False
        
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))
        
        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        btn_w, btn_h = 192, 48
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT  // 2 + FRAME_THICKNESS
        
        self.font = pygame.font.Font(FONT_PATH, 32)
        
        self.resume_btn = Button(
            rect=(0, 0, btn_w, btn_h),
            image=button_image,
            callback=self._on_resume
        )
        self.menu_btn = Button(
            rect=(0, 0, btn_w, btn_h),
            image=button_image,
            callback=self._on_menu
        )
        
        self.resume_btn.center_on(cx, cy - 32)
        self.menu_btn.center_on(cx, cy + 32)
        
        self._result = None

    def _on_resume(self): self._result = "resume"
    def _on_menu(self): self._result = "menu"

    def handle_event(self, event):
        if not self.visible: return None
        
        if self.resume_btn.handle_event(event):
            res = self._result
            self._result = None
            return res
        if self.menu_btn.handle_event(event):
            res = self._result
            self._result = None
            return res
        return None

    def draw(self):
        if not self.visible: return
        
        self.surface.blit(self.overlay, (0, 0))
        
        title_surf = self.font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.surface.blit(title_surf, title_rect)
        
        self.resume_btn.draw(self.surface)
        self.menu_btn.draw(self.surface)
        
        self._draw_text("Resume", self.resume_btn)
        self._draw_text("Menu", self.menu_btn)

    def _draw_text(self, text, button):
        text_surf = self.font.render(text, True, (255, 255, 255))
        rect = text_surf.get_rect(center=button.rect.center)
        self.surface.blit(text_surf, rect)