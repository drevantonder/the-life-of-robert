import pygame

class Chest(pygame.sprite.Sprite):
    def __init__(self,x,y,window,image,Map):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.map = Map
        self.gold = 0
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.position(window)

    def position(self,window):
        self.rect.x = window.x + self.x*16
        self.rect.y = window.y + self.y*16

    def take(self,amount):
        if self.gold - amount >= 0:
            self.gold -= amount
            return amount
        else:
            self.gold -= (amount-abs(self.gold - amount))
            return (amount-abs(self.gold - amount))

    def give(self,amount):
        self.gold += amount
