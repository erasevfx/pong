from config import *
from sprites import *
from groups import AllSprites
import json

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.running = True

        # score
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0, 'opponent': 0}

        # config
        try:
            with open(join('data', 'config.txt')) as config_file:
                self.config = json.load(config_file)
        except:
            self.config = {
                'SPEED': {'player': 1000, 'opponent': 1000, 'ball':900},
                'COLORS': {
                    'paddle': '#ee322c',
                    'paddle shadow': '#b12521', 
                    'ball': '#ee622c',
                    'ball shadow': '#c14f24',
                    'bg': '#002633',
                    'bg detail': '#004a63',
                },
        }
            
        # sprites 
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites), self.config)
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score, self.config)
        Opponent((self.all_sprites, self.paddle_sprites), self.config)

        self.font = pygame.font.Font(None, 320)

    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, self.config['COLORS']['bg detail'])
        player_rect = player_surf.get_rect(center = (WINDOW_WIDTH / 2 + 200, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, self.config['COLORS']['bg detail'])
        opponent_rect = opponent_surf.get_rect(center = (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        # line separater
        pygame.draw.line(self.display_surface, self.config['COLORS']['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 20)
    
    def reset_game_objects(self):
        # Remove existing sprites before reinitializing
        self.all_sprites.empty()
        self.paddle_sprites.empty()

        # Reinitialize the player, ball, and opponent with the new config
        self.player = Player((self.all_sprites, self.paddle_sprites), self.config)
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score, self.config)
        Opponent((self.all_sprites, self.paddle_sprites), self.config)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False
                    with open(join('data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)
                    with open(join('data', 'config.txt'), 'w') as config_file:
                        json.dump(self.config, config_file)
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    self.config = {
                        'SPEED': {'player': 1000, 'opponent': 1000, 'ball':900},
                        'COLORS': {
                            'paddle': '#ee322c',
                            'paddle shadow': '#b12521', 
                            'ball': '#ee622c',
                            'ball shadow': '#c14f24',
                            'bg': '#002633',
                            'bg detail': '#004a63',
                        }
                    }
                    self.reset_game_objects()
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    self.score = {'player': 0, 'opponent': 0}
            
            #update
            self.all_sprites.update(dt)
            
            #draw
            self.display_surface.fill(self.config['COLORS']['bg'])
            self.display_score()
            self.all_sprites.draw()
            pygame.display.update()
        pygame.quit()

    def update_score(self, side):
        self.score['player' if side =='player' else 'opponent'] += 1

if __name__ == '__main__':
    game = Game()
    game.run()