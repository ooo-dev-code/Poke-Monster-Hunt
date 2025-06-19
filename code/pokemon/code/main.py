from settings import *
from pokemon.code.support import *
from pokemon.code.timer import Timer
from pokemon.code.monster import *
from random import choice
from pokemon.code.ui import *
from pokemon.code.attack import AttackAnimationSprite

class Fight:
    def __init__(self, opponent, player, Game, team=None):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        self.Game = Game
        self.player = player
        self.player_active = True
        self.last_team = team

        # groups 
        self.all_sprites = pygame.sprite.Group()

        # data 
        self.player_monster_list = ['Larvea', "Ivieron", 'Plumette', 'Pluma', 'Sparchu', 'Cindrill']
        
        if self.last_team:
            self.new_player_monster_list = []
            for i in self.player_monster_list:
                try:
                    if self.last_team[i] > 0:
                        self.new_player_monster_list.append(i) 
                except:
                    print(i + 'is dead')
                if self.new_player_monster_list:
                    self.player_monsters = [Monster(name, self.back_surfs[name], health=self.last_team[name]) for name in self.new_player_monster_list]    
                else:
                    self.running = False
        else:
            self.player_monsters = [Monster(name, self.back_surfs[name]) for name in self.player_monster_list]
            
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = opponent
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        # ui 
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)

        # timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}
        
    def get_input(self, state, data = None):
        if state == 'attack':
            self.apply_attack(self.opponent, data)
            
        elif state == 'heal':
            self.monster.health = min(self.monster.health+50, self.monster.max_health)
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
            self.audio['green'].play()
        
        elif state == 'switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster

        elif state == 'escape':
            self.restart()
            
        self.player_active = False
        self.timers['player end'].activate()
        
    def restart(self):
        self.last_team = {}
        for i in self.player_monsters:
            self.last_team[i.name] = i.health
            
        self.Game(self.player, self.last_team).run()

    def apply_attack(self, target, attack):
        attack_data = ABILITIES_DATA[attack]
        attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
        target.health -= attack_data['damage'] * attack_multiplier
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
        self.audio[attack_data['animation']].play()

    def opponent_turn(self):
        if self.opponent.health <= 0:
            self.player_active = True
            self.opponent.kill()
            self.restart()
        else:
            attack = choice(self.opponent.abilities)
            self.apply_attack(self.monster, attack)
            self.timers['opponent end'].activate()

    def player_turn(self):
        self.player_active = True
        if self.monster.health <= 0:
            self.available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if self.available_monsters:
                self.monster.kill()
                self.monster = self.available_monsters[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
            else:
                self.running = False
                print("Fight Over! No monsters left.")

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.back_surfs = folder_importer('code', 'pokemon', 'images', 'back')
        self.front_surfs = folder_importer('code', 'pokemon', 'images', 'front')
        self.bg_surfs = folder_importer('code', 'pokemon', 'images', 'other')
        self.simple_surfs = folder_importer('code', 'pokemon', 'images', 'simple')
        self.attack_frames = tile_importer(4,'code', 'pokemon', 'images', 'attacks')
        self.audio = audio_importer('code', 'pokemon', 'audio')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # update
            self.update_timers()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()

            # draw  
            self.display_surface.blit(self.bg_surfs['bg'], (0,0))
            self.draw_monster_floor()
            self.opponent_ui.draw()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Fight()
    game.run()
