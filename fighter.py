import pygame

# Fighter class:
class Fighter():
    def __init__(self, x, y, name):
        self.name = name

        # Animations
        self.action_dict = { # Number of frames per animation
            'Idle': 9,
            'Attack': 7,
            'Hurt': 3,
            'Death':7,
        }
        self.update_time = pygame.time.get_ticks() #To know when the instance of the class is first created
        
        # Load all animation images to a dictionary
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
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        animation_cd = 100

        # Move through the animation frames
        self.image = self.animation_dict[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Make sure we don't go beyond the number of frames in the list
        if self.frame_index >= len(self.animation_dict[self.action]):
            self.frame_index = 0
            

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def idle(self):
        self.action = 'Idle'
        self.frame_index = 0 # Start with the first frame
        self.update_time = pygame.time.get_ticks()

    

