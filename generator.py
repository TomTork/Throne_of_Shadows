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
    index = 0
    map_ = Map()
    ran = [random.randint(1, 2) for _ in range(9)]
    field = map_.m_base(70)

    for r in ran:
        if r == 1:
            field = map_.insert(field, index, map_.m3x3(), 70, 5)
            index += 4
        elif r == 2:
            field = map_.insert(field, index, map_.m5x5(), 70, 7)
            index += 6
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

    @staticmethod
    def m5x10():
        return [
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1]
        ]

    @staticmethod
    def m10x5():
        return [
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        ]

    @staticmethod
    def m_base(base: int):
        return [
            [0 for _ in range(base)]
        ] * base

    def insert(self, isx: list, index: int, obj: list, _size: int, size_map: int) -> list:
        for i in range(len(obj)):
            # obj[i].extend(self.add_zero(isx, i, _size, obj)[len(obj):_size - len(obj)])
            # obj[i].extend([0] * len(obj))
            isx[i + index - 1] = (obj[i] + self.add_zero5(isx, i + index, _size, obj))[:_size]
        return isx

    def add_zero5(self, isx: list, ind: int, _size: int, obj: list) -> list:
        prev = isx[ind - 1]
        stop_index = 0
        ans = obj.copy() + [0] * (_size - len(obj))
        for i in range(_size):
            if prev[i] == 0 and prev[i + 1] != 1:
                stop_index = i - 1
                break

        for i in range(stop_index // len(obj) - 1):
            ans[i] = 1
        return ans

    def add_zero4(self, size_map: int, _size: int, obj: list) -> list:
        ans = [0] * (_size - len(obj))
        for i in range(_size - len(obj)):
            if i < 1:
                ans[i] = 1
            else:
                ans[i] = 0
        return ans


    def add_zero3(self, isx: list, obj: list, ind: int) -> list:
        prev = isx[ind - 1]
        for i in range(len(obj)):
            prev[i] = obj[i]
        return prev

    def add_zero(self, isx: list, ind: int, _size: int, obj: list) -> list:
        answer = [0] * _size
        for index in range(len(obj[ind - 1]), _size):
            if isx[ind][index] == 1:
                answer[index] = 1
            else:
                answer[index] = 0
        return answer

    def add_zero2(self, isx: list, ind: int, _size: int, obj: list):
        answer = [0] * _size
        for i in range(_size):
            if i < len(obj):
                answer[i] = obj[i]
            else:
                if isx[ind - 1][i] == 0:
                    answer[i] = 0
                else:
                    answer[i] = 1
        return answer

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

