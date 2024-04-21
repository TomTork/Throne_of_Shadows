import pygame.sprite
from pygame.transform import scale


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/player50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Void(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/death50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/pl50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/enemy50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/chest50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/boss50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Mimic(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/mimic50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('assets/game/states/exit50x50.png'), (10, 10))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))