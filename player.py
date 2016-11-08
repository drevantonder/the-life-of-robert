import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,window):
        pygame.sprite.Sprite.__init__(self)
        self.frames = {
        "down" : pygame.image.load("Images/Bob/1.png").convert_alpha(),
        "right" : pygame.image.load("Images/Bob/2.png").convert_alpha(),
        "left" : pygame.image.load("Images/Bob/3.png").convert_alpha(),
        "up" : pygame.image.load("Images/Bob/4.png").convert_alpha(),
        }

        self.image = self.frames["down"]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.position(window)

    def down(self):
        self.image = self.frames["down"]
        self.y += 1

    def right(self):
        self.image = self.frames["right"]
        self.x += 1

    def left(self):
        self.image = self.frames["left"]
        self.x -= 1

    def up(self):
        self.image = self.frames["up"]
        self.y -= 1

    def position(self,window):
        self.rect.x = window.x + self.x*16
        self.rect.y = window.y + self.y*16
