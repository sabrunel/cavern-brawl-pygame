import pygame
import random

# Settings and helper functions
from .settings import GROUND_Y, WIDTH, SOUNDS_DIR
from .helper import draw_health_bar

# Classes
from .fighter import Fighter


class Player(Fighter):
    def __init__(self, x, y, name, groups):
        super().__init__(x, y, name, groups)

        # Characteristics
        self.hp = self.max_hp
        self.damage = self.strength + random.randint(-3,3)

        # Special movement
        self.velocity_y = -20
        self.gravity = 0.9

        # Sounds
        self.load_sounds()

        # Status
        self.jumping = False
        self.attack_choice = 'Attack'
        self.attacking_melee = False
        self.attacking_range = False
        self.can_pick_collectible = True
        self.attack_time = 0
        self.hit = False

    def load_sounds(self):
        self.attack_sound = pygame.mixer.Sound(SOUNDS_DIR + 'Attack.wav')
        self.ranged_attack_sound = pygame.mixer.Sound(SOUNDS_DIR + 'RangedAttack.wav')

    def set_status(self):
        if self.alive and not self.hit:
            if self.direction[1] != 0:
                self.action = 'Jump'

            if self.direction[0] != 0 and not self.jumping: # avoids triggering the running animation while in the air
                self.action = 'Run'

            else:
                self.action = 'Idle'

            # Attack status
            if self.attacking_melee and not self.jumping:
                self.action = self.attack_choice
            
            elif self.attacking_melee and self.jumping:
                self.action = 'AttackUp'
                
            if self.attacking_range:
                self.action = 'RangedAttack'


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

    def melee_attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking_melee = True
        self.frame_index = 0
        self.attack_sound.play()

    def ranged_attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking_range = True
        self.frame_index = 0
        self.ranged_attack_sound.play()

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

   

        



    
    


    