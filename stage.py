import pygame
import random

# Settings and helper functions
from settings import *
from helper import draw_text

# Classes
from player import Player
from enemy import Enemy
from combattext import CombatText
from button import Button


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
        potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()
        self.potion_btn = Button(self.display_surface, 15, 45, potion_img, 40, 40)
        

    def draw_background(self):
        self.display_surface.blit(self.bg, (0,0)) 

    def create_fighters(self):
        self.hero = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()

        Player(150, GROUND_Y, 'Hero', [self.hero], self.enemies)
        
        for x in enemy_x_pos:
            enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
            Enemy(x, GROUND_Y, enemy_name, [self.enemies], self.hero)
        

    def update(self):
        self.hero.update(self.display_surface)
        self.enemies.update()
       

    def draw(self):
        # Draw UI elements
        self.hero.sprite.draw_health(self.display_surface)
        for enemy in self.enemies.sprites():
            enemy.draw_health(self.display_surface)

        self.potion_btn.draw()
        draw_text(self.display_surface, str(self.hero.sprite.potions), self.text, TEXT_COLOR, 55, 45)

        # Draw fighters
        self.enemies.draw(self.display_surface)
        self.hero.draw(self.display_surface)
     
        # Draw hitboxes
        pygame.draw.rect(self.display_surface, "red", self.hero.sprite.hitbox, 2)
        



    def run(self):
        self.draw_background()
        self.update()
        self.draw()





