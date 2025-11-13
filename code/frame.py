import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FRAME_THICKNESS

#Style settings

FRAME_COLOR = (40, 40, 40)
BUTTON_SIZE = 24
BUTTON_COLOR = (200, 50, 50)
BUTTON_HOVER_COLOR = (255, 80, 80)

#Button rectangle for click detection
CLOSE_BUTTON_RECT = pygame.Rect( WINDOW_WIDTH - BUTTON_SIZE - 4, 4, BUTTON_SIZE, BUTTON_SIZE)

def draw_styled_frame(surface):

    pygame.draw.rect(surface, FRAME_COLOR, (0, 0, WINDOW_WIDTH, FRAME_THICKNESS))

def draw_close_button(surface):
    
    #Check hover:
    mouse_pos = pygame.mouse.get_pos()
    current_color = BUTTON_HOVER_COLOR if CLOSE_BUTTON_RECT.collidepoint(mouse_pos) else BUTTON_COLOR

    #Button background
    pygame.draw.rect(surface, current_color, CLOSE_BUTTON_RECT, border_radius=5)
    
    #Button X
    x, y, w, h = CLOSE_BUTTON_RECT
    pygame.draw.line(surface, 'white', (x + 5, y + 5), (x + w - 5, y + h - 5), 3)
    pygame.draw.line(surface, 'white', (x + w - 5, y + 5), (x + 5, y + h - 5), 3)

def check_frame_events(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        if CLOSE_BUTTON_RECT.collidepoint(event.pos):
            return True
            
    return False