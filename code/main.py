import pygame
from random import randint

from settings import * 
from player import Player
from tilemap import TileMap
from frame import *

def setup_game():
    
    pygame.init() 

    
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS), pygame.NOFRAME)
    pygame.display.set_caption(CAPTION) 

    
    try:
        icon_image = pygame.image.load(ICON_IMAGE_PATH).convert_alpha()
        element_image = pygame.image.load(ELEMENT_IMAGE_PATH).convert_alpha()

        pygame.display.set_icon(icon_image)
    except pygame.error as e:
        print(f"Image download exeption: {e}")
        icon_image = None 
        element_image = None

    return display_surface, icon_image, element_image

def create_random_elements(num_elements):
    return [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(num_elements)]

def draw_background_elements(surface, element_image, positions):
    for position in positions:
        surface.blit(element_image, position)

def run_game():

    display_surface, icon_image, element_image = setup_game()
    
    player_image_path = PLAYER_IMAGE_PATH
    element_image_path = ELEMENT_IMAGE_PATH
    tile_image_path = TILE_IMAGE_PATH

    #Player creation
    
    tilemap = TileMap()
    player = Player(player_image_path, tilemap)

    #Random background elements
    elements_position = create_random_elements(20)

    running = True
    while running:
        #To stop the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.handle_move_event(event)
            if check_frame_events(event):
                running = False

        #===Updates===
        #Keys handling
        #keys = pygame.key.get_pressed()
        #player.handle_input(keys)

        #Player
        player.update()
        

        #===Visuals===
        #Background
        display_surface.fill('bisque4')

        tilemap.draw(display_surface)

        draw_styled_frame(display_surface)
        draw_close_button(display_surface)
        #Elements
        #draw_background_elements(display_surface, element_image, elements_position)
        
        #Player draw
        player.draw(display_surface)
        
        pygame.display.update() 

    pygame.quit()

if __name__ == '__main__':
    run_game()
