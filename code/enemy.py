import pygame
import random
from settings import *
from pokemon.code.support import folder_importer

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups):
        super().__init__(groups)
        self.name = name

        # Load and scale image
        self.simple_surfs = folder_importer('code', 'pokemon', 'images', 'simple')
        self.image = self.simple_surfs[self.name]
        original_size = self.image.get_size()
        scale_factor = 2
        new_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect(center=pos)

        # --- Random movement properties ---
        self.direction = pygame.Vector2(0, 0)
        self.speed = 2
        self.change_direction_time = pygame.time.get_ticks()
        self.change_interval = 1000  # Change direction every 1 second

    def update(self, dt):
        # Randomly change direction at intervals
        current_time = pygame.time.get_ticks()
        if current_time - self.change_direction_time > self.change_interval:
            self.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            self.change_direction_time = current_time

        # Normalize direction to prevent faster diagonal movement
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()

        # Move the enemy
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
