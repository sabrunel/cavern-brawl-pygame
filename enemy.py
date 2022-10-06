import pygame
import random

# Settings and helper functions
from settings import enemy_info
from helper import draw_health_bar

# Classes
from fighter import Fighter

class Enemy(Fighter):
    def __init__(self, x, y, name, groups, attackable_sprites):
        super().__init__(name, groups, attackable_sprites)


       # Characteristics
        self.name = name 
        self.strength = enemy_info[self.name]["strength"]
        self.max_hp = enemy_info[self.name]["max_hp"]
        self.hp = self.max_hp
        self.damage = self.strength + random.randint(-2,2)
        
        # Movement
        self.velocity = enemy_info[self.name]["velocity"]
        self.direction = pygame.math.Vector2(0,0)

        # Position and hitbox
        self.start_pos = (x, y + enemy_info[self.name]["y_offset"])
        self.rect.bottomleft = self.start_pos
        self.hitbox = pygame.Rect((self.rect.left + enemy_info[self.name]["hitbox_left_offset"], self.rect.top + enemy_info[self.name]["hitbox_top_offset"]),enemy_info[self.name]["hitbox_size"])
        self.player = attackable_sprites.sprite

        # Status
        self.can_attack = True
        self.attack_time = 0
        self.attacking = False
        self.hit = False


    def set_status(self):
        if self.alive and not self.hit:             
            if self.direction[0] != 0 and not self.attacking:
                self.action = 'Run'

            else:
                self.action = 'Idle'
            
            if self.can_attack and self.attacking:
                self.action = 'Attack'

       
    def run(self):
        self.hitbox.x += self.direction[0] * self.velocity
    
    def attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking = True
        self.can_attack = False

    def check_direction(self): # enemies will move towards the player character
        if self.hitbox.left > self.player.hitbox.right:
            self.direction[0] = -1
            self.faces_right = False

        elif self.hitbox.right < self.player.hitbox.left:
            self.direction[0] = 1
            self.faces_right = True
        
        else:
            self.direction[0] = 0


    def animate(self):
        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
            if self.action == 'Death':
                self.frame_index = len(self.animation_dict[self.action]) - 1
                self.rect.size = (0,0)
                self.hitbox.size = (0,0)

            elif self.action == 'Hurt':
                self.hit = False
                self.frame_index = 0

            elif self.action == 'Attack':
                self.attacking = False
                self.frame_index = 0

            else:
                self.frame_index = 0

        image = self.animation_dict[self.action][self.frame_index]

        if self.faces_right:
            self.image = image
            self.rect.left = self.hitbox.left - enemy_info[self.name]["hitbox_left_offset"]
            self.rect.top = self.hitbox.top  - enemy_info[self.name]["hitbox_top_offset"]
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.right = self.hitbox.right + enemy_info[self.name]["hitbox_left_offset"]
            self.rect.top = self.hitbox.top - enemy_info[self.name]["hitbox_top_offset"]

    def draw_health(self, screen):
        if self.hp > 0:
            health_ratio = self.hp / self.max_hp

            # Draw a rectangle with the desired dimensions for the healh tbar
            self.health_rect = pygame.Rect(0, 0, 50, 10)
            self.health_rect.midbottom = self.hitbox.centerx, self.rect.bottom + 10

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