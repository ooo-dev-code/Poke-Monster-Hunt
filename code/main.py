from settings import *
from groups import AllSprites
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from os import *
from random import *
from enemy import Enemy

class Game:
    def __init__(self, player=None, last_team = None):
        # setup
        pygame.init()
        
        self.last_team = last_team
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.prev_player = player

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_collision_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
            
        for obj in map.get_layer_by_name('Entities'): 
            num_enemies = randint(0, 2)
            name = choice(list(MONSTER_DATA.keys()))
            if obj.name == 'Enemy' and num_enemies == 1:
                self.enemy = Enemy((obj.x, obj.y),  name,(self.all_sprites, self.enemy_collision_sprites))
            if obj.name == 'Player':
                if self.prev_player:
                    print(self.prev_player[0])
                    self.player = Player((self.prev_player[0],self.prev_player[1]), self.all_sprites, self.collision_sprites, self.enemy_collision_sprites, Game, self.last_team)
                else:
                    self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites, self.enemy_collision_sprites, Game, self.last_team)

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(60) / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update 
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

game = Game()
game.run()