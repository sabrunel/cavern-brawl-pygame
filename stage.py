import pygame
import random

# Settings and helper functions
from settings import *
from helper import draw_text

# Classes
from player import Player
from enemy import Enemy
from collectible import Collectible
from combattext import CombatText


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
        self.attackable_sprites = pygame.sprite.Group() 
        self.collectible_sprites = pygame.sprite.Group()
        self.create_player_character()
        self.active_sprites = pygame.sprite.Group()

        # UI elements
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)

        # Wave control
        self.wave_cooldown = 8000 + random.randint(0,8000)
        self.current_wave = 0
        self.killed_enemies = 0

        # Attack status
        self.attack_time = 0
        self.attack_cooldown = 400
        self.pickup_collectible_time = 0
        self.pickup_collectible_cooldown = 400
        

    def draw_background(self):
        self.display_surface.blit(self.bg, (0,0))

    def create_player_character(self):
        Player(150, GROUND_Y, 'Hero', [self.hero], self.attackable_sprites, self.collectible_sprites)

    def create_wave(self):
        if pygame.time.get_ticks() - self.update_time > self.wave_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.current_wave += 1

            for x in range(1,4):
                y = random.randint(100,300)
                enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
                start_position = random.choice([WIDTH + x * y, -x * y])
                Enemy(start_position, GROUND_Y, enemy_name, [self.attackable_sprites], self.hero)
            
            Collectible(random.randint(100,WIDTH - 100), random.randint(230,480), self.collectible_sprites, self.hero)
            
    def player_actions(self): 
        hero = self.hero.sprite

        if hero.alive:
            # Attack
            for sprite in self.attackable_sprites:
                if hero.attacking and not sprite.hit:
                    if hero.attack_rect.colliderect(sprite.hitbox):
                        # Deal damage to the enemy
                        sprite.hit = True
                        sprite.hp -= hero.damage
                        print('hit')
                        
                        # Check if the target has died
                        if sprite.hp < 1:
                            sprite.hp = 0
                            sprite.alive = False
                            self.killed_enemies += 1
                            sprite.death()

                        # Run enemy hurt animation
                        else:
                            sprite.hurt()

                            # Create the damage text
                            CombatText(sprite.rect.centerx, sprite.rect.y, [self.active_sprites], self.text, str(hero.damage), HEALTH_RED)
                                   
            # Pick up collectible
            if hero.can_pick_collectible:
                for sprite in self.collectible_sprites:
                    if sprite.rect.colliderect(hero.hitbox):
                        print('pickup health')
                        self.pickup_collectible_time = pygame.time.get_ticks()
                        hero.can_pick_collectible = False

                         # Health check (to use collectible)
                        if hero.max_hp - hero.hp > HEAL_EFFECT:
                            heal_amount = HEAL_EFFECT

                        else:
                            heal_amount = hero.max_hp - hero.hp

                        hero.hp += heal_amount
                        sprite.kill()

                        # Create the healing text
                        CombatText(hero.rect.centerx, hero.rect.y, [self.active_sprites], self.text, str(heal_amount), HEALTH_GREEN)
                                 

    def cooldowns(self):
        hero = self.hero.sprite
        # Attack cooldown
        if pygame.time.get_ticks() - self.attack_time >= self.attack_cooldown:
            hero.attacking = False

        # Collectible cooldown
        if pygame.time.get_ticks() - self.pickup_collectible_time >= self.pickup_collectible_cooldown:
            hero.can_pick_collectible = True

    def update(self):     
        self.create_wave()
        self.hero.update(self.display_surface)
        self.attackable_sprites.update()
        self.collectible_sprites.update()
        self.active_sprites.update()
        self.player_actions()
        self.cooldowns()
        
       
    def draw(self):
        # Draw UI elements
        draw_text(self.display_surface, f'Current wave: {self.current_wave}', self.text, TEXT_COLOR, 730, 15)
        draw_text(self.display_surface, f'Enemies killed: {self.killed_enemies}', self.text, TEXT_COLOR, 730, 45)

        self.hero.sprite.draw_health(self.display_surface)
        for enemy in self.attackable_sprites.sprites():
            enemy.draw_health(self.display_surface)

        # Draw fighters
        self.attackable_sprites.draw(self.display_surface)
        self.hero.draw(self.display_surface)

        # Draw collectibles
        self.collectible_sprites.draw(self.display_surface)

        # Draw other active sprites
        self.active_sprites.draw(self.display_surface)

        # Draw hitboxes
        #pygame.draw.rect(self.display_surface, "red", self.hero.sprite.hitbox, 2)
        #for enemy in self.attackable_sprites.sprites():
        #   pygame.draw.rect(self.display_surface, "red", enemy.hitbox, 2)

        
    def run(self):
        self.draw_background()
        self.update()
        self.draw()





