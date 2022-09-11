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

    # Method loads and draws images
    def initialize(self):

        # Draw background
        self.screen.blit(self.bg, (0,0))

        #Create an instance of the Hero
        self.hero = Fighter(200, 350, 'Hero')


    # Method that handles events
    def handle_events(self):

        # User closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

    # Method that handles game logic and updates game elements
    def update(self):
        pygame.display.update()
    
    # Method that handle display
    def display(self):
        self.hero.draw(self.screen)
        

    # Method that handles the game loop
    def run(self):
        while self.running:
            # Call all the above methods
            self.handle_events()
            self.update()
            self.display()
            self.clock.tick(self.fps)

        pygame.quit()
    
