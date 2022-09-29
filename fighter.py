import pygame
from settings import BORDER_RADIUS, HEALTH_BORDER, HEALTH_GREEN, HEALTH_RED, BORDER_WIDTH, animation_frames



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
    def __init__(self, name, groups, collision_groups):
        super().__init__(groups)
        self.name = name

        # Animations
        self.action = 'Idle'
        self.frame_index = 0
        self.load_graphics()

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





    