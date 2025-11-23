from os.path import join
import pygame

#window settings
WINDOW_WIDTH = 640 #11
WINDOW_HEIGHT = 512 #9
CAPTION = "DigOut.CandyVersion"

TILE_SIZE = 64

FRAME_THICKNESS = 32

#pathes
PLAYER_IMAGE_PATH = join('images', 'player1_mini.png')
ICON_IMAGE_PATH = join('images', 'player1_mini.png')
ELEMENT_IMAGE_PATH = join('images', 'player1_mini.png')
TILE_IMAGE_PATH = join('images', 'block.png')
BUTTON_IMAGE_PATH = join('images', 'button_1try.png')
BUTTON_ONCLICK_IMAGE_PATH = join('images', 'button_1try_onclick.png')
DIRT_IMAGE_PATH = join('images', 'player1_mini.png')

#dead zone settings
DEAD_ZONE_TILES = 3 
DEAD_ZONE_WIDTH = DEAD_ZONE_TILES * TILE_SIZE
DEAD_ZONE_HEIGHT = DEAD_ZONE_TILES * TILE_SIZE

#display center
SCREEN_CENTER_X = WINDOW_WIDTH // 2
SCREEN_CENTER_Y = WINDOW_HEIGHT // 2 + FRAME_THICKNESS