import pygame
from game import Game


if __name__ == "__main__":
    pygame.init()
    game = Game("Cavern Brawl", 800, 450)
    game.initialize()
    game.run()
