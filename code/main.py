import pygame
from random import randint

from settings import * 
from player import Player
from tilemap import TileMap
from frame import *
from menu import *
from datapanel import DataPanel 

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
    #element_image_path = ELEMENT_IMAGE_PATH
    #tile_image_path = TILE_IMAGE_PATH

    #initializing
    tilemap = None
    player = Player()
    datapanel = None

    #menu
    menu = Menu(display_surface)
    showing_menu = True

    #random background elements
    #elements_position = create_random_elements(20)

    running = True
    while running:
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                return "quit"


            #menu events
            result = menu.handle_event(event)
            if result == 'start' and tilemap is None:
                showing_menu = False

                #wait screen
                display_surface.fill('black')
                font = pygame.font.SysFont(None, 32)
                text = font.render("Your mom", True, (255, 255, 255))
                rect = text.get_rect(center=(SCREEN_CENTER_X, SCREEN_CENTER_Y))
                display_surface.blit(text, rect)
                draw_styled_frame(display_surface)
                draw_close_button(display_surface)
                pygame.display.update()

                MAP_WIDTH = 200
                MAP_HEIGHT = 150
                tilemap = TileMap()
                #tilemap.save_map_to_file('data/level_1_map.txt')
                player = Player(player_image_path, tilemap)
                datapanel = DataPanel()
                player.initial_y_offset = tilemap.offset.y
            elif result == 'quit':
                return "quit"
                running = False
            elif result == 'options':
                pass
                #print('Menu: options (not implemented)')

            if not showing_menu and player and event.type == pygame.KEYDOWN:
                player.handle_move_event(event)

            if check_frame_events(event):
                running = False

            if player.resources_collected < 0:
                choice = show_game_over_screen(display_surface)
                return choice
            
        if not showing_menu and tilemap and player:
            player.update()
            
            display_surface.fill('bisque4')
            tilemap.partition_draw(display_surface)
            player.draw(display_surface)
            datapanel.draw(display_surface, player)

            # draw_background_elements(display_surface, element_image, elements_position)

        if showing_menu:
            menu.draw()

        draw_styled_frame(display_surface)
        draw_close_button(display_surface)

        pygame.display.update()

    return "quit"
    #pygame.quit()


if __name__ == '__main__':
    while True:
        result = run_game()

        if result == "menu":
            continue

        if result == "quit":
            pygame.quit()
            break
