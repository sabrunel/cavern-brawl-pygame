import pygame
import random


class Fighter():
    def __init__(self, x, y, name, strength, max_hp, start_potions):

        # Characteristics
        self.name = name
        self.hp = max_hp 
        self.strength = strength
        self.max_hp = max_hp
        self.start_potions = start_potions
        self.potions = start_potions
        self.alive = True
        self.damage = self.strength + random.randint(-5,5)

        # Animations
        self.action_dict = { # Number of frames per animation
            'Idle': 9,
            'Attack': 7,
            'Hurt': 3,
            'Death':7,
        }
        
        self.animation_dict = {}
        for action in self.action_dict.keys():
            temp_list = []
            for i in range(1, self.action_dict[action] + 1):
                img = pygame.image.load(f'assets/{self.name}/{action}/0{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_dict.update({action : temp_list})

        self.action = 'Idle'
        self.frame_index = 0

        # Image
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Creation time
        self.update_time = pygame.time.get_ticks() 
        

    def idle(self):
        self.action = 'Idle'
        self.frame_index = 0 # Start with the first frame
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Deal damage to the enemy
        target.hp -= self.damage
        
        # Check if the target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        # Run enemy hurt animation
        else:
            target.hurt()

        # Set variables to attack animation
        self.action = 'Attack' # switch to attack action
        self.frame_index = 0 # start at the beginning of the sequence
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
            self.action = 'Hurt' # switch to hurt action
            self.frame_index = 0 # start at the beginning of the sequence
            self.update_time = pygame.time.get_ticks()


    def death(self):
        self.action = 'Death' # switch to death action
        self.frame_index = 0 # start at the beginning of the sequence
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.hp = self.max_hp 
        self.potions = self.start_potions
        self.alive = True
        self.action = 'Idle'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    

    def update(self):
        animation_cd = 100

        # Move through the animation frames
        self.image = self.animation_dict[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
            if self.action == 'Death':
                self.frame_index = len(self.animation_dict[self.action]) - 1
            else:
                self.idle()
            

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    