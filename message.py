import pygame
import utils

class Message(pygame.sprite.Sprite):
    def __init__(self,x,y,message,window):
        super().__init__()
        font_size = 16
        self.text = utils.draw_font(message,font_size)
        self.image = pygame.Surface([self.text.get_width()+16,self.text.get_height()+8])
        self.image.fill([23,38,38])
        self.image.blit(self.text,(8,6))
        self.rect = self.image.get_rect()
        self.x = x-self.text.get_width()/2
        self.y = y-16-self.text.get_height()
        self.position(window)
    def position(self,window):
        screen = pygame.display.get_surface()
        self.rect.x = window.x + self.x
        self.rect.y = window.y + self.y
        if self.rect.x < 0:
            self.rect.x += abs(self.rect.x)
        if self.rect.y < 0:
            self.rect.y += abs(self.rect.y)
        if self.rect.x+self.rect.width > screen.get_width():
            self.rect.x -= abs(screen.get_width()-(self.rect.x+self.rect.width))
        if self.rect.y+self.rect.height > screen.get_height():
            self.rect.y -= abs(screen.get_height()-(self.rect.y+self.rect.height))
