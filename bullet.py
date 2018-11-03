import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = position
        self.speed = 12
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.alive = False

    def reset(self,position):
        self.rect.left , self.rect.top = position
        self.alive = True
    
class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = position
        self.speed = 14
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self,position):
        self.rect.left, self.rect.top = position
        self.alive = True

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.alive = False
        
