import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from random import randint
from ctypes import windll

from settings import * 
from player import Player
from tilemap import TileMap
#from frame import *
from menu import *
from datapanel import DataPanel 
from options import *
from audio import audio_manager
from pause import PauseMenu
from light import LightManager
from shop import ShopMenu
from stats import StatsMenu
from ghost import Ghost
from levels import LevelsMenu, load_map_from_txt

def setup_game():
    
    pygame.init() 
    
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS), pygame.NOFRAME)
    pygame.display.set_caption(CAPTION) 

    return display_surface

def create_random_elements(num_elements):
    return [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(num_elements)]

def draw_background_elements(surface, element_image, positions):
    for position in positions:
        surface.blit(element_image, position)

def start_new_game(display_surface, player_image_path, tilemap_width=200, tilemap_height=150, map_file=None):
    #wait screen
    display_surface.fill((20, 20, 20))
    font = pygame.font.Font(FONT_PATH, 32)
    text = font.render("Please wait...", True, (221, 247, 244))
    rect = text.get_rect(center=(SCREEN_CENTER_X, SCREEN_CENTER_Y))
    display_surface.blit(text, rect)
    draw_styled_frame(display_surface)
    draw_close_button(display_surface)
    pygame.display.update()

    tilemap = TileMap(tilemap_width, tilemap_height, map_data=map_file)
    player = Player(player_image_path, tilemap)
    datapanel = DataPanel()
    ghost = Ghost(tilemap, player)
    player.initial_y_offset = tilemap.offset.y

    return tilemap, player, datapanel, ghost

