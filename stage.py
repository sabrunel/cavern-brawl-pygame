import pygame
import random

# Settings and helper functions
from settings import *
from helper import draw_text

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

        # Creation time
        self.update_time = pygame.time.get_ticks()

        # Create an instance of each fighter type
        self.hero = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group() 
        self.create_player_character()

        # UI elements
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)

        # Wave control
        self.wave_cooldown = 10000 + random.randint(0,5000)
        self.current_wave = 0
        

    def draw_background(self):
        self.display_surface.blit(self.bg, (0,0))

    def create_player_character(self):
        Player(150, GROUND_Y, 'Hero', [self.hero], self.enemies)

    def create_enemies(self):

        if pygame.time.get_ticks() - self.update_time > self.wave_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.current_wave += 1

            for x in range(1,4):
                y = random.randint(100,300)
                enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
                start_position = random.choice([WIDTH + x * y, -x * y])
                Enemy(start_position, GROUND_Y, enemy_name, [self.enemies], self.hero)
        

    def update(self):
        self.hero.update(self.display_surface)
        self.enemies.update()
       

    def draw(self):
        # Draw UI elements
        draw_text(self.display_surface, f'Current wave: {self.current_wave}', self.text, TEXT_COLOR, 770, 15)


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
        self.create_enemies()
        self.update()
        self.draw()





