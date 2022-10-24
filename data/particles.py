import pygame
from .settings import particle_animation_frames, GRAPHICS_DIR

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, name, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.name = name
        
        # Animation
        self.frame_index = 0
        self.load_graphics()
        self.animation_cooldown = 60

        # Position
        self.rect.center = (x,y)

        # Creation time
        self.update_time = pygame.time.get_ticks()

    def load_graphics(self):
        self.particle_dict = particle_animation_frames
        self.animation_dict = {}

        for particle in self.particle_dict.keys():
            temp_list = []
            for i in range(1, self.particle_dict[particle] + 1):
                img = pygame.image.load(GRAPHICS_DIR + f'effects/{particle}/0{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_dict.update({particle : temp_list})
        
        self.image = self.animation_dict[self.name][self.frame_index]
        self.rect = self.image.get_rect()

    def animate(self):
        self.image = self.animation_dict[self.name][self.frame_index]

        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.name]):
            self.kill()

    def update(self):
        self.animate()

        

