import pygame
import random

# Settings and helper functions
from settings import enemy_info
from helper import draw_health_bar

# Classes
from fighter import Fighter

class Enemy(Fighter):
    def __init__(self, x, y, name, groups, collision_groups):
        super().__init__(name, groups, collision_groups)

        # Movement
        self.velocity = 6
        self.direction = pygame.math.Vector2(0,0)

       # Characteristics
        self.name = name 
        self.strength = enemy_info[self.name]["strength"]
        self.max_hp = enemy_info[self.name]["max_hp"]
        self.damage = self.strength + random.randint(-4,4)
        self.hp = self.max_hp

       # Enemy location
        self.rect.bottomleft = (x,y)


    def animate(self):
        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
            if self.action == 'Death':
                self.frame_index = len(self.animation_dict[self.action]) - 1
            else:
                self.action = 'Idle'
                self.frame_index = 0

        self.image = self.animation_dict[self.action][self.frame_index]

    def draw_health(self, screen):
        if self.hp > 0:
            health_ratio = self.hp / self.max_hp

            # Draw a rectangle with the desired dimensions for the healh tbar
            self.health_rect = pygame.Rect(0, 0, 100, 8)
            self.health_rect.midbottom = self.rect.centerx, self.rect.bottom + 10

            # Draw the health bar on the surface
            draw_health_bar(screen, self.health_rect.bottomleft, self.health_rect.size, health_ratio)
        
        else:
            # Trick to hide the health bar upon enemy death
            draw_health_bar(screen, self.health_rect.bottomleft, (0,0), 0)


    def update(self):
            self.animate()