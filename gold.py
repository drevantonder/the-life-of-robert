import pygame
import math
import utils
from threading import Timer

class Gold(pygame.sprite.Sprite):
    def __init__(self,x,y,window,image,worth):
        pygame.sprite.Sprite.__init__(self)
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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gold.image,(24,24))
        self.rect = self.image.get_rect()
        self.rect.x = gold.rect.x - 6
        self.rect.y = gold.rect.y - 6
        Timer(0.2,self.kill).start()
