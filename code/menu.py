import pygame

from typing import Optional
from settings import *
from button import Button
from frame import *
from textinput import TextInput 

class Menu:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.visible = True

        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image, 
            (WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS)
        )

        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        stats_icon_image = pygame.image.load(STAT_IMAGE_PATH).convert_alpha()

        btn_w, btn_h = 192, 48
        icon_size = 32
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        self.start_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_start)
        self.levels_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_levels)
        self.shop_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_shop)
        # self.results_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_levels)
        self.options_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_options)
        self.quit_btn = Button(rect=(0, 0, btn_w, btn_h), image=button_image, callback=self._on_quit)

        self.buttons = [
            self.start_btn, self.shop_btn, 
            self.levels_btn, self.options_btn, self.quit_btn
        ]
        
        spacing = 12
        total_h = (btn_h * len(self.buttons)) + (spacing * (len(self.buttons) - 1))
        top = cy - total_h // 2 + 40

        for i, btn in enumerate(self.buttons):
            btn.center_on(cx, top + i * (btn_h + spacing) + btn_h // 2)

        self._result: Optional[str] = None
        self._font = pygame.font.Font(FONT_PATH, 32)

        self.nickname_input = TextInput(
            x=WINDOW_WIDTH // 2 - 192 // 2, 
            y=64, 
            width=150, 
            height=32, 
            font_path=FONT_PATH, 
            font_size=32
        )

        self.stats_icon_btn = Button(
            rect=(self.nickname_input.rect.right + 10, self.nickname_input.rect.y, 32, 32), 
            image=pygame.transform.scale(stats_icon_image, (32, 32)), 
            callback=self._on_results 
        )

        self.selected_index = 0

    def _on_start(self): self._result = "start"
    def _on_levels(self): self._result = "levels"
    def _on_shop(self): self._result = "shop"
    def _on_results(self): self._result = "stats"
    def _on_options(self): self._result = "options"
    def _on_quit(self): self._result = "quit"

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.visible:
            return None

        self.nickname_input.handle_event(event)

        if self.stats_icon_btn.handle_event(event):
            result = self._result
            self._result = None
            return result

        m_pos = pygame.mouse.get_pos()
        for i, btn in enumerate(self.buttons):
            if btn.rect.collidepoint(m_pos):
                self.selected_index = i
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_index].callback()
                result = self._result
                self._result = None
                return result

        for i, btn in enumerate(self.buttons):
            if btn.handle_event(event):
                self.selected_index = i
                result = self._result
                self._result = None
                return result
            
        return None

    def draw(self):
        if not self.visible:
            return

        self.surface.blit(self.background_image, (0, 0))

        self.nickname_input.draw(self.surface)
        title_font = pygame.font.Font(FONT_PATH, 20)
        title_surf = title_font.render(" ", True, (221, 247, 244))
        self.surface.blit(title_surf, (self.nickname_input.rect.x, self.nickname_input.rect.y - 25))

        button_labels = ["Start", "Shop", "Levels", "Settings", "Quit"]
        for i, (btn, label) in enumerate(zip(self.buttons, button_labels)):

            btn.hovered = (i == self.selected_index)

            btn.draw(self.surface)
            color = (221, 247, 244)
            self._draw_button_text(btn, label, color)

        self.stats_icon_btn.draw(self.surface)

    def _draw_button_text(self, button: Button, text: str, color=(221, 247, 244)):
        surf = self._font.render(text, True, color)
        rect = surf.get_rect(center=button.rect.center)
        self.surface.blit(surf, rect)

    def show(self): self.visible = True
    def hide(self): self.visible = False


#finish menu
def show_game_over_screen(surface, gems: int) -> str:
    pygame.event.clear()
    button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()

    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
    overlay.fill((20, 20, 20))
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))

    font = pygame.font.Font(FONT_PATH, 32)
    small_font = pygame.font.Font(FONT_PATH, 24)

    title_surf = font.render("GAME OVER", True, (221, 247, 244))
    title_rect = title_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
    surface.blit(title_surf, title_rect)

    coins_surf = small_font.render(f"Gems collected: {gems}", True, (221, 247, 244))
    coins_rect = coins_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 70))

    button_font = pygame.font.Font(FONT_PATH, 32)
    btn_w, btn_h = 192, 48
    cx = WINDOW_WIDTH // 2

    restart_btn = Button(
        rect=(cx - btn_w//2, WINDOW_HEIGHT//2 - btn_h//2, btn_w, btn_h),
        image=button_image,
        callback=lambda: setattr(show_game_over_screen, "_choice", "restart")
    )

    menu_btn = Button(
        rect=(cx - btn_w//2, WINDOW_HEIGHT//2 + 40, btn_w, btn_h),
        image=button_image,
        callback=lambda: setattr(show_game_over_screen, "_choice", "menu")
    )

    def draw_button_text(btn, text):
        surf = button_font.render(text, True, (221, 247, 244))
        rect = surf.get_rect(center=btn.rect.center)
        surface.blit(surf, rect)

    show_game_over_screen._choice = None

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

        surface.blit(overlay, (0, 0))
        surface.blit(title_surf, title_rect)
        surface.blit(coins_surf, coins_rect)
        restart_btn.draw(surface)
        menu_btn.draw(surface)
        draw_button_text(restart_btn, "Restart")
        draw_button_text(menu_btn, "Menu")
        draw_styled_frame(surface)
        draw_close_button(surface)
        pygame.display.update()
        clock.tick(30)

    return show_game_over_screen._choice

