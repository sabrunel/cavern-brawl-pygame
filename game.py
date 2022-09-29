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
        # Check if user closes the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            # Listen for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
               self.stage.player_clicked = True
            else:
               self.stage.player_clicked = False
     
    # Method that handles the game loop
    def run(self):
        while True:

            self.handle_events()
            self.stage.run()
            pygame.display.update()
            self.clock.tick(FPS)

            

                

            
            
            

        
        
    
