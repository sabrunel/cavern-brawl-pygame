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
        self.bg = pygame.image.load('assets/Background.png').convert_alpha()

        # Sprite group setup
        self.active_sprites = pygame.sprite.Group()

        # Create an instance of each fighter type
        self.hero = Player(150, 350, 'Hero', [self.active_sprites])
        self.pick_enemies()

        # UI elements
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()
        self.potion_btn = Button(self.display_surface, 15, 45, potion_img, 40, 40)
        
        # Turn attributes
        self.current_turn = 1
        self.total_fighters = len(self.active_sprites)
        self.action_wait = 0
        self.action_cooldown = 90

        # Player input
        self.player_clicked = False 

        # Stage states
        self.outcome = 0 # 0: game playing, -1: defeat, 1: victory
        self.is_attacking = False
        self.is_using_potion = False
        self.target = None

    def draw_background(self):
        self.display_surface.blit(self.bg, (0,0)) 

    def pick_enemies(self):
        self.enemy_list = []

        for x in enemy_x_pos:
            enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
            enemy = Enemy(x, 350, enemy_name, [self.active_sprites])
            self.enemy_list.append(enemy)

    def player_action(self):
        # Target an enemy to attack it
        for index, enemy in enumerate(self.enemy_list):
            if enemy.rect.collidepoint(pygame.mouse.get_pos()): #  Checks where the mouse is
                if self.player_clicked and enemy.alive:
                    self.is_attacking = True
                    self.target = self.enemy_list[index]

        # Click the potion button
        if self.potion_btn.draw():
            self.is_using_potion = True

    def hero_action(self):
        if self.hero.alive:
            if self.current_turn == 1:
                self.action_wait += 1
                if self.action_wait >= self.action_cooldown:
                    
                    # Attack
                    if self.is_attacking == True and self.target != None:
                        self.hero.attack(self.target)
                        self.current_turn += 1
                        self.action_wait = 0

                        # Create the damage text
                        CombatText(self.target.rect.centerx, self.target.rect.y, [self.active_sprites], self.text,  str(self.hero.damage), HEALTH_RED) 

                    # Use potion
                    if self.is_using_potion == True:
                        if self.hero.potions > 0:
                            if self.hero.max_hp - self.hero.hp > POTION_EFFECT:
                                heal_amount = POTION_EFFECT

                            else:
                                heal_amount = self.hero.max_hp - self.hero.hp

                            self.hero.hp += heal_amount
                            self.hero.potions -= 1

                            # Create the healing text
                            CombatText(self.hero.rect.centerx, self.hero.rect.y, [self.active_sprites], self.text,  str(heal_amount), HEALTH_GREEN)

                            self.current_turn += 1
                            self.action_wait = 0

        else:
            self.outcome = -1
            self.player_clicked = False    


    def enemy_action(self):
        for index, enemy in enumerate(self.enemy_list):
            if self.current_turn == 2 + index:
                if enemy.alive:
                    self.action_wait += 1
                    if self.action_wait >= self.action_cooldown:

                        # Health check (to use potion)
                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                            if enemy.max_hp - enemy.hp > POTION_EFFECT:
                                heal_amount = POTION_EFFECT

                            else:
                                heal_amount = enemy.max_hp - enemy.hp

                            enemy.hp += heal_amount
                            enemy.potions -= 1
                            self.current_turn += 1
                            self.action_wait = 0 

                            # Create the healing text
                            CombatText(enemy.rect.centerx, enemy.rect.y,  [self.active_sprites], self.text, str(heal_amount), HEALTH_GREEN)

                        # Bandit attack
                        else:
                            enemy.attack(self.hero)
                            self.current_turn += 1
                            self.action_wait = 0       

                            # Create the damage text
                            CombatText(self.hero.rect.centerx, self.hero.rect.y, [self.active_sprites], self.text, str(enemy.damage), HEALTH_RED)
                                            


                else:
                    self.current_turn += 1 #skips a dead enemy

    
    def end_turn(self):
        if self.current_turn > self.total_fighters:
            self.current_turn = 1

        # Check whether all enemies are dead
        alive_enemies = 0
        for enemy in self.enemy_list:
            if enemy.alive:
                alive_enemies += 1

        if alive_enemies == 0:
            self.outcome = 1
            self.player_clicked = False


    def end_combat(self):
        if self.outcome != 0:
            draw_text(self.display_surface,'Click to start again', self.text, TEXT_COLOR, 290, 180)
            if self.outcome == -1:
                draw_text(self.display_surface,'DEFEAT', self.title, HEALTH_RED, 260, 100)

            if self.outcome == 1:
                draw_text(self.display_surface,'VICTORY', self.title, HEALTH_GREEN, 240, 100)
            

    def reset_stage(self):
        if self.outcome != 0 and self.player_clicked:
            self.outcome = 0
            self.current_turn = 1

            # Reset the player character
            self.hero.reset()

            # Make sure to remove any remaining enemy before picking a new combination
            for enemy in self.enemy_list:
                enemy.kill()

            # Select new enemies
            self.pick_enemies()

            # Reset stage state
            self.is_attacking = False
            self.is_using_potion = False
            self.target = None

    def update(self):
        if self.outcome == 0:
            # Reset action variables
            self.is_attacking = False
            self.is_using_potion = False
            self.target = None

            self.player_action()
            self.hero_action()
            self.enemy_action()
            self.end_turn()
        
        self.active_sprites.update()
        self.end_combat()
        self.reset_stage()

    def draw(self):
        # Draw visible sprites
        self.active_sprites.draw(self.display_surface)

        # Draw health bars
        self.hero.draw_health(self.display_surface)
        for enemy in self.enemy_list:
            enemy.draw_health(self.display_surface)

        # Draw potion button
        self.potion_btn.draw()
        draw_text(self.display_surface, str(self.hero.potions), self.text, TEXT_COLOR, 55, 45)

    def run(self):
        self.draw_background()
        self.update()
        self.draw()





