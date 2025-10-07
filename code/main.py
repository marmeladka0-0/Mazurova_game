import pygame
from os.path import join #to show the path to file correctly

from random import randint #for randow display of sparks or etc.

# general setup
pygame.init() #initialize

#window size
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("DigOut.CandyVersion") #change the name of window

#set icon
path = join('images', 'player1_mini.png') #ота страшна бібліотека
#.convert() for not transperent and .convert_alpha() for transperent
icon = pygame.image.load(path).convert_alpha()
pygame.display.set_icon(icon)

running = True

#surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

#player
player_surf = icon
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
#rect целие числа frect нецелие
player_direction = 1

#random elements positions
elements_position = [(randint(0, WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)) for i in range(20)]

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draw the game
    # fill with the one color
    display_surface.fill('bisque4')

    #random background elements
    for position in elements_position:
        display_surface.blit(player_surf, position)

    player_rect.x += player_direction * 0.4
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_direction *= -1
    display_surface.blit(player_surf, player_rect) #one surface to another
    
    # pygame.display.flip() # update part of the window
    pygame.display.update() # update entire window

    #pygame.Surface((width, height)) To create a plain surface
    #pygame.image.load(path) To create a surface from an image
    #font.render(text, AntiAlias, Color) To create a surface from text



pygame.quit() #uninitialize
