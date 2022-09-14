import pygame, sys
from settings import *
from stage import Stage

class Game:
    def __init__(self, title:str):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.stage = Stage()


    # Method that handles events
    def handle_events(self):
        for event in pygame.event.get():
            # Check if user closes the game window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Listen for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.stage.player_input(True)
                else:
                    self.stage.player_input(False)

    # Method that draws the background
    def draw_background(self):
        self.screen.blit(self.stage.bg, (0,0))  

    # Method that handles game logic and updates game elements
    def update(self):
        self.stage.update()
        
    # Method that handles display
    def display(self):
        self.stage.draw()
        
    # Method that handles the game loop
    def run(self):
        while True:
            # Call all the above methods
            self.handle_events()
            self.draw_background()
            self.update()
            self.display()
            pygame.display.update()
            self.clock.tick(FPS)

            

                

            
            
            

        
        
    
