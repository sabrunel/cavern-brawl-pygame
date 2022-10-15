import pygame
from settings import projectile_animation_frames, projectile_info

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, name, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.name = name

        # Animation
        self.frame_index = 0
        self.load_graphics()
        self.animation_cooldown = 80

        # Position
        self.rect = self.image.get_rect()
        self.rect.midleft = (x,y)
    
        # Movement
        self.velocity = projectile_info[self.name]['velocity']
        self.direction = pygame.math.Vector2(0,0)

        # Creation time
        self.update_time = pygame.time.get_ticks()

    def load_graphics(self):
        self.projectile_dict = projectile_animation_frames
        self.animation_dict = {}

        for projectile in self.projectile_dict.keys():
            temp_list = []
            for i in range(1, self.projectile_dict[projectile] + 1):
                img = pygame.image.load(f'assets/projectiles/{projectile}/0{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_dict.update({projectile : temp_list})
        
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


class Dagger(Projectile):
    def __init__(self, x, y, name, groups, faces_right):
        super().__init__(x, y, name, groups)
    
        # Movement
        self.faces_right = faces_right

    def check_direction(self):
        if self.faces_right:
            self.direction[0] = 1

        else:
            self.direction[0] = -1

    def move(self):
        self.rect.x += self.direction[0] * self.velocity

    def animate(self):
        # Move through the animation frames  
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.name]):
            self.frame_index = 0

        image = self.animation_dict[self.name][self.frame_index]

        if self.faces_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def update(self): # override the inherited update method
        self.check_direction()
        self.move()
        self.animate()
        
            
class Orb(Projectile):
    def __init__(self, x, y, name, groups):
        super().__init__(x, y, name, groups)

        # Movement
        self.direction = pygame.math.Vector2(0,1)

    def move(self):
        self.rect.y += self.direction[1] * self.velocity

    def update(self): # override the inherited update method
        self.move()
        self.animate()
            

        