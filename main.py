import pygame
from data.game import Game


if __name__ == "__main__":
    pygame.init()
    game = Game("Cavern Brawl")
    game.run()
