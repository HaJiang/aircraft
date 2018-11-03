import pygame

class Background2():
    def __init__(self):
        self.image = pygame.image.load("image/background2.png").convert()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = (0,-700)
        self.speed = 5

    def move(self):
        if self.rect.top < 0:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left,self.rect.top = (0,-700)
    
