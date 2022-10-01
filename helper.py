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
    pygame.draw.rect(screen, HEALTH_BORDER, (*pos, *size))
    inner_x = pos[0]+ BORDER_WIDTH
    inner_y = pos[1]+ BORDER_WIDTH
    inner_w = size[0] - BORDER_WIDTH * 2
    inner_h = size[1] - BORDER_WIDTH * 2
    pygame.draw.rect(screen, HEALTH_GREY, ((inner_x, inner_y), (inner_w, inner_h)))
    pygame.draw.rect(screen, HEALTH_RED, ((inner_x, inner_y), (inner_w * health_ratio,inner_h)))