import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from random import randint
from ctypes import windll

from settings import * 
from player import Player
from tilemap import TileMap
from frame import check_frame_events
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

class Game:
    def __init__(self):
        self.display_surface = setup_game()
        audio_manager.play_music()
        self.clock = pygame.time.Clock()
        self.player_image_path = PLAYER_IMAGE_PATH

        #initializing
        self.tilemap = None
        self.player = Player()
        self.datapanel = None
        self.ghost = None

        #menu
        self.menu = Menu(self.display_surface)
        self.showing_menu = True
        saved_music = self.menu.nickname_input.game_data["music_volume"]
        saved_sound = self.menu.nickname_input.game_data["sound_volume"]

        audio_manager.set_music_volume(saved_music)
        audio_manager.set_sounds_volume(saved_sound)

        self.options_menu = OptionsMenu(self.display_surface)
        self.showing_options = False
        self.pause_menu = PauseMenu(self.display_surface)
        self.is_paused = False

        self.light_manager = LightManager()

        self.shop_menu = ShopMenu(self.display_surface, self.menu.nickname_input)
        self.showing_shop = False

        self.stats_menu = StatsMenu(self.display_surface)
        self.showing_stats = False
        self.levels_menu = LevelsMenu(self.display_surface)
        self.showing_levels = False

        self.running = True
        self.gems = self.menu.nickname_input.game_data["gems"]
        self.tilemap_width = self.menu.nickname_input.game_data["map_w"]
        self.tilemap_height = self.menu.nickname_input.game_data["map_h"]
        if self.menu.nickname_input.game_data["selected_skin"] == 1:
            self.player_image_path = PLAYER_IMAGE_PATH2
            # print("Selected skin 1")
        elif self.menu.nickname_input.game_data["selected_skin"] == 2:
            self.player_image_path = PLAYER_IMAGE_PATH3
            # print("Selected skin 2")
        self.session_traps_destroyed = 0
        self.state = "menu" 
        # можливо на майбутнє ось так зберігати

    @property
    def is_game_active(self):
        return ( 
            not self.showing_menu and 
            not self.showing_options and 
            not self.showing_shop and 
            not self.showing_stats and 
            not self.showing_levels
        )

    def start_new_game(self, display_surface, player_image_path, tilemap_width=200, tilemap_height=150, map_file=None):
        #wait screen
        display_surface.fill((20, 20, 20))
        font = pygame.font.Font(FONT_PATH, 32)
        text = font.render("Please wait...", True, (221, 247, 244))
        rect = text.get_rect(center=(SCREEN_CENTER_X, SCREEN_CENTER_Y))
        display_surface.blit(text, rect)
        draw_styled_frame(display_surface)
        draw_close_button(display_surface)
        pygame.display.update()

        self.tilemap = TileMap(tilemap_width, tilemap_height, map_data=map_file)
        self.player = Player(player_image_path, self.tilemap)
        self.datapanel = DataPanel()
        self.ghost = Ghost(self.tilemap, self.player)
        self.player.initial_y_offset = self.tilemap.offset.y 
        return self.tilemap, self.player, self.datapanel, self.ghost

    def _handle_menu_events(self, event):
        result = self.menu.handle_event(event)
        if result == 'start' and self.tilemap is None:
            self.showing_menu = False
            audio_manager.play_sound('click')
            if self.menu.nickname_input.game_data["selected_skin"] == 0:
                self.player_image_path = PLAYER_IMAGE_PATH
            elif self.menu.nickname_input.game_data["selected_skin"] == 1:
                self.player_image_path = PLAYER_IMAGE_PATH2
            elif self.menu.nickname_input.game_data["selected_skin"] == 2:
                self.player_image_path = PLAYER_IMAGE_PATH3
            self.tilemap, self.player, self.datapanel, self.ghost = self.start_new_game(self.display_surface, self.player_image_path, self.tilemap_width, self.tilemap_height)
            self.tilemap.save_full_map_to_file()
        elif result == 'quit':
            audio_manager.play_sound('click')
            pygame.time.delay(500)
            return "quit"
        elif result == 'options':
            audio_manager.play_sound('click')
            self.showing_menu = False
            self.showing_options = True
            self.options_menu.visible = True
        elif result == 'shop':
            audio_manager.play_sound('click')
            self.showing_shop = True
            self.showing_menu = False
            self.shop_menu.show()
        elif result == 'stats':
            audio_manager.play_sound('click')
            self.showing_stats = True
            self.showing_menu = False
        elif result == 'levels':
            audio_manager.play_sound('click')
            self.showing_levels = True
            self.showing_menu = False
            self.levels_menu.visible = True  

    def _handle_options_events(self, event): 
        result = self.options_menu.handle_event(event)
        # print (result)
        if result is not None:
            if result and result["action"] == "back":
                audio_manager.play_sound('click')
                
                self.menu.nickname_input.save_game_data(
                    map_w=result["map_w"],
                    map_h=result["map_h"],
                    music_volume=result["music_volume"],
                    sound_volume=result["sound_volume"]
                )

                self.tilemap_width = result["map_w"]
                self.tilemap_height = result["map_h"]
                self.showing_options = False
                self.showing_menu = True
                self.display_surface.fill('black')

    def _handle_shop_events(self, event):
        result = self.shop_menu.handle_event(event, player_coins=self.gems)
        if result is not None:
            if result["action"] == "back":
                audio_manager.play_sound('click')
                self.menu.nickname_input.save_game_data(
                        gems=result["gems"]
                    )
                self.display_surface.fill('black')
                self.showing_shop = False
                self.showing_menu = True
                # menu.nickname_input.game_data = menu.nickname_input.load_all_data()
            elif isinstance(result, dict) and result["action"] == "buy":
                # isinstance - checks if dict
                # audio_manager.play_sound('click')
                self.gems = result["gems"]

    def _handle_levels_events(self, event):
        result = self.levels_menu.handle_event(event)
        if result is not None:
            if result:
                if result["action"] == "back":
                    self.showing_levels = False
                    self.showing_menu = True
                    audio_manager.play_sound('cancel')
                elif result["action"] == "load":
                    self.showing_levels = False
                    audio_manager.play_sound('click')
                    
                    map_file = load_map_from_txt(f"./data/slot{result['slot']}.txt")

                    self.tilemap, self.player, self.datapanel, self.ghost = self.start_new_game(
                        self.display_surface, 
                        self.player_image_path, 
                        self.tilemap_width, 
                        self.tilemap_height,
                        map_file=map_file
                    )


    def run_game(self):
        
        while self.running:

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


                if self.showing_options:
                    self._handle_options_events(event)
                    
                elif self.showing_stats:
                    res = self.stats_menu.handle_event(event)
                    if res == "back":
                        self.showing_stats = False
                        self.showing_menu = True
                        self.display_surface.fill('black')

                #menu events
                elif self.showing_menu:
                    result = self._handle_menu_events(event)
                    if result == "quit":
                        return "quit"
                    

                if self.showing_levels:
                    self._handle_levels_events(event)

                if self.showing_shop:
                    self._handle_shop_events(event)

                if self.is_game_active and not self.is_paused:
                    result = self.datapanel.handle_event(event)
                    if result == "pause":
                        audio_manager.play_sound('click')
                        self.is_paused = True
                        self.pause_menu.visible = True
                    elif result == "save_map":
                        audio_manager.play_sound('click')
                        self.tilemap.save_full_map_to_file("./data/slot0.txt")

                if self.is_paused:
                    res = self.pause_menu.handle_event(event)
                    if res:
                        audio_manager.play_sound('click')
                        self.is_paused = False
                        self.pause_menu.visible = False
                        if res == "menu":
                            self.showing_menu = True
                            self.tilemap = None
                            return 'menu'
                # ВИПРАВЛЕННЯ, ВИКОРИСТАННЯ ВЛАСТИВОСТІ!!!
                if self.is_game_active and event.type == pygame.KEYDOWN:
                    self.player.handle_move_event(event)

                if check_frame_events(event):
                    audio_manager.play_sound('cancel')
                    pygame.time.delay(500)
                    return "quit"


            if self.is_game_active and self.tilemap and self.player:
                if not self.is_paused:
                    result = self.player.update()
                    changed, traps_count = self.tilemap.apply_gravity(self.player)
                    result = result
                    self.session_traps_destroyed += traps_count
                    self.light_manager.update()
                    self.ghost.update()
                    if self.player.blocks_dug_now > 0:
                        self.menu.nickname_input.game_data["blocks_dug"] += self.player.blocks_dug_now
                        self.player.blocks_dug_now = 0
                    if self.player.max_depth_reached > self.menu.nickname_input.game_data["max_depth"]:
                        self.menu.nickname_input.game_data["max_depth"] = self.player.max_depth_reached
                if result == "game_over" or self.player.resources_collected < 1:
                    self.gems += self.player.gems_collected
                    self.menu.nickname_input.save_game_data(gems = self.gems)
                    traps_count = self.menu.nickname_input.game_data["traps_count"] + self.session_traps_destroyed

                    self.menu.nickname_input.save_game_data(traps_count = traps_count)
                    choice = show_game_over_screen(self.display_surface, self.player.gems_collected)
                    if choice == 'menu':
                        audio_manager.play_sound('click') 
                        self.tilemap = None
                        self.showing_menu = True
                        return 'menu'
                    if choice == 'quit':
                        audio_manager.play_sound('click')
                        pygame.time.delay(500)
                        return 'quit'
                    if choice == 'restart':
                        audio_manager.play_sound('click')
                        self.tilemap, self.player, self.datapanel, self.ghost = self.start_new_game(self.display_surface, self.player_image_path, self.tilemap_width, self.tilemap_height)
                        self.tilemap.save_full_map_to_file()

                self.display_surface.fill(('bisque4'))            
                self.tilemap.partition_draw(self.display_surface)
                self.player.draw(self.display_surface)
                self.ghost.draw(self.display_surface)
                self.light_manager.draw(self.display_surface, self.player)
                self.datapanel.draw(self.display_surface, self.player)

                if self.is_paused:
                    self.pause_menu.draw()  

            if self.showing_options:
                self.options_menu.draw()
            elif self.showing_shop:
                self.shop_menu.draw(self.gems)
            elif self.showing_stats:
                self.stats_menu.draw(self.menu.nickname_input.game_data)
            elif self.showing_levels:
                self.levels_menu.draw()    
            elif self.showing_menu:
                self.menu.draw()

            draw_styled_frame(self.display_surface)
            draw_close_button(self.display_surface)

            pygame.display.update()
            self.clock.tick(60)

        return "quit"


if __name__ == '__main__':
    game = Game()
    while True:
        result = game.run_game()

        if result == "menu":
            continue

        if result == "quit":
            pygame.quit()
            break
