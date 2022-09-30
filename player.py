import pygame
import random

# Settings and helper functions
from settings import PLAYER_MAX_HP, PLAYER_START_POTIONS, PLAYER_STRENGTH, GROUND_Y
from helper import draw_health_bar

# Classes
from fighter import Fighter


class Player(Fighter):
    def __init__(self, x, y, name, groups, collision_groups):
        super().__init__(name, groups, collision_groups)

        # Movement
        self.velocity = 6
        self.velocity_y = -20
        self.gravity = 0.8
        self.direction = pygame.math.Vector2(0,0)
        self.faces_right = True

        # Status
        self.is_jumping = False
        self.is_attacking = False
        self.attack_time = 0
        self.attack_cooldown = 400

        # Characteristics
        self.name = name
        self.max_hp = PLAYER_MAX_HP
        self.strength = PLAYER_STRENGTH
        self.start_potions = PLAYER_START_POTIONS 
        self.damage = self.strength + random.randint(-5,5)

        self.hp = self.max_hp
        self.potions = self.start_potions

        # Player location
        self.rect.bottomleft = (x,y)
        self.hitbox = pygame.Rect((self.rect.left + 24, self.rect.top + 50), (42, 75))
        self.attack_rect = pygame.Rect(self.hitbox.left, self.hitbox.top, self.hitbox.width, self.hitbox.height)
        

    def player_input(self, screen):
            keys = pygame.key.get_pressed() 

            if not self.is_attacking:

                if keys[pygame.K_d]:
                    self.direction[0] = 1
                    self.faces_right = True
                    self.run()

                elif keys[pygame.K_q]:
                    self.direction[0] = -1
                    self.faces_right = False
                    self.run()

                else:
                    self.direction[0] = 0

                if keys[pygame.K_p]:
                    self.attack(screen)
                    print('attack')

            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.jump()
                


    def set_status(self):
        if self.direction[1] != 0:
            self.action = 'Run'

        if self.direction[0] != 0:
            self.action = 'Run'
            
        else:
            self.action = 'Idle'

        if self.is_attacking:
            self.action = 'Attack'


    def apply_gravity(self):
        self.direction[1] += self.gravity
        self.hitbox.y += self.direction[1]

         # Check collision with the ground
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False
            self.direction[1] = 0

    def run(self):
        self.hitbox.x += self.direction[0] * self.velocity

        # Check horizontal collisions with enemies
        for sprite in self.collision_groups:
            if sprite.rect.colliderect(self.hitbox):
                if self.direction[0] > 0: # player was moving right
                    self.hitbox.right = sprite.rect.left
                if self.direction[0] < 0: # player was moving left
                    self.hitbox.left = sprite.rect.right

    def jump(self):
        self.is_jumping = True
        self.direction[1] = self.velocity_y



    def attack(self, screen):
        self.is_attacking = True
        self.attack_time = pygame.time.get_ticks()

        for sprite in self.collision_groups:
            if sprite.rect.colliderect(self.attack_rect):
                # Deal damage to the enemy
                sprite.hp -= self.damage
                
                # Check if the target has died
                if sprite.hp < 1:
                    sprite.hp = 0
                    sprite.alive = False
                    sprite.death()

                # Run enemy hurt animation
                else:
                    sprite.hurt()

        pygame.draw.rect(screen, "green", self.attack_rect, 2)

           
    def cooldown(self):
         if pygame.time.get_ticks() - self.attack_time >= self.attack_cooldown:
                self.is_attacking = False


    def animate(self):
        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
            self.frame_index = 0

        image = self.animation_dict[self.action][self.frame_index]

        if self.faces_right:
            self.image = image
            self.rect.left = self.hitbox.left - 24
            self.rect.top = self.hitbox.top - 50
            self.attack_rect.left = self.hitbox.right
            self.attack_rect.top = self.hitbox.top
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.right = self.hitbox.right + 24
            self.rect.top = self.hitbox.top - 50
            self.attack_rect.right = self.hitbox.left
            self.attack_rect.top = self.hitbox.top
            
    

    def draw_health(self, screen):
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp

        # Position the health bar
        self.health_rect = pygame.Rect(0, 0, 100, 8)

        # Draw the health bar on the surface
        draw_health_bar(screen, (15, 15), (200, 15), health_ratio) 

    def update(self, screen):
        self.player_input(screen)
        self.cooldown()
        self.apply_gravity()
        self.set_status()
        self.animate()

   

        



    
    


    