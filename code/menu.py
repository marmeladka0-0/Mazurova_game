import pygame
from typing import Optional
from settings import *
from button import Button
from frame import *

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
    button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
    # затемнение фона
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 32)
    title_surf = font.render("Game Over", True, (255, 0, 0))
    title_rect = title_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))
    surface.blit(title_surf, title_rect)

    # создаём кнопки через класс Button
    button_font = pygame.font.SysFont(None, 36)
    btn_w, btn_h = 192, 64
    cx = WINDOW_WIDTH // 2

    restart_btn = Button(
        rect=(cx - btn_w//2, WINDOW_HEIGHT//2 - btn_h//2, btn_w, btn_h),
        image=button_image,
        callback=lambda: setattr(show_game_over_screen, "_choice", "restart")
    )

    menu_btn = Button(
        rect=(cx - btn_w//2, WINDOW_HEIGHT//2 + 70, btn_w, btn_h),
        image=button_image,
        callback=lambda: setattr(show_game_over_screen, "_choice", "menu")
    )

    # текст на кнопках
    def draw_button_text(btn, text):
        surf = button_font.render(text, True, (0, 0, 0))
        rect = surf.get_rect(center=btn.rect.center)
        surface.blit(surf, rect)

    show_game_over_screen._choice = None

    # главный цикл ожидания
    clock = pygame.time.Clock()
    while show_game_over_screen._choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if check_frame_events(event):
                return "quit"
            
            restart_btn.handle_event(event)
            menu_btn.handle_event(event)

        # перерисовываем экран
        surface.blit(overlay, (0, 0))
        surface.blit(title_surf, title_rect)
        restart_btn.draw(surface)
        menu_btn.draw(surface)
        draw_button_text(restart_btn, "Restart")
        draw_button_text(menu_btn, "Menu")
        draw_styled_frame(surface)
        draw_close_button(surface)
        pygame.display.update()
        clock.tick(30)

    return show_game_over_screen._choice

