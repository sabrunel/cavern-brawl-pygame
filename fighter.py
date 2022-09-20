import pygame
from settings import BORDER_RADIUS, HEALTH_BORDER, HEALTH_GREEN, HEALTH_RED, BORDER_WIDTH



# Helper functions
def draw_health_bar(screen, pos, size, health_ratio):
    """ 
    This function draws the different components of a healthbar: background, foreground and border
    """
    pygame.draw.rect(screen, HEALTH_RED, (*pos, *size), 0, BORDER_RADIUS)
    pygame.draw.rect(screen, HEALTH_BORDER, (*pos, *size), BORDER_WIDTH, BORDER_RADIUS)
    inner_pos  = (pos[0]+1, pos[1]+1)
    inner_size = ((size[0]-2) * health_ratio, size[1]-2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(screen, HEALTH_GREEN, rect, 0, BORDER_RADIUS)


# Fighter class
class Fighter(pygame.sprite.Sprite):
    def __init__(self, name, groups):
        super().__init__(groups)

        self.name = name
        self.alive = True

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


    