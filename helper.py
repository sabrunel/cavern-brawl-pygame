import pygame
from settings import *

def draw_text(screen, text, font, text_color, x, y):
    """ 
    This function draws an input text to the screen
    """
    img = font.render(text, False, text_color)
    screen.blit(img, (x, y))

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