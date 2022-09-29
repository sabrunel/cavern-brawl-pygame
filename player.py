import pygame
import random
from fighter import Fighter, draw_health_bar
from settings import PLAYER_MAX_HP, PLAYER_START_POTIONS, PLAYER_STRENGTH


class Player(Fighter):
    def __init__(self, x, y, name, groups, collision_groups):
        super().__init__(name, groups, collision_groups)

        # Movement
        self.velocity = 6
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.8
        self.vertical_velocity = -15
        self.faces_right = True

        # Status
        self.is_attacking = False
        self.attack_time = 0
        self.animation_cooldown = 80
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
        self.rect.topleft = (x,y)

    def player_input(self):
            keys = pygame.key.get_pressed() 

            if keys[pygame.K_d]:
                self.direction[0] = 1
                self.faces_right = True

            elif keys[pygame.K_q]:
                self.direction[0] = -1
                self.faces_right = False

            else:
                self.direction[0] = 0

            if keys[pygame.K_p] and not self.is_attacking: # attack
                self.is_attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('attack')
                


    def move(self):
        # Horizontal movement
        if self.direction[0] != 0:
            self.rect.x += self.direction[0] * self.velocity

        # Horizontal collisions
        for sprite in self.collision_groups:
            if sprite.rect.colliderect(self.rect):
                if self.direction[0] > 0: # player was moving right
                    self.rect.right = sprite.rect.left
                if self.direction[0] < 0: # player was moving left
                    self.rect.left = sprite.rect.right

 
    def set_status(self):
        if self.direction[0] != 0:
            self.action = 'Run'
        else:
            self.action = 'Idle'

        if self.is_attacking:
            self.action = 'Attack'

           
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
        else:
            self.image = pygame.transform.flip(image, True, False)
    

    def draw_health(self, screen):
        # Calculate health ratio
        health_ratio = self.hp / self.max_hp

        # Position the health bar
        self.health_rect = pygame.Rect(0, 0, 100, 8)

        # Draw the health bar on the surface
        draw_health_bar(screen, (15, 15), (200, 15), health_ratio) 

    def update(self):
        self.player_input()
        self.set_status()
        self.move()
        self.cooldown()
        self.animate()

   

        



    
    


    