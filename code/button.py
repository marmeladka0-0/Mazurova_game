import pygame
from typing import Callable, Optional, Tuple


def adjust_brightness(image: pygame.Surface, amount: int) -> pygame.Surface:
    img = image.copy()
    if amount > 0:
        img.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_ADD)
    else:
        img.fill((-amount, -amount, -amount), special_flags=pygame.BLEND_RGB_SUB)
    return img


class Button:
    def __init__(
        self,
        rect: Tuple[int, int, int, int], #незміний список елементів
        image: pygame.Surface,
        callback: Optional[Callable] = None,
        *,
        hover_brightness: int = 30,
        pressed_brightness: int = -40
    ):
        self.rect = pygame.Rect(rect)
        self.callback = callback

        self.image_default = pygame.transform.scale(image, self.rect.size)
        self.image_hover = adjust_brightness(self.image_default, hover_brightness)
        self.image_pressed = adjust_brightness(self.image_default, pressed_brightness)

        self.enabled = True
        self.hovered = False
        self.pressed = False

    def handle_event(self, event: pygame.event.Event):
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    if callable(self.callback):
                        self.callback()
                    return True

        return False

    def draw(self, surface: pygame.Surface):
        if not self.enabled:
            img = adjust_brightness(self.image_default, -60)
        elif self.pressed:
            img = self.image_pressed
        elif self.hovered:
            img = self.image_hover
        else:
            img = self.image_default

        surface.blit(img, self.rect)

    def set_enabled(self, value: bool):
        self.enabled = value
        if not value:
            self.hovered = False
            self.pressed = False

    def move(self, dx: int, dy: int):
        self.rect.move_ip(dx, dy)

    def center_on(self, x: int, y: int):
        self.rect.center = (x, y)
