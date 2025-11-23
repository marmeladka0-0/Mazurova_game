import pygame
from typing import Optional
from settings import *
from button import Button

class Menu:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.visible = True

        #background image
        self.background_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image, 
            (WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS)
        )

        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()

        btn_w, btn_h = 192, 64
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        # Buttons
        self.start_btn = Button(
            rect=(0, 0, btn_w, btn_h),
            image=button_image,
            callback=self._on_start
        )

        self.options_btn = Button(
            rect=(0, 0, btn_w, btn_h),
            image=button_image,
            callback=self._on_options
        )

        self.quit_btn = Button(
            rect=(0, 0, btn_w, btn_h),
            image=button_image,
            callback=self._on_quit
        )

        # Vertical placement
        spacing = 16
        total_h = btn_h * 3 + spacing * 2
        top = cy - total_h // 2

        self.start_btn.center_on(cx, top + btn_h // 2)
        self.options_btn.center_on(cx, top + btn_h + spacing + btn_h // 2)
        self.quit_btn.center_on(cx, top + (btn_h + spacing) * 2 + btn_h // 2)

        self._result: Optional[str] = None

        #render text
        self._font = pygame.font.SysFont(None, 32)

    #button callbacks
    def _on_start(self):
        self._result = "start"

    def _on_options(self):
        self._result = "options"

    def _on_quit(self):
        self._result = "quit"

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.visible:
            return None

        #buttons react to event
        for btn in (self.start_btn, self.options_btn, self.quit_btn):
            if btn.handle_event(event):
                result = self._result
                self._result = None
                return result

        return None

    def draw(self):
        if not self.visible:
            return

        #background
        self.surface.blit(self.background_image, (0, 0))

        #image-buttons
        self.start_btn.draw(self.surface)
        self.options_btn.draw(self.surface)
        self.quit_btn.draw(self.surface)

        #text over buttons
        self._draw_button_text(self.start_btn, "Start")
        self._draw_button_text(self.options_btn, "Options")
        self._draw_button_text(self.quit_btn, "Quit")

    def _draw_button_text(self, button: Button, text: str):
        surf = self._font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=button.rect.center)
        self.surface.blit(surf, rect)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


#finish menu
def show_game_over_screen(surface) -> str:

    pygame.event.clear()
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    surface.blit(overlay, (0, FRAME_THICKNESS))

    font = pygame.font.SysFont(None, 32)
    text = font.render("You are loser, please go fuck yourself", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50 - FRAME_THICKNESS))
    surface.blit(text, text_rect)

    #buttons
    button_font = pygame.font.SysFont(None, 36)
    buttons = {
        "restart": pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20 - FRAME_THICKNESS, 200, 50),
        "menu": pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 90 - FRAME_THICKNESS, 200, 50)
    }

    for name, rect in buttons.items():
        pygame.draw.rect(surface, (200, 200, 200), rect)
        text_btn = button_font.render(name.capitalize(), True, (0, 0, 0))
        text_rect_btn = text_btn.get_rect(center=rect.center)
        surface.blit(text_btn, text_rect_btn)
    pygame.display.update()

    #wait for event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                #my -= FRAME_THICKNESS
                for key, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return key

        pygame.time.delay(50)

