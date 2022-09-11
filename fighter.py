import pygame

# Fighter class:
class Fighter():
    def __init__(self, x, y, name):
        self.name = name
        img = pygame.image.load(f'assets/{self.name}/Idle/01.png').convert_alpha() 
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    

