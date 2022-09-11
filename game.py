import pygame
from fighter import Fighter

# Game class and corresponding methods
class Game:
    def __init__(self, title:str, width:int, height:int, fps:int = 60):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.bg = pygame.image.load('assets/Background.png').convert_alpha()

        self.running = True
        self.fps = fps
        self.clock = pygame.time.Clock()

        #Create an instance of each fighter type
        self.hero = Fighter(200, 350, 'Hero')
        bat = Fighter(500, 320, 'Bat')
        plaguedoctor = Fighter(600, 350, 'PlagueDoctor')

        # Add enemies to a list
        self.enemy_list = []
        self.enemy_list.append(bat)
        self.enemy_list.append(plaguedoctor)

    # Method loads and draws images
    def initialize(self):

        # Draw background
        self.screen.blit(self.bg, (0,0))


    # Method that handles events
    def handle_events(self):
        # Player actions

        # User closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

    # Method that handles game logic and updates game elements
    def update(self):
        self.hero.update()

        for enemy in self.enemy_list:
            enemy.update()

    
    # Method that handle display
    def display(self):
        self.hero.draw(self.screen)

        for enemy in self.enemy_list:
            enemy.draw(self.screen)
        

    # Method that handles the game loop
    def run(self):
        while self.running:
            # Call all the above methods
            self.initialize()
            self.handle_events()
            self.update()
            self.display()
            self.clock.tick(self.fps)
            pygame.display.update()

        
        pygame.quit()
    