def run_game():
    display_surface = setup_game()
    audio_manager.play_music()
    clock = pygame.time.Clock()
    player_image_path = PLAYER_IMAGE_PATH

    #initializing
    tilemap = None
    player = Player()
    datapanel = None
    ghost = None

    #menu
    menu = Menu(display_surface)
    showing_menu = True
    saved_music = menu.nickname_input.game_data["music_volume"]
    saved_sound = menu.nickname_input.game_data["sound_volume"]

    audio_manager.set_music_volume(saved_music)
    audio_manager.set_sounds_volume(saved_sound)

    options_menu = OptionsMenu(display_surface)
    showing_options = False
    pause_menu = PauseMenu(display_surface)
    is_paused = False

    light_manager = LightManager()

    shop_menu = ShopMenu(display_surface, menu.nickname_input)
    showing_shop = False

    stats_menu = StatsMenu(display_surface)
    showing_stats = False
    levels_menu = LevelsMenu(display_surface)
    showing_levels = False

    running = True
    gems = menu.nickname_input.game_data["gems"]
    tilemap_width = menu.nickname_input.game_data["map_w"]
    tilemap_height = menu.nickname_input.game_data["map_h"]
    if menu.nickname_input.game_data["selected_skin"] == 1:
        player_image_path = PLAYER_IMAGE_PATH2
        # print("Selected skin 1")
    elif menu.nickname_input.game_data["selected_skin"] == 2:
        player_image_path = PLAYER_IMAGE_PATH3
        # print("Selected skin 2")
    session_traps_destroyed = 0



    while running:

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and is_on_frame(event.pos):
                    #T_T why i add a new панелька зверху
                    pygame.display.get_wm_info() #dict with texnical info
                    if os.name == 'nt': #only for Windows
                        #send a system message
                        windll.user32.ReleaseCapture()
                        windll.user32.SendMessageW(pygame.display.get_wm_info()['window'], 0xA1, 2, 0)


            if showing_options:
                result = options_menu.handle_event(event)
                # print (result)
                if result is not None:
                    if result and result["action"] == "back":
                        audio_manager.play_sound('click')
                        
                        menu.nickname_input.save_game_data(
                            map_w=result["map_w"],
                            map_h=result["map_h"],
                            music_volume=result["music_volume"],
                            sound_volume=result["sound_volume"]
                        )
                        
                        tilemap_width = result["map_w"]
                        tilemap_height = result["map_h"]
                        showing_options = False
                        showing_menu = True
                        display_surface.fill('black')

            elif showing_stats:
                res = stats_menu.handle_event(event)
                if res == "back":
                    showing_stats = False
                    showing_menu = True
                    display_surface.fill('black')

            #menu events
            elif showing_menu:
                result = menu.handle_event(event)
                if result == 'start' and tilemap is None:
                    showing_menu = False
                    audio_manager.play_sound('click')
                    if menu.nickname_input.game_data["selected_skin"] == 0:
                        player_image_path = PLAYER_IMAGE_PATH
                    elif menu.nickname_input.game_data["selected_skin"] == 1:
                        player_image_path = PLAYER_IMAGE_PATH2
                    elif menu.nickname_input.game_data["selected_skin"] == 2:
                        player_image_path = PLAYER_IMAGE_PATH3
                    tilemap, player, datapanel, ghost = start_new_game(display_surface, player_image_path, tilemap_width, tilemap_height)
                    tilemap.save_full_map_to_file()
                elif result == 'quit':
                    audio_manager.play_sound('click')
                    pygame.time.delay(500)
                    return "quit"
                    running = False
                elif result == 'options':
                    audio_manager.play_sound('click')
                    showing_menu = False
                    showing_options = True
                    options_menu.visible = True
                elif result == 'shop':
                    audio_manager.play_sound('click')
                    showing_shop = True
                    showing_menu = False
                    shop_menu.show()
                elif result == 'stats':
                    audio_manager.play_sound('click')
                    showing_stats = True
                    showing_menu = False
                elif result == 'levels':
                    audio_manager.play_sound('click')
                    showing_levels = True
                    showing_menu = False
                    levels_menu.visible = True

            if showing_levels:
                result = levels_menu.handle_event(event)
                if result is not None:
                    if result:
                        if result["action"] == "back":
                            showing_levels = False
                            showing_menu = True
                            audio_manager.play_sound('cancel')
                        elif result["action"] == "load":
                            showing_levels = False
                            audio_manager.play_sound('click')
                            
                            map_file = load_map_from_txt(f"./data/slot{result['slot']}.txt")
                            
                            tilemap, player, datapanel, ghost = start_new_game(
                                display_surface, 
                                player_image_path, 
                                tilemap_width, 
                                tilemap_height,
                                map_file=map_file
                            )
                            pass

            if showing_shop:
                result = shop_menu.handle_event(event, player_coins=gems)
                if result is not None:
                    if result["action"] == "back":
                        menu.nickname_input.save_game_data(
                                gems=result["gems"]
                            )
                        display_surface.fill('black')
                        showing_shop = False
                        showing_menu = True
                        # menu.nickname_input.game_data = menu.nickname_input.load_all_data()
                    elif isinstance(result, dict) and result["action"] == "buy":
                        gems = result["gems"]

            if not showing_options and not showing_menu and not showing_shop and not showing_stats and not showing_levels:
                result = datapanel.handle_event(event)
                if result == "pause":
                    is_paused = True
                    pause_menu.visible = True
                elif result == "save_map":
                    tilemap.save_full_map_to_file("./data/slot0.txt")

            if is_paused:
                res = pause_menu.handle_event(event)
                if res == "resume":
                    is_paused = False
                    pause_menu.visible = False
                elif res == "menu":
                    is_paused = False
                    pause_menu.visible = False
                    return 'menu'

            if not showing_menu and not showing_options and not showing_shop and not showing_levels and player and event.type == pygame.KEYDOWN:
                player.handle_move_event(event)

            if check_frame_events(event):
                audio_manager.play_sound('cancel')
                pygame.time.delay(500)
                running = False


        if not showing_menu and not showing_shop and not showing_options and not showing_stats and not showing_levels and tilemap and player:
            if not is_paused:
                result = player.update()
                changed, traps_count = tilemap.apply_gravity(player)
                result = result
                session_traps_destroyed += traps_count
                light_manager.update()
                ghost.update()
                if player.blocks_dug_now > 0:
                    menu.nickname_input.game_data["blocks_dug"] += player.blocks_dug_now
                    player.blocks_dug_now = 0
                if player.max_depth_reached > menu.nickname_input.game_data["max_depth"]:
                    menu.nickname_input.game_data["max_depth"] = player.max_depth_reached

            if result == "game_over" or player.resources_collected < 1:
                gems += player.gems_collected
                menu.nickname_input.save_game_data(gems = gems)
                traps_count = menu.nickname_input.game_data["traps_count"] + session_traps_destroyed

                menu.nickname_input.save_game_data(traps_count = traps_count)
                choice = show_game_over_screen(display_surface, player.gems_collected)
                if choice == 'menu': 
                    return 'menu'
                if choice == 'quit':
                    return 'quit'
                if choice == 'restart':
                    tilemap, player, datapanel, ghost = start_new_game(display_surface, player_image_path, tilemap_width, tilemap_height)
                    tilemap.save_full_map_to_file()

            display_surface.fill(('bisque4'))            
            tilemap.partition_draw(display_surface)
            player.draw(display_surface)
            ghost.draw(display_surface)
            light_manager.draw(display_surface, player)
            datapanel.draw(display_surface, player)

            if is_paused:
                pause_menu.draw()


        if showing_options:
            options_menu.draw()
        elif showing_shop:
            shop_menu.draw(gems)
        elif showing_stats:
            stats_menu.draw(menu.nickname_input.game_data)
        elif showing_levels:
            levels_menu.draw()    
        elif showing_menu:
            menu.draw()

        draw_styled_frame(display_surface)
        draw_close_button(display_surface)

        pygame.display.update()
        clock.tick(60)

    return "quit"


if __name__ == '__main__':
    while True:
        result = run_game()

        if result == "menu":
            continue

        if result == "quit":
            pygame.quit()
            break
