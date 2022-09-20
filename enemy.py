import pygame
import random
from fighter import Fighter, draw_health_bar
from settings import enemy_info

class Enemy(Fighter):
    def __init__(self, x, y, name, groups):
        super().__init__(name, groups)

       # Characteristics
        self.name = name 
        self.strength = enemy_info[self.name]["strength"]
        self.max_hp = enemy_info[self.name]["max_hp"]
        self.start_potions = enemy_info[self.name]["start_potions"] 
        self.damage = self.strength + random.randint(-5,5)

        self.hp = self.max_hp
        self.potions = self.start_potions

       # Enemy location
        self.rect.center = (x,y)


    def draw_health(self, screen):
        if self.hp > 0:
            health_ratio = self.hp / self.max_hp

            # Draw a rectangle with the desired dimensions for the healh tbar
            self.health_rect = pygame.Rect(0, 0, 100, 8)
            self.health_rect.midbottom = self.rect.centerx, self.rect.bottom + 10

            # Draw the health bar on the surface
            draw_health_bar(screen, self.health_rect.bottomleft, self.health_rect.size, health_ratio)
        
        else:
            # Trick to hide the health bar upon enemy death
            draw_health_bar(screen, self.health_rect.bottomleft, (0,0), 0)

