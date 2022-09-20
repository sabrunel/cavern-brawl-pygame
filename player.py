import pygame
import random
from fighter import Fighter, draw_health_bar
from settings import PLAYER_MAX_HP, PLAYER_START_POTIONS, PLAYER_STRENGTH


class Player(Fighter):
    def __init__(self, x, y, name, groups):
        super().__init__(name, groups)

        # Characteristics
        self.name = name
        self.max_hp = PLAYER_MAX_HP
        self.strength = PLAYER_STRENGTH
        self.start_potions = PLAYER_START_POTIONS 
        self.damage = self.strength + random.randint(-5,5)

        self.hp = self.max_hp
        self.potions = self.start_potions

        # Player location
        self.rect.center = (x,y)


    def draw_health(self, screen):
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp

        # Position the health bar
        self.health_rect = pygame.Rect(0, 0, 100, 8)

        # Draw the health bar on the surface
        draw_health_bar(screen, (15, 15), (200, 15), health_ratio) 

    def reset(self):
        self.hp = self.max_hp 
        self.potions = self.start_potions
        self.alive = True
        self.action = 'Idle'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()   


    


    