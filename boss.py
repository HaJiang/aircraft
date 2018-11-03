import pygame
from random import *

pygame.init()#++++++++

class Boss(pygame.sprite.Sprite):
    Energy = 200
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("image/boss.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("image/boss_bomb1.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb1.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb2.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb2.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb3.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb3.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb4.png").convert_alpha(),\
            pygame.image.load("image/boss_bomb4.png").convert_alpha()
            ])
        
        self.rect = self.image.get_rect()
        self.width ,self.height = bg_size[0] , bg_size[1]
        self.speed = 1
        self.alive = True
        self.rect.left , self.rect.top = \
                       randint(0,self.width),\
                       40
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = Boss.Energy
        self.direction = True
        
    def move(self):
        if self.rect.left <= 0 :
            self.direction = False
        if self.rect.right >= self.width:
            self.direction = True
        if self.direction:
            self.rect.left -= self.speed
        else:
            self.rect.left += self.speed

    def reset(self):
        self.alive = True
        self.energy = Boss.Energy
        self.rect.left , self.rect.top = \
                       randint(0,self.width),\
                       -2*self.height
