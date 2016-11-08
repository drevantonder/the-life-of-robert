import pygame
import settings
import utils

class Button(pygame.sprite.Sprite):
    def __init__(self,text,x,y,color=settings.BUTTON_COLOR):
        pygame.sprite.Sprite.__init__(self)
        font_size = 24
        text = utils.draw_font(text,font_size)
        self.image = pygame.Surface([text.get_width()+16,text.get_height()+8])
        self.image.fill(color)
        self.image.blit(text,(8,6))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pressed(self, pos):
        return self.rect.collidepoint(pos)
