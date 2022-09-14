import pygame
from settings import *

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.display_surface = pygame.display.get_surface()
        self.x = x
        self.y = y 

        self.max_hp = max_hp 
        self.hp = hp

    def draw(self, hp): 
        # Update with new health
        self.hp = hp
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(self.display_surface, HEALTH_RED, (self.x, self.y, 150, 15))
        pygame.draw.rect(self.display_surface, HEALTH_GREEN, (self.x, self.y, 150 * health_ratio, 15))