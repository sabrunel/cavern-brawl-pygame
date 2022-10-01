import pygame
import random

# Settings and helper functions
from settings import *

# Classes
from player import Player
from enemy import Enemy


# Main class
class Stage():
    def __init__(self):

        # Stage setup
        self.display_surface = pygame.display.get_surface()
        bg_img = pygame.image.load('assets/bg.png').convert_alpha()
        self.bg = pygame.transform.scale(bg_img,(bg_img.get_width() * 2, bg_img.get_height() * 2))

        # Create an instance of each fighter type
        self.create_fighters()

        # UI elements
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        

    def draw_background(self):
        self.display_surface.blit(self.bg, (0,0)) 

    def create_fighters(self):
        self.hero = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()

        Player(150, GROUND_Y, 'Hero', [self.hero], self.enemies)
        
        for x in range(1,4):
            enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
            start_position = random.choice([WIDTH + x, -x])
            Enemy(start_position, GROUND_Y, enemy_name, [self.enemies], self.hero)
        

    def update(self):
        self.hero.update(self.display_surface)
        self.enemies.update()
       

    def draw(self):
        # Draw UI elements
        self.hero.sprite.draw_health(self.display_surface)
        for enemy in self.enemies.sprites():
            enemy.draw_health(self.display_surface)

        # Draw fighters
        self.enemies.draw(self.display_surface)
        self.hero.draw(self.display_surface)
     
        # Draw hitboxes
        #pygame.draw.rect(self.display_surface, "red", self.hero.sprite.hitbox, 2)
        #for enemy in self.enemies.sprites():
        #   pygame.draw.rect(self.display_surface, "red", enemy.hitbox, 2)

        



    def run(self):
        self.draw_background()
        self.update()
        self.draw()





