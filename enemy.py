import pygame
import random

# Settings and helper functions
from helper import draw_health_bar

# Classes
from fighter import Fighter

class Enemy(Fighter):
    def __init__(self, x, y, name, groups, attackable_sprites):
        super().__init__(x, y, name, groups, attackable_sprites)

       # Characteristics 
        self.hp = self.max_hp
        self.damage = self.strength + random.randint(-2,2)

        # Status
        self.can_attack = True
        self.attacking = False
        self.hit = False

        # Attack cooldowns
        self.attack_time = 0
        self.damage_cooldown = 500

        # Collision sprites
        self.player = attackable_sprites.sprite


    def set_status(self):
        if self.alive and not self.hit:             
            if self.direction[0] != 0 and not self.attacking:
                self.action = 'Run'

            else:
                self.action = 'Idle'
            
            if self.attacking:
                self.action = 'Attack'

       
    def run(self):
        self.hurtbox.x += self.direction[0] * self.velocity
    
    def attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking = True
        self.can_attack = False

    def check_direction(self): # enemies will move towards the player character
        if self.hurtbox.left > self.player.hurtbox.right:
            self.direction[0] = -1
            self.faces_right = False

        elif self.hurtbox.right < self.player.hurtbox.left:
            self.direction[0] = 1
            self.faces_right = True
        
        else:
            self.direction[0] = 0

    def draw_health(self, screen):
        if self.hp > 0:
            health_ratio = self.hp / self.max_hp

            # Draw a rectangle with the desired dimensions for the healh tbar
            self.health_rect = pygame.Rect(0, 0, 50, 10)
            self.health_rect.midbottom = self.hurtbox.centerx, self.rect.bottom + 10

            # Draw the health bar on the surface
            draw_health_bar(screen, self.health_rect.bottomleft, self.health_rect.size, health_ratio)
        
        else:
            # Trick to hide the health bar upon enemy death
            draw_health_bar(screen, self.health_rect.bottomleft, (0,0), 0)


    def update(self):
        self.check_direction()
        self.run()
        self.set_status()
        self.animate()