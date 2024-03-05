# Генератор карты, по умолчанию level: 1, 2, 3, 4, 5
import random
import pygame.draw

from entity import Wall

start_x = 50
start_y = 50
b = 0


def generate_procedure_map(level=1):
    # 0 - void, 1 - wall, 2 - chest, 3 - player, 4 - next floor, 5 - standard enemy
    # 6 - mimic, 7 - boss, 8 - exit, 9 - death (real void)
    map = Map()
    field = map.mv3x7()
    return field


class Map:
    @staticmethod
    def mv3x3():
        return [
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1]
        ]

    @staticmethod
    def mh3x3():
        return [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]

    @staticmethod
    def m3x3():
        return [
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1]
        ]

    @staticmethod
    def mv3x7():
        return [
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1]
        ]

    @staticmethod
    def m5x5():
        return [
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1]
        ]


def get_real_image(image, scale=0.8):  # Функция для изменения размера кнопки
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))


# Константы:
scale = 1
death = get_real_image(pygame.image.load('assets/game/states/death50x50.png'), scale)
void = get_real_image(pygame.image.load('assets/game/states/void50x50.png'), scale)
wall = get_real_image(pygame.image.load('assets/game/states/wall50x50.png'), scale)
boss = get_real_image(pygame.image.load('assets/game/states/boss50x50.png'), scale)
chest = get_real_image(pygame.image.load('assets/game/states/chest50x50.png'), scale)
enemy = get_real_image(pygame.image.load('assets/game/states/enemy50x50.png'), scale)
mimic = get_real_image(pygame.image.load('assets/game/states/mimic50x50.png'), scale)
next_level = get_real_image(pygame.image.load('assets/game/states/next_level50x50.png'), scale)
player = get_real_image(pygame.image.load('assets/game/states/player50x50.png'), scale)

