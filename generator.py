import random
import pygame.draw


def generate_procedure_map():
    # 0 - void, 1 - wall, 2 - chest, 3 - player, 4 - next floor, 5 - standard enemy
    # 6 - mimic, 7 - boss, 8 - exit, 9 - death (real void)
    m_or_c = [random.randint(0, 1) for _ in range(32)]
    generator = Generator2()
    ans = generator.mix(generator.generator2() + generator.part4(), generator.part2() + generator.part3())
    for x in range(len(ans)):
        for y in range(len(ans[0])):
            if ans[x][y] == 9:
                if m_or_c[0] == 0:
                    ans[x][y] = 6
                else:
                    ans[x][y] = 2
                m_or_c.pop(0)
    return ans


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
                a = [0, 0, 2, 2, 6]
                random.shuffle(a)
                temp[w2] = a[0]
                b1 = [0, 0, 2, 2, 6]
                random.shuffle(b1)
                temp[w3] = b1[0]
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
