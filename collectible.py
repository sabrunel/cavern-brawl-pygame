import pygame
from settings import collectible_animation_frames

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, name, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.name = name
        
        # Animation
        self.frame_index = 0
        self.load_graphics()
        self.animation_cooldown = 80

        # Position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.counter = 0

        # Creation time
        self.update_time = pygame.time.get_ticks()

    def load_graphics(self):
        self.collectible_dict = collectible_animation_frames
        self.animation_dict = {}

        for collectible in self.collectible_dict.keys():
            temp_list = []
            for i in range(1, self.collectible_dict[collectible] + 1):
                img = pygame.image.load(f'assets/collectibles/{collectible}/0{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_dict.update({collectible : temp_list})
        
        self.image = self.animation_dict[self.name][self.frame_index]
        self.rect = self.image.get_rect()

    def animate(self):
        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.name]):
            self.frame_index = 0

        self.image = self.animation_dict[self.name][self.frame_index]

    def update(self):
        self.counter += 1

        # Delete the collectible after a few seconds
        if self.counter > 300:
            self.kill()
        else:
            self.animate()

        

