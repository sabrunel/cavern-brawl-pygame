import pygame
from settings import animation_frames



# Fighter class
class Fighter(pygame.sprite.Sprite):
    def __init__(self, name, groups, collision_groups):
        super().__init__(groups)
        self.name = name

        # Animations
        self.action = 'Idle'
        self.frame_index = 0
        self.load_graphics()
        self.animation_cooldown = 80

        # Group setup
        self.collision_groups = collision_groups

        # Creation time
        self.update_time = pygame.time.get_ticks() 

    def load_graphics(self):
        self.action_dict = animation_frames[self.name]
        self.animation_dict = {}

        for action in self.action_dict.keys():
            temp_list = []
            for i in range(1, self.action_dict[action] + 1):
                img = pygame.image.load(f'assets/{self.name}/{action}/0{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_dict.update({action : temp_list})
        
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def hurt(self):
            self.action = 'Hurt' # switch to hurt action
            self.frame_index = 0 # start at the beginning of the sequence
            self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 'Death' # switch to death action
        self.frame_index = 0 # start at the beginning of the sequence
        self.update_time = pygame.time.get_ticks()




    