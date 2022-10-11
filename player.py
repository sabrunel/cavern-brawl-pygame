import pygame
import random

# Settings and helper functions
from settings import GROUND_Y, WIDTH
from helper import draw_health_bar

# Classes
from fighter import Fighter


class Player(Fighter):
    def __init__(self, x, y, name, groups, attackable_sprites, collectible_sprites):
        super().__init__(x, y, name, groups, attackable_sprites)

        # Characteristics
        self.hp = self.max_hp
        self.damage = self.strength + random.randint(-5,5)

        # Vertical movement
        self.velocity_y = -20
        self.gravity = 0.9

        # Status
        self.jumping = False
        self.attacking = False
        self.can_pick_collectible = True
        self.attack_time = 0
        self.hit = False

        # Collision sprites
        self.collectible_sprites = collectible_sprites
                

    def set_status(self):
        if self.alive and not self.hit:
            if self.direction[1] != 0:
                self.action = 'Jump'

            if self.direction[0] != 0 and not self.jumping: # avoids triggering the running animation while in the air
                self.action = 'Run'

            else:
                self.action = 'Idle'

            if self.attacking:
                self.action = 'Attack'


    def apply_gravity(self):
        self.direction[1] += self.gravity
        self.hurtbox.y += self.direction[1]

         # Check collision with the ground
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.jumping = False
            self.direction[1] = 0

    def run(self):
        self.hurtbox.x += self.direction[0] * self.velocity
        # Make sure the characters stays on the screen
        if self.hurtbox.right >= WIDTH:
          self.hurtbox.right = WIDTH

        if self.hurtbox.left <= 0:
           self.hurtbox.left = 0

    def attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking = True
        

    def jump(self):
        self.jumping = True
        self.direction[1] = self.velocity_y

    def draw_health(self, screen):
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp

        # Position the health bar
        self.health_rect = pygame.Rect(0, 0, 100, 8)

        # Draw the health bar on the surface
        draw_health_bar(screen, (15, 15), (200, 15), health_ratio) 

    def update(self):
        self.apply_gravity()
        self.set_status()
        self.animate()

   

        



    
    


    