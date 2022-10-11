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

        self.bg_img_list = []
        for i in range(1,3):
            img = pygame.image.load(f'assets/background/bg{i}.png').convert_alpha()
            img_scale = pygame.transform.scale(img,(img.get_width() * 2, img.get_height() * 2))
            self.bg_img_list.append(img_scale)

        fg_img = pygame.image.load('assets/background/fg.png').convert_alpha()
        self.fg_img = pygame.transform.scale(fg_img,(fg_img.get_width() * 2, fg_img.get_height() * 2))
        self.scroll = 150

        # Creation time
        self.update_time = pygame.time.get_ticks()

        # Sprite and sprite groups setup
        self.hero_sprite = pygame.sprite.GroupSingle()
        self.attackable_sprites = pygame.sprite.Group() 
        self.collectible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.create_player_character()

        # UI elements
        self.text = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONT_NAME, TITLE_SIZE)

        # Wave control
        self.wave_cooldown = 8000 + random.randint(0,8000)

        # Stage status
        self.current_wave = 0
        self.killed_enemies = 0
        self.status = 'Idle'

        # Stage variables 
        self.pickup_collectible_time = 0
        self.pickup_collectible_cooldown = 400
        self.hero_attack_cooldown = 400
        self.enemy_attack_cooldown = 900
        

    def draw_background(self):
        for x in range(2):
            scroll_speed = 1
        
            for img in self.bg_img_list:
                    self.display_surface.blit(img, ((x*img.get_width()) - self.scroll * scroll_speed,0))
                    scroll_speed += 0.5

    def draw_foreground(self):
        self.display_surface.blit(self.fg_img, (0,0))
        

    def create_player_character(self):
        Player(150, GROUND_Y, 'Hero', [self.hero_sprite], self.attackable_sprites, self.collectible_sprites)
        self.hero = self.hero_sprite.sprite

    def create_wave(self):
        if pygame.time.get_ticks() - self.update_time > self.wave_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.current_wave += 1

            for x in range(1,4):
                y = random.randint(100,300)
                enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
                start_position = random.choice([WIDTH + x * y, -x * y])
                Enemy(start_position, GROUND_Y, enemy_name, [self.attackable_sprites], self.hero_sprite)
            

    def generate_health(self):
        roll = 5

        if random.randint(1,5) == roll:
            Collectible(random.randint(100,WIDTH - 100), random.randint(230,480), self.collectible_sprites, self.hero_sprite)

    def player_input(self):
        keys = pygame.key.get_pressed() 

        if self.status != 'Combat':

            if keys[pygame.K_RETURN]:
                self.reset_stage()

        if self.status != 'Score':
            if keys[pygame.K_d]:
                self.hero.direction[0] = 1
                self.hero.faces_right = True
                self.hero.run()
                        
                if self.scroll < WIDTH and self.hero.hurtbox.right < WIDTH:
                    self.scroll += 1

            elif keys[pygame.K_q]:
                self.hero.direction[0] = -1
                self.hero.faces_right = False
                self.hero.run()

                if self.scroll > 0 and self.hero.hurtbox.left > 0:
                    self.scroll -= 1

            else:
                self.hero.direction[0] = 0

            if keys[pygame.K_p]:
                self.hero.attack()

            if keys[pygame.K_SPACE] and not self.hero.jumping: 
                self.hero.jump()


    def player_actions(self):
        if self.hero.alive:
            # Attack
            for enemy in self.attackable_sprites:
                if self.hero.attacking and not enemy.hit:
                    if self.hero.hitbox.colliderect(enemy.hurtbox):
                       
                        # Deal damage to the enemy
                        enemy.hit = True
                        enemy.hp -= self.hero.damage
                        enemy.hurtbox.x -= enemy.direction[0] * 30 # adds a little push back
                            
                        # Check if the target has died
                        if enemy.hp < 1:
                            enemy.hp = 0
                            enemy.alive = False
                            enemy.death()
                            self.killed_enemies += 1

                            # Generate health (20% chances)
                            self.generate_health()

                        # Run enemy hurt animation
                        else:
                            enemy.hurt()

                            # Create the damage text
                            CombatText(enemy.rect.centerx, enemy.rect.y, [self.active_sprites], self.text, str(self.hero.damage), HEALTH_RED)
                                   
            # Pick up collectible
            if self.hero.can_pick_collectible:
                for sprite in self.collectible_sprites:
                    if sprite.rect.colliderect(self.hero.hurtbox):
                        self.pickup_collectible_time = pygame.time.get_ticks()
                        self.hero.can_pick_collectible = False

                         # Health check (to use collectible)
                        if self.hero.max_hp - self.hero.hp > HEAL_EFFECT:
                            heal_amount = HEAL_EFFECT

                        else:
                            heal_amount = self.hero.max_hp - self.hero.hp

                        self.hero.hp += heal_amount
                        sprite.kill()

                        # Create the healing text
                        CombatText(self.hero.rect.centerx, self.hero.rect.y, [self.active_sprites], self.text, str(heal_amount), HEALTH_GREEN)


    def enemy_actions(self):
        for enemy in self.attackable_sprites.sprites():
            if enemy.hitbox.colliderect(self.hero.hurtbox):
                if enemy.can_attack:
                    enemy.attack()
                
                if pygame.time.get_ticks() - enemy.attack_time > enemy.damage_cooldown and enemy.attacking:
                    # Reset attack time
                    enemy.attack_time = 0
                    # Deal damage to player
                    self.hero.hit = True
                    self.hero.hp -= enemy.damage

                    # Check if the target has died
                    if self.hero.hp <= 0:
                        self.hero.death()
                        self.hero.alive = False
                        self.status = 'Score'

                    # Run enemy hurt animation
                    else:
                        self.hero.hurt()

                        # Create the damage text
                        CombatText(self.hero.rect.centerx, self.hero.rect.y, [self.active_sprites], self.text, str(enemy.damage), HEALTH_RED)

    def cooldowns(self):
        # Player attack cooldown
        if pygame.time.get_ticks() - self.hero.attack_time >= self.hero_attack_cooldown:
            self.hero.attacking = False

        # Collectible cooldown
        if pygame.time.get_ticks() - self.pickup_collectible_time >= self.pickup_collectible_cooldown:
            self.hero.can_pick_collectible = True

        # Enemy attack cooldown
        for enemy in self.attackable_sprites.sprites():
            if pygame.time.get_ticks() - enemy.attack_time >= self.enemy_attack_cooldown:
                enemy.attacking = False
                enemy.can_attack = True


    def stage_status(self):
            if self.status != 'Combat':
                draw_text(self.display_surface,'Press enter to start', self.text, TEXT_COLOR, 360, 180)

                if self.status == 'Idle':
                   draw_text(self.display_surface,'JOIN THE BRAWL', self.title, HEALTH_GREEN, 160, 100)

                if self.status == 'Score':
                    draw_text(self.display_surface,'YOU DIED', self.title, HEALTH_RED, 300, 100)
        
    def reset_stage(self):
        # Reset stage state
        self.status = 'Combat'
        self.current_wave = 0
        self.killed_enemies = 0

        # Reset the player character
        self.create_player_character()

        # Make sure to remove any remaining enemy before creating a new wave
        for enemy in self.attackable_sprites.sprites():
            enemy.kill()

                
    def update(self):

        self.player_actions()

        if self.status == 'Combat':
            self.create_wave()
            self.enemy_actions()  

        self.cooldowns()
        self.hero_sprite.update()
        self.attackable_sprites.update()
        self.collectible_sprites.update()
        self.active_sprites.update()
        self.stage_status()

       
    def draw(self):

        # Draw UI elements
        if self.status == 'Combat':
            draw_text(self.display_surface, f'Current wave: {self.current_wave}', self.text, TEXT_COLOR, 730, 15)
            draw_text(self.display_surface, f'Enemies killed: {self.killed_enemies}', self.text, TEXT_COLOR, 730, 45)
            self.hero.draw_health(self.display_surface)

        # Draw fighters
        self.hero_sprite.draw(self.display_surface)

        self.attackable_sprites.draw(self.display_surface)
        for enemy in self.attackable_sprites.sprites():
            enemy.draw_health(self.display_surface)

        # Draw collectibles
        self.collectible_sprites.draw(self.display_surface)

        # Draw other active sprites
        self.active_sprites.draw(self.display_surface)

        # Draw collisionboxes
        # pygame.draw.rect(self.display_surface, "green", self.hero.hurtbox, 2)
        # pygame.draw.rect(self.display_surface, "red", self.hero.hitbox, 2)
        # for enemy in self.attackable_sprites.sprites():
            # pygame.draw.rect(self.display_surface, "green", enemy.hurtbox, 2)
            # pygame.draw.rect(self.display_surface, "red", enemy.hitbox, 2)
           

        
    def run(self):
        self.player_input()
        self.draw_background()
        self.draw_foreground()
        self.update()
        self.draw()





