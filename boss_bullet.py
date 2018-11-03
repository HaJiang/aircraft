import pygame

pygame.init()

class BossBullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image0 = pygame.image.load("image/boss_bullet0.png").convert_alpha()
        self.image1 = pygame.image.load("image/boss_bullet1.png").convert_alpha()
        self.image2 = pygame.image.load("image/boss_bullet2.png").convert_alpha()
        self.image = self.image0
        
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = position
        self.speed = 5
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)
        self.kind = 0

    def move0(self):
        if self.rect.top < 700-self.rect.width:
            self.rect.top += self.speed
        else:
            self.alive = False
       
    def move1(self):
        if self.rect.top < 700-self.rect.width and self.rect.left < 480 and self.rect.left > 0:
            self.rect.top += self.speed * 0.707
            self.rect.left -= self.speed * 0.707
        else:
            self.alive = False
        
    def move2(self):
        if self.rect.top < 700-self.rect.width and self.rect.left < 480 and self.rect.left > 0:
            self.rect.top += self.speed * 0.707
            self.rect.left += self.speed * 0.707
        else:
            self.alive = False
        

    def reset(self,position):
        self.rect.left , self.rect.top = position
        self.alive = True
        self.kind = 0 
