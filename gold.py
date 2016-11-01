import pygame
import math
import utils

class Gold(pygame.sprite.Sprite):
    def __init__(self,x,y,window,image,worth):
        super().__init__()
        self.image = image
        self.worth = int(worth)
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.position(window)
    def position(self,window):
        self.rect.x = window.x + self.x*16
        self.rect.y = window.y + self.y*16


class AnimatedGold(pygame.sprite.Sprite):
    def __init__(self,gold):
        super().__init__()
        self.image = gold.image
        self.rect = self.image.get_rect()
        self.rect.x = gold.rect.x
        self.rect.y = gold.rect.y

    def move(self):
        screen = pygame.display.get_surface()
        d = utils.distance(self.rect.x,self.rect.y,screen.get_width(),screen.get_width())
        leg = d/30

        dx = screen.get_width() - self.rect.x
        dy = screen.get_width() - self.rect.y
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        degs = math.degrees(rads)

        self.rect.x +=  leg*math.sin(degs)
        self.rect.y +=  leg*math.cos(degs)
