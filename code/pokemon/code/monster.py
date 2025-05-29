from settings import *
from random import sample

class Creature:
    def get_data(self, name, health = None):
        self.name = name
        self.element = MONSTER_DATA[name]["element"]
        if health:
            self.health = health
            self.max_health = MONSTER_DATA[name]["health"]
        else:
            self.health = self.max_health = MONSTER_DATA[name]["health"]
        self.abilities = sample(list(ABILITIES_DATA), 4)

class Monster(pygame.sprite.Sprite, Creature):
    def __init__(self, name, surf, health=None):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.get_data(name, health)

class Opponent(pygame.sprite.Sprite, Creature):
    def __init__(self, name, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH-250, 300))
        self.get_data(name)