import pygame
import math
from settings import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, tilemap, player):
        super().__init__()
        self.original_image = pygame.image.load(GHOST_IMAGE_PATH).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (TILE_SIZE, TILE_SIZE))

        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.original_image.get_rect()
        self.image = self.original_image
        
        self.tilemap = tilemap
        self.player = player
        
        self.world_x = player.world_x + 300
        self.world_y = player.world_y + 300
        self.speed = 1.5

    def update(self):
        dx = self.player.world_x - self.world_x
        dy = self.player.world_y - self.world_y
        dist = math.hypot(dx, dy) 
        # math.hypot() - sqrt(x*x + y*y)

        if dist != 0:
            self.world_x += (dx / dist) * self.speed
            self.world_y += (dy / dist) * self.speed

            if dx > 0:
                self.image = self.flipped_image
            else:
                self.image = self.original_image

        self.rect.x = self.world_x - self.tilemap.offset.x
        self.rect.y = self.world_y - self.tilemap.offset.y

        if self.rect.colliderect(self.player.rect):
            self.player.is_dead = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)