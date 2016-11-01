#Copyright (c) 2016 Copyright Andre van Tonder All Rights Reserved.
import settings
import pygame
import os
import math

def distance2(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
def distance(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

def draw_font(text,font_size,font=settings.FONT, color = (255,255,255)):
    try:
        myFont=pygame.font.Font(font,font_size)
    except OSError:
        myFont=pygame.font.SysFont(font,font_size)
    return myFont.render(text, 1, color)

def load_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
