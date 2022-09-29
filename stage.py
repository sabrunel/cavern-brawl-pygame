import pygame
from settings import *
from player import Player
from enemy import Enemy
from combattext import CombatText
from button import Button
import random


# Helper functions
def draw_text(screen, text, font, text_color, x, y):
    """ 
    This function draws an input text to the screen
    """
    img = font.render(text, False, text_color)
    screen.blit(img, (x, y))

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

        Player(150, 350, 'Hero', [self.hero], self.enemies)
        
        for x in enemy_x_pos:
            enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
            Enemy(x, 350, enemy_name, [self.enemies], self.hero)
        

    def update(self):
        self.hero.update()
        self.enemies.update()
       

    def draw(self):
        # Draw fighters
        self.hero.draw(self.display_surface)
        self.enemies.draw(self.display_surface)

        # Draw health bars
        self.hero.sprite.draw_health(self.display_surface)
        for enemy in self.enemies.sprites():
            enemy.draw_health(self.display_surface)

        # Draw potion button
        self.potion_btn.draw()
        draw_text(self.display_surface, str(self.hero.sprite.potions), self.text, TEXT_COLOR, 55, 45)
     

    def run(self):
        self.draw_background()
        self.update()
        self.draw()





