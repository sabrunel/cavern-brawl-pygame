import pygame, sys
from settings import *
from stage import Stage

# Game class and corresponding methods
class Game:
    def __init__(self, title:str):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.stage = Stage()

    def draw_background(self):
        self.screen.blit(self.stage.bg, (0,0))    

    # Method that handles game logic and updates game elements
    def update(self):
        self.stage.update()
    
    # Method that handle display
    def display(self):
        self.stage.draw()

    # Method that handles events
    def handle_events(self):
        pass
        
    # Method that handles the game loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Call all the above methods
            self.draw_background()
            self.handle_events()
            self.update()
            self.display()
            pygame.display.update()
            self.clock.tick(FPS)
            

        
        
    
