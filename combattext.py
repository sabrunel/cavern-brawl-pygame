import pygame

class CombatText(pygame.sprite.Sprite):
    def __init__(self, x, y, font, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self): # override the inherited update method
        # Move damage text upwards
        self.rect.y -= 1

        # Delete the text after a few seconds
        self.counter += 1

        if self.counter > 30:
            self.kill()