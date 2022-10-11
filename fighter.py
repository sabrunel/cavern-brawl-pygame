import pygame
from settings import character_animation_frames, fighter_info



# Fighter class
class Fighter(pygame.sprite.Sprite):
    def __init__(self, x, y, name, groups, attackable_sprites):
        super().__init__(groups)
        self.name = name

        # Animations
        self.action = 'Idle'
        self.frame_index = 0
        self.load_graphics()
        self.animation_cooldown = 80

        # Group setup
        self.attackable_sprites = attackable_sprites

        # Core characteristics 
        self.strength = fighter_info[self.name]["strength"]
        self.max_hp = fighter_info[self.name]["max_hp"]
        
        # Movement
        self.velocity = fighter_info[self.name]["velocity"]
        self.direction = pygame.math.Vector2(0,0)

        # Position and collisionboxes
        self.start_pos = (x, y + fighter_info[self.name]["y_offset"])
        self.rect.bottomleft = self.start_pos
        self.hurtbox = pygame.Rect((self.rect.left + fighter_info[self.name]["hurtbox"][0], self.rect.top + fighter_info[self.name]["hurtbox"][1]),fighter_info[self.name]["hurtbox"][2])
        self.hitbox = pygame.Rect((self.rect.left + fighter_info[self.name]["hitbox"][0], self.rect.top + fighter_info[self.name]["hitbox"][1]),fighter_info[self.name]["hitbox"][2])
        self.faces_right = True

        # Creation time
        self.update_time = pygame.time.get_ticks() 
        self.alive = True

    def load_graphics(self):
        self.action_dict = character_animation_frames[self.name]
        self.animation_dict = {}

        for action in self.action_dict.keys():
            temp_list = []
            for i in range(1, self.action_dict[action] + 1):
                img = pygame.image.load(f'assets/characters/{self.name}/{action}/0{i}.png')
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
        self.hurtbox.size = (0,0)
        self.hitbox.size = (0,0)

    def animate(self):
            # Move through the animation frames  
            if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            # Make sure we don't go beyond the number of frames in the list
            if self.frame_index >= len(self.animation_dict[self.action]):
                if self.action == 'Death':
                    self.frame_index = len(self.animation_dict[self.action]) - 1

                elif self.action == 'Hurt':
                    self.hit = False
                    self.frame_index = 0

                else:
                    self.frame_index = 0

            image = self.animation_dict[self.action][self.frame_index]

            if self.faces_right:
                self.image = image
                self.rect.left = self.hurtbox.left - fighter_info[self.name]["hurtbox"][0]
                self.rect.top = self.hurtbox.top  - fighter_info[self.name]["hurtbox"][1]
                self.hitbox.left = self.hurtbox.left + fighter_info[self.name]["hitbox"][0]
                self.hitbox.top = self.hurtbox.top  + fighter_info[self.name]["hitbox"][1]
            else:
                self.image = pygame.transform.flip(image, True, False)
                self.rect.right = self.hurtbox.right + fighter_info[self.name]["hurtbox"][0]
                self.rect.top = self.hurtbox.top - fighter_info[self.name]["hurtbox"][1]
                self.hitbox.right = self.hurtbox.right - fighter_info[self.name]["hitbox"][0]
                self.hitbox.top = self.hurtbox.top + fighter_info[self.name]["hitbox"][1]





    