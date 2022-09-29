import pygame
import random
from fighter import Fighter, draw_health_bar
from settings import enemy_info

class Enemy(Fighter):
    def __init__(self, x, y, name, groups, collision_groups):
        super().__init__(name, groups, collision_groups)

        # Movement
        self.speed = 6
        self.direction = pygame.math.Vector2(0,0)

       # Characteristics
        self.name = name 
        self.strength = enemy_info[self.name]["strength"]
        self.max_hp = enemy_info[self.name]["max_hp"]
        self.damage = self.strength + random.randint(-4,4)
        self.hp = self.max_hp

       # Enemy location
        self.rect.topleft = (x,y)

    def move(self):
        if self.direction[0] != 0:
            self.action = 'Run'
            self.rect.x += self.direction[0] * self.speed
        else:
            self.action = 'Idle'

    def animate(self):
        animation_cd = 80

        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
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
            self.move()
            self.animate()