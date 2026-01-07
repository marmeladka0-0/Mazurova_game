import pygame

from settings import *

# FRAME_COLOR = (88, 83, 87)
FRAME_COLOR = (49, 43, 43)
BUTTON_SIZE = 24
BUTTON_COLOR = (169, 59, 58)
BUTTON_HOVER_COLOR = (130, 30, 30)
X_COLOR = (221, 247, 244)
TITLE_COLOR = (221, 247, 244)

CLOSE_BUTTON_RECT = pygame.Rect( WINDOW_WIDTH - BUTTON_SIZE - 4, 4, BUTTON_SIZE, BUTTON_SIZE)

def draw_styled_frame(surface):

    pygame.draw.rect(surface, FRAME_COLOR, (0, 0, WINDOW_WIDTH, FRAME_THICKNESS))

    #text
    font_size = int(FRAME_THICKNESS * 0.6) 
    font = pygame.font.Font(FONT_PATH, font_size)
    
    title_text = "DigOut: 2025 Edition"
    title_surf = font.render(title_text, True, TITLE_COLOR)
    
    title_rect = title_surf.get_rect(midleft=(15, FRAME_THICKNESS // 2))

    surface.blit(title_surf, title_rect)
    # blit - copy one image to another

def draw_close_button(surface):
    
    #check hover
    mouse_pos = pygame.mouse.get_pos()
    current_color = BUTTON_HOVER_COLOR if CLOSE_BUTTON_RECT.collidepoint(mouse_pos) else BUTTON_COLOR

    #background
    pygame.draw.rect(surface, current_color, CLOSE_BUTTON_RECT, border_radius=5)
    
    #X
    x, y, w, h = CLOSE_BUTTON_RECT
    pygame.draw.line(surface, X_COLOR, (x + 5, y + 5), (x + w - 5, y + h - 5), 3)
    pygame.draw.line(surface, X_COLOR, (x + w - 5, y + 5), (x + 5, y + h - 5), 3)

def check_frame_events(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        if CLOSE_BUTTON_RECT.collidepoint(event.pos):
            return True
            
    return False

def is_on_frame(pos):
    x, y = pos
    if 0 <= y <= FRAME_THICKNESS:
        if not CLOSE_BUTTON_RECT.collidepoint(pos):
            return True
    return False