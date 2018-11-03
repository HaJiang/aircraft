import pygame
from random import *

pygame.init()

class SmallEnemy(pygame.sprite.Sprite):
    Energy = 1
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("image/enemy1.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("image/enemy1_bomb1.png").convert_alpha(),\
            pygame.image.load("image/enemy1_bomb2.png").convert_alpha(),\
            pygame.image.load("image/enemy1_bomb3.png").convert_alpha(),\
            pygame.image.load("image/enemy1_bomb4.png").convert_alpha()
            ])
        
        self.rect = self.image.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 2
        self.alive = True
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-5 * self.height , 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = SmallEnemy.Energy

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.alive = True
        self.energy = SmallEnemy.Energy
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-5 * self.height , 0)

class MidEnemy(pygame.sprite.Sprite):
    Energy = 20
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("image/enemy2.png").convert_alpha()
        self.image_hit =pygame.image.load("image/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("image/enemy2_bomb1.png").convert_alpha(),\
            pygame.image.load("image/enemy2_bomb2.png").convert_alpha(),\
            pygame.image.load("image/enemy2_bomb3.png").convert_alpha(),\
            pygame.image.load("image/enemy2_bomb4.png").convert_alpha()
            ])
        
        self.rect = self.image.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 1
        self.alive = True
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-10 * self.height , -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.Energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.alive = True
        self.energy = MidEnemy.Energy
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-10 * self.height , -self.height)

class BigEnemy(pygame.sprite.Sprite):
    Energy = 50
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image1 = pygame.image.load("image/enemy3_1.png").convert_alpha()
        self.image2 = pygame.image.load("image/enemy3_2.png").convert_alpha()
        self.image_hit = pygame.image.load("image/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("image/enemy3_bomb1.png").convert_alpha(),\
            pygame.image.load("image/enemy3_bomb2.png").convert_alpha(),\
            pygame.image.load("image/enemy3_bomb3.png").convert_alpha(),\
            pygame.image.load("image/enemy3_bomb4.png").convert_alpha(),\
            pygame.image.load("image/enemy3_bomb5.png").convert_alpha(),\
            pygame.image.load("image/enemy3_bomb6.png").convert_alpha()
            ])
        
        self.rect = self.image1.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 1
        self.alive = True
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-15 * self.height , -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemy.Energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.alive = True
        self.energy = BigEnemy.Energy
        self.rect.left , self.rect.top = \
                       randint(0,self.width - self.rect.width) , \
                       randint(-15 * self.height , -5 * self.height)
