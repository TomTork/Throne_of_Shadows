# Генератор карты, по умолчанию level: 1, 2, 3, 4, 5
import random
import pygame.draw
import numpy

from entity import Wall

start_x = 50
start_y = 50
b = 0


def generate_procedure_map(level=1):
    # 0 - void, 1 - wall, 2 - chest, 3 - player, 4 - next floor, 5 - standard enemy
    # 6 - mimic, 7 - boss, 8 - exit, 9 - death (real void)
    # index = 0
    # map_ = Map()
    # ran = [random.randint(1, 2) for _ in range(9)]
    # field = map_.m_base(70)
    #
    # for r in ran:
    #     if r == 1:
    #         field = map_.insert(field, index, map_.m3x3(), 70, 5)
    #         index += 4
    #     elif r == 2:
    #         field = map_.insert(field, index, map_.m5x5(), 70, 7)
    #         index += 6
    # return field
    generator = Generator2()
    map_ = Map()
    field = map_.m_base(70)
    return generator.mix(generator.generator2() + generator.part4(), generator.part2() + generator.part3())


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
    def m7x7():
        return [
            [1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 1]
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

    def insert(self, isx: list, index: int, obj: list, _size: int, size_map: int, y=5) -> list:
        for i in range(len(obj)):
            isx[i + index - 1] = (obj[i] + self.add_zero5(isx, i + index, _size, obj))[:_size]
        return isx

    def add_zero5(self, isx: list, ind: int, _size: int, obj: list) -> list:
        if ind != 0:
            prev = isx[ind - 1]
        else:
            prev = isx[ind]
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













class Generator2:
    @staticmethod
    def generate(m: list):
        sx = 0
        sy = 0
        widths = [random.randint(3, 23) for _ in range(3)]
        heights = [random.randint(3, 10) for _ in range(9)]
        ops = 0
        while len(widths) != 0 or len(heights) != 0:
            if ops > 10:
                break
            for x in range(sx, len(m)):
                if len(widths) == 0 or len(heights) == 0:
                    break
                for w in range(sx, widths[0]):
                    if w % 3 == 0:
                        m[w][sy] = 0
                    else:
                        m[w][sy] = 1
                sx = widths[0]
                widths.pop(0)
                for y in range(sy, len(m[0])):
                    if len(widths) == 0 or len(heights) == 0:
                        break
                    for h in range(sy, heights[0]):
                        if h % 3 == 0:
                            m[sx][h] = 0
                        else:
                            m[sx][h] = 1
                    sy = heights[0]
                    heights.pop(0)
            ops += 1
        return m

    @staticmethod
    def generator2():
        part1 = []
        fragment1 = [1] + [1] * 38 + [1]
        wall1 = [1] + [0] + [0] * 36 + [0] + [1]
        h = [random.randint(3, 40) for _ in range(16)]
        w1, w2, w3 = [random.randint(3, 37) for _ in range(3)]
        for local_h in range(0, 40, 1):
            if local_h in h:
                temp = fragment1.copy()
                temp[w1] = 0
                temp[w2] = 0
                temp[w3] = 0
                part1.append(temp)
                for y in range(len(part1)):
                    part1[y][local_h] = 0
            else:
                w1, w2, w3 = [random.randint(3, 37) for _ in range(3)]
                temp_wall = wall1.copy()
                temp_wall[w1] = 0
                temp_wall[w2] = 0
                temp_wall[w3] = 0
                part1.append(temp_wall)
        add_wall = [random.randint(3, 40) for _ in range(8)]
        stop_wall = ([random.randint(3, 40) for _ in range(8)])
        for x in range(40):
            if x in add_wall:
                for y in range(3, 40):
                    if len(stop_wall) > 0 and y == stop_wall[0]:
                        stop_wall.pop(0)
                        break
                    if part1[y][x] == 0:
                        part1[y][x] = 1
        part1[0] = [1] * 40
        part1[-1] = [1] * 40
        part1[18] = [1] + [0] * 39
        part1[19] = [1] + [0] * 39
        part1[20] = [1] + [0] * 39
        part1[1] = [1] + [0] * 39
        part1[2] = [1] + [0] * 39
        part1[-2] = [1] + [0] * 39
        part1[-3] = [1] + [0] * 39
        part1[39][1] = 0
        part1[39][2] = 0
        part1[39][19] = 0
        part1[39][20] = 0
        return part1

    @staticmethod
    def part2():
        f = open('assets/stage1.txt', 'r')
        mas = []
        for line in f:
            if line != '\n':
                mas.append([int(i) for i in line.split(', ')])
        f.close()
        return mas

    @staticmethod
    def part3():
        f = open('assets/stage2.txt', 'r')
        mas = []
        for line in f:
            if line != '\n':
                mas.append([int(i) for i in line.split(', ')])
        f.close()
        return mas

    @staticmethod
    def part4():
        f = open('assets/stage3.txt', 'r')
        mas = []
        for line in f:
            if line != '\n':
                mas.append([int(i) for i in line.split(', ')])
        f.close()
        return mas

    @staticmethod
    def mix(mas1, mas2):
        answer = []
        for x in range(len(mas1)):
            answer.append(mas1[x] + mas2[x])
        return answer
