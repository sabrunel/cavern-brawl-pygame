from tkinter import E
import pygame
import random

# Settings and helper functions
from settings import PLAYER_MAX_HP, PLAYER_STRENGTH, GROUND_Y, WIDTH
from helper import draw_health_bar

# Classes
from fighter import Fighter


class Player(Fighter):
    def __init__(self, x, y, name, groups, attackable_sprites, collectible_sprites):
        super().__init__(name, groups, attackable_sprites)

        # Movement
        self.velocity = 6
        self.velocity_y = -20
        self.gravity = 0.9
        self.direction = pygame.math.Vector2(0,0)
        self.faces_right = True

        # Status
        self.jumping = False
        self.attacking = False
        self.can_pick_collectible = True
        

        # Characteristics
        self.name = name
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.strength = PLAYER_STRENGTH
        self.damage = self.strength + random.randint(-5,5)

        # Player location
        self.rect.bottomleft = (x,y)
        self.hitbox = pygame.Rect((self.rect.left + 24, self.rect.top + 50), (42, 75))
        self.attack_rect = pygame.Rect(self.hitbox.left, self.hitbox.top, self.hitbox.width * 2, self.hitbox.height)
        
        # Progress
        self.collectible_sprites = collectible_sprites
        self.killed_enemies = 0

    def player_input(self, screen):
            keys = pygame.key.get_pressed() 

            if not self.attacking:

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
                    self.attack()


            if keys[pygame.K_SPACE] and not self.jumping: 
                self.jump()
                
    def attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()

    def set_status(self):
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
        self.hitbox.y += self.direction[1]

         # Check collision with the ground
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.jumping = False
            self.direction[1] = 0

    def run(self):
        self.hitbox.x += self.direction[0] * self.velocity
        # Make sure the characters stays on the screen
        if self.hitbox.right >= WIDTH:
            self.hitbox.right = WIDTH

        if self.hitbox.left <= 0:
            self.hitbox.left = 0

    def jump(self):
        self.jumping = True
        self.direction[1] = self.velocity_y

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
            self.attack_rect.topleft = self.hitbox.topleft
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.right = self.hitbox.right + 24
            self.rect.top = self.hitbox.top - 50
            self.attack_rect.topright = self.hitbox.topright
            
    

    def draw_health(self, screen):
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp

        # Position the health bar
        self.health_rect = pygame.Rect(0, 0, 100, 8)

        # Draw the health bar on the surface
        draw_health_bar(screen, (15, 15), (200, 15), health_ratio) 

    def update(self, screen):
        self.player_input(screen)
        self.apply_gravity()
        self.set_status()
        self.animate()

   

        



    
    


    