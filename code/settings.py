from os.path import join

#window settings
WINDOW_WIDTH = 640 #11
WINDOW_HEIGHT = 512 #9
CAPTION = "DigOut.CandyVersion"

TILE_SIZE = 64

FRAME_THICKNESS = 32

#pathes
PLAYER_IMAGE_PATH = join('images', 'player1_1.png')
ICON_IMAGE_PATH = join('images', 'player1.png')
ELEMENT_IMAGE_PATH = join('images', 'player1.png')
TILE_IMAGE_PATH = join('images', 'stone6.png')
BUTTON_IMAGE_PATH = join('images', 'button_4try.png')
#BUTTON_ONCLICK_IMAGE_PATH = join('images', 'button_1try_onclick.png')
DIRT_IMAGE_PATH = join('images', 'earth2.png')
BLUE_SPHERE_PATH = join('images', 'blue_sphere_1.png')
NICKNAME_ICON_PATH = join('images', 'nickname_icon_1.png')
PAUSE_ICON_PATH = join('images', 'pause_icon_1.png')
STONE_ROCK_PATH = join('images', 'stone_round_2.png')
GEM_IMAGE_PATH = join('images', 'gem_2.png')
MUSIC_REG_IMAGE_PATH = join('images', 'music_reg.png')
PLAYER_IMAGE_PATH2 = join('images', 'player2.png')
PLAYER_IMAGE_PATH3 = join('images', 'player3.png')
TRAP_IMAGE_PATH = join('images', 'lovushka.png')
BACKGROUND_IMAGE_PATH = join('images', 'download (3).png')
GHOST_IMAGE_PATH = join('images', 'ghost3.png')
SAVE_IMAGE_PATH = join('images', 'save_icon.png')
STAT_IMAGE_PATH = join('images', 'stat_icon.png')
DOC_IMAGE_PATH = join('images', 'file_icon.png')

#dead zone settings
DEAD_ZONE_TILES = 3 
DEAD_ZONE_WIDTH = DEAD_ZONE_TILES * TILE_SIZE
DEAD_ZONE_HEIGHT = DEAD_ZONE_TILES * TILE_SIZE

#display center
SCREEN_CENTER_X = WINDOW_WIDTH // 2
SCREEN_CENTER_Y = WINDOW_HEIGHT // 2 + FRAME_THICKNESS

FONT_PATH = './font/fibberish.ttf'
FONT_SIZE = 32
#FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
