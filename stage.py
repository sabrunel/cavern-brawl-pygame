import pygame
from settings import *
from fighter import Fighter
from healthbar import HealthBar
from combattext import CombatText
from button import Button


# Helper functions
def draw_text(screen, text, font, text_color, x, y):
    img = font.render(text, False, text_color)
    screen.blit(img, (x, y))

# Main class
class Stage():
    def __init__(self):

        # Stage setup
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('assets/Background.png').convert_alpha()
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)

        # Stage elements
        self.create_fighters()
        self.create_healthbars()
        self.combat_text_group = pygame.sprite.Group()
        potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()
        self.potion_btn = Button(self.display_surface, 10, 400, potion_img, 40, 40)
        
        # Turn attributes
        self.current_turn = 1
        self.total_fighters = len(self.enemy_list) + 1
        self.action_cd = 0
        self.action_wait_time = 90
        self.potion_effect = 15

        # Player input
        self.player_clicked = False # User input

        # Stage states
        self.outcome = 0 # 0: game playing, -1: defeat, 1: victory
        self.is_attacking = False
        self.is_using_potion = False
        self.target = None

    def create_fighters(self):
        #Create an instance of each fighter type
        self.hero = Fighter(200, 350, 'Hero', 8, 30, 3)
        self.bat = Fighter(450, 320, 'Bat', 4, 15, 2)
        self.plaguedoctor = Fighter(600, 350,'PlagueDoctor', 5, 20, 2)

        # Add enemies to a list
        self.enemy_list = []
        self.enemy_list.append(self.bat)
        self.enemy_list.append(self.plaguedoctor)

    def draw_names(self):
        # Draw hero name
        draw_text(self.display_surface,f'{self.hero.name}', self.text, TEXT_COLOR, 10, 10)

        # Draw enemy names
        for count, enemy in enumerate(self.enemy_list):
            draw_text(self.display_surface,f'{enemy.name}', self.text, TEXT_COLOR, 640, 10 + count * 50)

    def create_healthbars(self):
        self.hero_healthbar = HealthBar( 10, 30, self.hero.hp, self.hero.max_hp)
        self.bat_healthbar = HealthBar(640, 30, self.bat.hp, self.bat.max_hp)
        self.plaguedoctor_healthbar = HealthBar(640, 80, self.plaguedoctor.hp, self.plaguedoctor.max_hp)  

    def player_input(self, bool):
            # Listen for mouse click
            self.player_clicked = bool

    def set_potion(self):
        if self.potion_btn.draw():
            self.is_using_potion = True

    def set_target(self):
        # Check where the mouse is
        pos = pygame.mouse.get_pos()
    
        # Target enemies to attack them
        for index, enemy in enumerate(self.enemy_list):
            if enemy.rect.collidepoint(pos):
                #pygame.mouse.set_visible(False)
                #screen.blit(sword_img, pos)
                if self.player_clicked and enemy.alive:
                    self.is_attacking = True
                    self.target = self.enemy_list[index]

    def player_actions(self):
        # Player action
        if self.hero.alive:
            if self.current_turn == 1:
                self.action_cd += 1
                if self.action_cd >= self.action_wait_time:
                    # Look for a player action
                    
                    # Attack
                    if self.is_attacking == True and self.target != None:
                        self.hero.attack(self.target)
                        self.current_turn += 1
                        self.action_cd = 0

                        # Create the damage text
                        dmg_txt = CombatText(self.target.rect.centerx, self.target.rect.y, self.text,  str(self.hero.damage), HEALTH_RED)
                        self.combat_text_group.add(dmg_txt)  

                    # Use potion
                    if self.is_using_potion == True:
                        if self.hero.potions > 0:
                            if self.hero.max_hp - self.hero.hp > self.potion_effect:
                                heal_amount = self.potion_effect

                            else:
                                heal_amount = self.hero.max_hp - self.hero.hp

                            self.hero.hp += heal_amount
                            self.hero.potions -= 1

                            # Create the healing text
                            heal_txt = CombatText(self.hero.rect.centerx, self.hero.rect.y, self.text,  str(heal_amount), HEALTH_GREEN)
                            self.combat_text_group.add(heal_txt)

                            self.current_turn += 1
                            self.action_cd = 0

        else:
            self.outcome = -1
            self.player_clicked = False    


    def enemy_actions(self):
        for index, enemy in enumerate(self.enemy_list):
            if self.current_turn == 2 + index:
                if enemy.alive:
                    self.action_cd += 1
                    if self.action_cd >= self.action_wait_time:
                        # Health check (to use potion)
                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                            if enemy.max_hp - enemy.hp > self.potion_effect:
                                heal_amount = self.potion_effect

                            else:
                                heal_amount = enemy.max_hp - enemy.hp

                            enemy.hp += heal_amount
                            enemy.potions -= 1
                            self.current_turn += 1
                            self.action_cd = 0 

                            # Create the healing text
                            heal_txt = CombatText(enemy.rect.centerx, enemy.rect.y,  self.text, str(heal_amount), HEALTH_GREEN)
                            self.combat_text_group.add(heal_txt)

                        # Bandit attack
                        else:
                            enemy.attack(self.hero)
                            self.current_turn += 1
                            self.action_cd = 0       

                            # Create the damage text
                            dmg_txt = CombatText(self.hero.rect.centerx, self.hero.rect.y, self.text, str(enemy.damage), HEALTH_RED)
                            self.combat_text_group.add(dmg_txt)                 


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

            # Reset characters
            self.hero.reset()
            self.bat.reset()
            self.plaguedoctor.reset()

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

            self.set_potion()
            self.set_target()
            self.player_actions()
            self.enemy_actions()
            self.end_turn()

        self.end_combat()
        self.hero.update()
        for enemy in self.enemy_list:
            enemy.update()
        self.combat_text_group.update()
        self.reset_stage()

    def draw(self):
        # Draw fighters
        self.hero.draw(self.display_surface)

        for enemy in self.enemy_list:
            enemy.draw(self.display_surface)

        # Draw fighter names
        self.draw_names()

        # Draw healthbars
        self.hero_healthbar.draw(self.hero.hp)
        self.bat_healthbar.draw(self.bat.hp)
        self.plaguedoctor_healthbar.draw(self.plaguedoctor.hp)

        # Draw combat text
        self.combat_text_group.draw(self.display_surface)

        # Draw potion button
        self.potion_btn.draw()
        draw_text(self.display_surface, str(self.hero.potions), self.text, TEXT_COLOR, 55, 400)




