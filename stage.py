import pygame
from settings import *
from fighter import Fighter
from healthbar import HealthBar
from button import Button


# Helper functions
def draw_text(screen, text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Main class
class Stage():
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Load images
        self.bg = pygame.image.load('assets/Background.png').convert_alpha()
        potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()

        # Initialize font
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        # Initialize elements
        self.create_fighters()
        self.create_healthbars()
        self.damage_text_group = pygame.sprite.Group()
        self.potion_btn = Button(self.display_surface, 10, 400, potion_img, 40, 40)

    def create_fighters(self):
        #Create an instance of each fighter type
        self.hero = Fighter(200, 350, 'Hero', 30, 3)
        bat = Fighter(500, 320, 'Bat', 15, 3)
        plaguedoctor = Fighter(600, 350, 'PlagueDoctor', 20, 3)

        # Add enemies to a list
        self.enemy_list = []
        self.enemy_list.append(bat)
        self.enemy_list.append(plaguedoctor)

    def draw_names(self):
        # Draw hero name
        draw_text(
            self.display_surface,
            f'{self.hero.name}', 
            self.font, 
            TEXT, 
            10, 
            10
            )

        # Draw enemy names
        for count, enemy in enumerate(self.enemy_list):
            draw_text(
                self.display_surface,
                f'{enemy.name}', 
                self.font, 
                TEXT, 
                640, 
                10 + count * 50
                )

    def create_healthbars(self):
        self.hero_healthbar = HealthBar( 10, 35, self.hero.hp, self.hero.max_hp)

        self.enemy_healthbar_list = []
        for index, enemy in enumerate(self.enemy_list):
            enemy_healthbar = HealthBar(640, 35 + index * 50, enemy.hp, enemy.max_hp ) #Stack healthbars on top of each other
            self.enemy_healthbar_list.append(enemy_healthbar)
    
    def update(self):
        self.hero.update()

        for enemy in self.enemy_list:
            enemy.update()

    def draw(self):
        # Draw fighters
        self.hero.draw(self.display_surface)

        for enemy in self.enemy_list:
            enemy.draw(self.display_surface)

        # Draw fighter names
        self.draw_names()

        # Draw healthbars
        self.hero_healthbar.draw(self.hero_healthbar.hp)

        for enemy_healthbar in self.enemy_healthbar_list:
            enemy_healthbar.draw(enemy_healthbar.hp)

        # Draw button
        self.potion_btn.draw()



