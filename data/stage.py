import pygame
import random

# Settings and helper functions
from .settings import *
from .helper import draw_text

# Classes
from .player import Player
from .enemy import Enemy, Bat
from .collectible import Collectible
from .projectile import Dagger, Orb
from .combattext import CombatText
from .particles import Particle


class Stage():
    """ Class that handles player input and contains the game logic """

    def __init__(self):
        # Stage setup
        self.display_surface = pygame.display.get_surface()

        self.bg_img_list = []
        for i in range(1,3):
            img = pygame.image.load(GRAPHICS_DIR + f'background/bg{i}.png').convert_alpha()
            img_scale = pygame.transform.scale(img,(img.get_width() * 2, img.get_height() * 2))
            self.bg_img_list.append(img_scale)

        fg_img = pygame.image.load(GRAPHICS_DIR + 'background/fg.png').convert_alpha()
        self.fg_img = pygame.transform.scale(fg_img,(fg_img.get_width() * 2, fg_img.get_height() * 2))
        self.scroll = 150

        # Creation time
        self.update_time = pygame.time.get_ticks()

        # Sprite groups setup
        self.active_sprites = pygame.sprite.Group()
        self.hero_sprite = pygame.sprite.GroupSingle()
        self.attackable_sprites = pygame.sprite.Group() 
        self.collectible_sprites = pygame.sprite.Group()
        self.player_projectile_sprites = pygame.sprite.Group()
        self.enemy_projectile_sprites = pygame.sprite.Group()
        self.ranged_enemy_sprites = pygame.sprite.Group()
        self.melee_enemy_sprites = pygame.sprite.Group()
        self.create_player_character()

        # UI elements
        self.text = pygame.font.Font(FONTS_DIR + FONT_NAME, FONT_SIZE)
        self.title = pygame.font.Font(FONTS_DIR + FONT_NAME, TITLE_SIZE)

        # Wave control
        self.wave_cooldown = 8000 + random.randint(0,8000)

        # Stage status
        self.current_wave = 0
        self.killed_enemies = 0
        self.best_score = 0
        self.status = 'Idle'

        # Stage variables 
        self.pickup_collectible_time = 0
        self.pickup_collectible_cooldown = 400
        self.hero_attack_cooldown = 630
        self.enemy_attack_cooldown = 630
        

    def draw_background(self):
        """ Handles the parallax effect with background layers """
        for x in range(2):
            scroll_speed = 1
        
            for img in self.bg_img_list:
                    self.display_surface.blit(img, ((x*img.get_width()) - self.scroll * scroll_speed,0))
                    scroll_speed += 0.5

    def draw_foreground(self):
        """ Draws the static foreground """
        self.display_surface.blit(self.fg_img, (0,0))
        

    def create_player_character(self):
        """ Generates the player character """
        Player(150, GROUND_Y, 'Hero', [self.hero_sprite])
        self.hero = self.hero_sprite.sprite

    def create_wave(self):
        """ Generates a set of random enemies """
        if pygame.time.get_ticks() - self.update_time > self.wave_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.current_wave += 1

            for x in range(1,4):
                y = random.randint(100,300)
                enemy_name = random.choice(["Bat", "Monster", "PlagueDoctor"])
                start_position = random.choice([WIDTH + x * y, -x * y])

                if enemy_name == 'Bat':
                    Bat(start_position, GROUND_Y, enemy_name, [self.attackable_sprites, self.ranged_enemy_sprites], self.hero_sprite)
                
                else:
                    Enemy(start_position, GROUND_Y, enemy_name, [self.attackable_sprites, self.melee_enemy_sprites], self.hero_sprite)

            

    def generate_health(self):
        """ Creates a health collectible with 20 % probability """
        roll = 5
        if random.randint(1,5) == roll:
            Collectible(random.randint(100,WIDTH - 100), random.randint(230,480), 'Health', self.collectible_sprites)
  
    
    def player_input(self):
        """ Handles player input (keys and mouse buttons pressed) """
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed() 

        if self.status != 'Combat':

            if key[pygame.K_RETURN]:
                self.reset_stage()

        if self.status != 'Score':
            if key[pygame.K_d]:
                self.hero.direction[0] = 1
                self.hero.faces_right = True
                self.hero.run()
                        
                if self.scroll < WIDTH and self.hero.hurtbox.right < WIDTH:
                    self.scroll += 1

            elif key[pygame.K_q]:
                self.hero.direction[0] = -1
                self.hero.faces_right = False
                self.hero.run()

                if self.scroll > 0 and self.hero.hurtbox.left > 0:
                    self.scroll -= 1

            else:
                self.hero.direction[0] = 0

            if mouse[0] and not self.hero.attacking_melee:
                self.hero.attack_choice = random.choice(['Attack', 'Attack2','Attack3'])
                self.hero.melee_attack()

            if mouse[2] and not self.hero.attacking_range:
                self.hero.ranged_attack()
                Dagger(self.hero.hurtbox.centerx, self.hero.hurtbox.centery, 'Dagger', self.player_projectile_sprites, self.hero.faces_right)

            if key[pygame.K_SPACE] and not self.hero.jumping: 
                self.hero.jump()


    def player_actions(self):
        """ Handles player combat logic """
        if self.hero.alive:

            # Is hit by an enemy projectile
            for enemy in self.ranged_enemy_sprites.sprites():
                for projectile in self.enemy_projectile_sprites.sprites():
                    if projectile.rect.colliderect(self.hero.hurtbox):
                        self.enemy_hits_player(enemy)
                        self.enemy_projectile_sprites.remove(projectile)

            # Attacks
            for enemy in self.attackable_sprites.sprites():
                if self.hero.attacking_melee and not enemy.hit:
                    if self.hero.hitbox.colliderect(enemy.hurtbox):
                        enemy.hurtbox.x -= enemy.direction[0] * 30 # adds a little push back
                        self.player_hits_enemy(enemy)
                                 

            # Picks up collectible
            if self.hero.can_pick_collectible:
                for sprite in self.collectible_sprites.sprites():
                    if sprite.rect.colliderect(self.hero.hurtbox):
                        self.player_picks_collectible(sprite)
                        self.pickup_collectible_time = pygame.time.get_ticks()
                        self.hero.can_pick_collectible = False

                
    def enemy_actions(self):
        """ Handles enemy combat logic """
        for enemy in self.attackable_sprites.sprites():
            if enemy.alive:
                # Is hit by a player projectile
                for projectile in self.player_projectile_sprites:
                    if projectile.rect.colliderect(enemy.hurtbox) and not enemy.hit:
                        self.player_hits_enemy(enemy)
                        Particle(enemy.hurtbox.centerx, enemy.hurtbox.centery, 'RangedAttack', self.active_sprites)
                        self.player_projectile_sprites.remove(projectile)

                # Attacks within melee range
                if enemy.hitbox.colliderect(self.hero.hurtbox):
                    if enemy.alive and enemy.can_attack:
                        enemy.melee_attack()    
                    
                    if pygame.time.get_ticks() - enemy.attack_time > enemy.damage_cooldown and enemy.attacking:
                        self.enemy_hits_player(enemy)
                        enemy.attack_time = 0      
                
        # Drops an orb
        for enemy in self.ranged_enemy_sprites.sprites():
            if enemy.alive and enemy.can_shoot:
                Orb(enemy.hurtbox.left, enemy.hurtbox.top, 'Orb', self.enemy_projectile_sprites)
                enemy.can_shoot = False


    def player_hits_enemy(self, enemy):
        """ Handles damages dealt to enemies by the player and associated effects """
        enemy.hit = True
        enemy.hp -= self.hero.damage

        # Check if the target has died
        if enemy.hp < 1:
            enemy.hp = 0
            enemy.alive = False
            enemy.death()
            self.generate_health()

            # Update score
            self.killed_enemies += 1

        else:
            enemy.hurt()

            if self.hero.attacking_range:
                Particle(enemy.hurtbox.centerx, enemy.hurtbox.centery, 'RangedAttack', self.active_sprites)
            elif self.hero.attacking_melee:
                Particle(enemy.hurtbox.centerx, enemy.hurtbox.centery, 'Attack', self.active_sprites)
            
            CombatText(enemy.rect.centerx, enemy.rect.y, self.active_sprites, self.text, str(self.hero.damage), HEALTH_RED)

    def enemy_hits_player(self,enemy):
        """ Handles damages dealt to the player by enemies and associated effects """
        self.hero.hit = True
        self.hero.hp -= enemy.damage

        # Check if the player has died
        if self.hero.hp <= 0:
            self.hero.death()
            self.hero.alive = False

            # Display score screen
            self.status = 'Score'
            self.update_max_score()

        else:
            self.hero.hurt()
            Particle(self.hero.hurtbox.centerx, self.hero.hurtbox.centery, 'Attack', self.active_sprites)
            CombatText(self.hero.rect.centerx, self.hero.rect.y, self.active_sprites, self.text, str(enemy.damage), HEALTH_RED)

    def player_picks_collectible(self, collectible):
        """ Handles player collisions with collectibles """
        # Health check (to use collectible)
        if self.hero.max_hp - self.hero.hp > HEAL_EFFECT:
            heal_amount = HEAL_EFFECT

        else:
            heal_amount = self.hero.max_hp - self.hero.hp

        self.hero.hp += heal_amount
        self.collectible_sprites.remove(collectible)

        CombatText(self.hero.rect.centerx, self.hero.rect.y, self.active_sprites, self.text, str(heal_amount), HEALTH_GREEN)

    def clean_projectiles(self):
        """ Clears all projectiles upon reaching the edge of the screen """
        # Player projectiles
        for projectile in self.player_projectile_sprites:
            if projectile.rect.x > WIDTH or projectile.rect.x < 0:
                self.player_projectile_sprites.remove(projectile)

        # Enemy projectiles
        for projectile in self.enemy_projectile_sprites:
            if projectile.rect.y > HEIGHT:
                self.enemy_projectile_sprites.remove(projectile)

    def cooldowns(self):
        """ Handles cooldowns on various actions """
        # Player attack
        if pygame.time.get_ticks() - self.hero.attack_time >= self.hero_attack_cooldown:
            self.hero.attacking_melee = False
            self.hero.attacking_range = False

        # Collectible pick up
        if pygame.time.get_ticks() - self.pickup_collectible_time >= self.pickup_collectible_cooldown:
            self.hero.can_pick_collectible = True

        # Enemy attack
        for enemy in self.attackable_sprites.sprites():
            if pygame.time.get_ticks() - enemy.attack_time >= self.enemy_attack_cooldown:
                enemy.attacking = False
                enemy.can_attack = True


    def update_max_score(self):
        """ Updates the score board when the player reaches a higher score """
        if self.killed_enemies >= self.best_score:
            self.best_score = self.killed_enemies

    def stage_status(self):
        """ Updates the score board when the player reaches a higher score """
        if self.status != 'Combat':
            draw_text(self.display_surface,'Press enter to start', self.text, TEXT_COLOR, 360, 180)

            if self.status == 'Idle':
                draw_text(self.display_surface,'JOIN THE BRAWL', self.title, HEALTH_GREEN, 160, 100)

            if self.status == 'Score':
                draw_text(self.display_surface,'YOU DIED', self.title, HEALTH_RED, 300, 100)
                draw_text(self.display_surface, f'Score: {self.killed_enemies}', self.text, TEXT_COLOR, 420, 50)
        
    def reset_stage(self):
        """ Clears the stage and resets it """
        # Reset stage state
        self.status = 'Combat'
        self.current_wave = 0
        self.killed_enemies = 0

        # Reset the player character
        self.create_player_character()

        # Make sure to remove any remaining enemy before creating a new wave
        for enemy in self.attackable_sprites.sprites():
            self.attackable_sprites.remove(enemy)

        # Clear any projectile remaining on the screen
        self.clean_projectiles()

                
    def update(self):
        """ Updates the game """
        self.player_actions()

        if self.status == 'Combat':
            self.create_wave()
            self.enemy_actions()  

        self.cooldowns()
        self.clean_projectiles()
        self.hero_sprite.update()
        self.attackable_sprites.update()
        self.collectible_sprites.update()
        self.player_projectile_sprites.update()
        self.enemy_projectile_sprites.update()
        self.active_sprites.update()
        self.stage_status()

       
    def draw(self):
        """ Draws the elements of the game by order of appearance """
        # Draw UI elements
        if self.status == 'Combat':
            draw_text(self.display_surface, f'Current wave: {self.current_wave}', self.text, TEXT_COLOR, 730, 15)
            draw_text(self.display_surface, f'Enemies killed: {self.killed_enemies}', self.text, TEXT_COLOR, 730, 45)
            draw_text(self.display_surface, f'Best score: {self.best_score}', self.text, TEXT_COLOR, 730, 75)
            self.hero.draw_health(self.display_surface)

        # Draw collectibles
        self.collectible_sprites.draw(self.display_surface)

        # Draw fighters
        self.attackable_sprites.draw(self.display_surface)
        for enemy in self.attackable_sprites.sprites():
            enemy.draw_health(self.display_surface)

        self.hero_sprite.draw(self.display_surface)

        # Draw projectiles
        self.player_projectile_sprites.draw(self.display_surface)
        self.enemy_projectile_sprites.draw(self.display_surface)

        # Draw other active sprites (combat text, particles)
        self.active_sprites.draw(self.display_surface)

        # Draw collisionboxes
        # pygame.draw.rect(self.display_surface, "green", self.hero.hurtbox, 2)
        # pygame.draw.rect(self.display_surface, "red", self.hero.hitbox, 2)
        # for enemy in self.attackable_sprites.sprites():
            # pygame.draw.rect(self.display_surface, "green", enemy.hurtbox, 2)
            # pygame.draw.rect(self.display_surface, "red", enemy.hitbox, 2)
           

    def run(self):
        """ Runs the combat """
        self.player_input()
        self.draw_background()
        self.draw_foreground()
        self.update()
        self.draw()





