import pygame.sprite
from pygame.transform import scale


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/wall50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Void(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/void50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/player50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))