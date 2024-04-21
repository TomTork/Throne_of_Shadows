import time

import generator
from database import Database
import pygame
import threading
from entity import Wall, Player, Enemy, Chest, Mimic, Boss
import random

database = Database()
window = 0  # Переменная, хранящая состояние окна
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_cycle = True
fell_alive = True  # Переменная, следящая за жизнью игрока
hp = 7
level1 = generator.generate_procedure_map(1)
le_x, le_y = len(level1), len(level1[0])
x, y = 1, 1
text = ''
in_fight = False
type_enemy = 0  # 5 - st. enemy; 6 - mimic; 7 - boss;
choice = 0
action = -1
in_food = False
type_trader = -1  # 0 - food, 1 - weapons, 2 - others
init_enemy = True
image_enemy = None
hp_enemy = 1
damage_enemy = 0
chance_enemy = 100
chance_escape = 100
reward = 0
motion = True  # первым ходит игрок
x_enemy, y_enemy = 0, 0
enemy_id = -1
escape = False


def show_start_buttons():
    background = pygame.image.load('assets/backgrounds/background_game.png')
    screen.blit(background, (0, 0))

    from support import new_game_img, continue_img, quit_img
    screen.blit(new_game_img, (20, 100))
    screen.blit(continue_img, (20, 200))
    screen.blit(quit_img, (20, 300))


def show_game_buttons():
    from support import button_cave
    screen.blit(button_cave, (20, 1800))


def main_module():
    global window, screen, database, clock, fell_alive, hp, x, y, in_fight, \
        type_enemy, choice, action, text, in_food, type_trader, level1, \
        init_enemy, image_enemy, hp_enemy, chance_enemy, chance_escape, \
        reward, motion, damage_enemy, x_enemy, y_enemy, enemy_id, escape
    from support import button_new_game, button_continue, \
        button_quit, background, wait_fullscreen, button_cave, \
        cave_img, button_castle, castle_img, button_ferm, ferm_img, \
        button_wizard, wizard_img, only_black, n_text, weapon_to_name_and_damage, \
        to_normal_foods, generate_money_from_chest, field_choice, exit_button, \
        Button, to_normal_others, ViewEnemy, generate_name_enemy, probability, \
        mimic_img
    weapon_id = database.get_weapons()
    food = to_normal_foods(database.get_foods())
    name, damage = weapon_to_name_and_damage(weapon_id)
    happy = database.get_happy()
    happy_debug = True
    money = database.get_money()
    money_debug = True
    threading.Thread(target=show_start_buttons(),
                     args=(1,), daemon=True).start()
    plus_buttons2 = [
        Button(' +', 1004, 640, screen=screen, font_size=50),
        Button(' +', 1004, 690, screen=screen, font_size=50),
        Button(' +', 1004, 740, screen=screen, font_size=50),
        Button(' +', 1004, 790, screen=screen, font_size=50),
    ]

    enemies = [
        ViewEnemy(5, 2, 2, 2),
        ViewEnemy(5, 3, 4, 4)
    ]
    for enemy in enemies:
        level1[enemy.x][enemy.y] = 5

    while game_cycle:  # Обработка работы pygame
        clock.tick(15)
        if happy_debug:  # обновляем уровень счастья
            happy = database.get_happy()
            if happy <= 0:
                window = 4
            happy_debug = False
        if money_debug:
            money = database.get_money()
            money_debug = False
        if window == 0:
            if button_new_game.draw():
                print("NEW GAME - 0")
                database.reload()  # Очищение базы данных
                window = 1
                wait_fullscreen = True
            if button_continue.draw():
                if database.get_existing() == 0:  # create new game
                    print("NEW GAME - 1")
                    database.reload()
                window = 1
                wait_fullscreen = True
                database.set_existing(1)
            if button_quit.draw():
                exit()
                pygame.quit()
                break
            fell_alive = True
            hp = 7
        elif window == 1:
            if wait_fullscreen:
                pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                wait_fullscreen = False
            if button_cave.draw():  # Нажатие на кнопку cave, запуск игры
                screen.blit(cave_img, (0, 0))
                window = 2
            elif button_castle.draw():
                screen.blit(castle_img, (0, 0))
                window = 3
                type_trader = 1
            elif button_ferm.draw():
                screen.blit(ferm_img, (0, 0))
                window = 3
                type_trader = 0
            elif button_wizard.draw():
                screen.blit(wizard_img, (0, 0))
                window = 3
                type_trader = 2
            else:
                if not button_cave.listener(screen, cave_img) \
                        and not button_castle.listener(screen, castle_img) \
                        and not button_ferm.listener(screen, ferm_img) \
                        and not button_wizard.listener(screen, wizard_img):
                    screen.blit(background, (0, 0))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f'Уровень счастья граждан: {happy}', False, (255, 255, 255)), (10, 10))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f'Капитал: {money}', False, (255, 255, 255)), (10, 36))
        elif window == 2:  # В подземелье
            screen.blit(only_black, (0, 0))
            if hp <= 0:
                window = 4
            for w in range(le_x):
                for h in range(le_y):
                    if not in_fight:  # если не находимся в битве
                        if level1[w][h] == 1:
                            Wall(h * 10 + 50, w * 10 + 50).draw(screen)
                        elif level1[w][h] == 5:
                            Enemy(h * 10 + 50, w * 10 + 50).draw(screen)
                        elif level1[w][h] == 2:
                            Chest(h * 10 + 50, w * 10 + 50).draw(screen)
                        elif level1[w][h] == 6:
                            Mimic(h * 10 + 50, w * 10 + 50).draw(screen)
                        elif level1[w][h] == 7:
                            Boss(h * 10 + 50, w * 10 + 50).draw(screen)
                        if w == y and h == x:
                            Player(x * 10 + 50, y * 10 + 50).draw(screen)
                        if not escape and level1[y][x] == 5:
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                            in_fight = True
                            init_enemy = True
                            x_enemy, y_enemy = y, x

            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f"hp: {hp} / 7", True, (255, 255, 255)), (900, 20))
            f_text = n_text(text)
            for line in range(len(f_text)):
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f_text[line], True, (255, 255, 255)), (900, 50 + line * 30))
            if in_fight:
                if hp <= 0:  # проверка на смерть
                    window = 4
                if init_enemy and type_enemy != 6:
                    init_enemy = False
                    generate = generate_name_enemy()
                    text += generate[0]
                    image_enemy = generate[1]
                    hp_enemy = enemies[enemy_id].hp
                    damage_enemy = generate[3]
                    chance_enemy = generate[4]
                    chance_escape = generate[5]
                    reward = generate[6]
                    motion = True
                elif init_enemy and type_enemy == 6:  # наш противник - мимик
                    init_enemy = False
                    text += 'На вас напал мимик! '
                    image_enemy = mimic_img
                    hp_enemy = 4
                    damage_enemy = 4
                    chance_enemy = 55
                    chance_escape = 35
                    reward = 10
                    motion = True
                screen.blit(image_enemy, (20, 20))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f' | enemy hp: {hp_enemy}', True, (255, 255, 255)), (1000, 20))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render('Выберите действие', False, (255, 255, 255)), (900, 450))
                # Атака(урон)=0 Еда=1
                # Побег=2       Защита=3

                if in_food:
                    if 'bread' in food or 'bread_w' in food or 'beer' in food or 'small_potion' in food\
                            or 'big_potion' in food:
                        if 'bread' in food:
                            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                        .render(f'Bread: {food["bread"]}', False, (255, 255, 255)), (900, 480))
                        if 'bread_w' in food:
                            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                        .render(f'Bread: {food["bread_w"]}', False, (255, 255, 255)), (1200, 480))
                        if 'small_potion' in food:
                            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                        .render(f'S Potion: {food["small_potion"]}', False, (255, 255, 255)),
                                        (900, 520))
                        if 'big_potion' in food:
                            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                        .render(f'B Potion: {food["big_potion"]}', False, (255, 255, 255)), (1200, 520))
                    else:
                        in_food = False
                else:
                    screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                .render(f'{name}: {damage}', False, (255, 255, 255)), (900, 480))
                    screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                .render('Еда', False, (255, 255, 255)), (1200, 480))
                    screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                .render('Сбежать', False, (255, 255, 255)), (900, 520))
                    screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                                .render('Защита', False, (255, 255, 255)), (1200, 520))

                if choice == 0:
                    pygame.draw.line(screen, (153, 0, 0), (900, 480), (900, 500), 4)
                elif choice == 1:
                    pygame.draw.line(screen, (153, 0, 0), (1200, 480), (1200, 500), 4)
                elif choice == 2:
                    pygame.draw.line(screen, (153, 0, 0), (900, 520), (900, 540), 4)
                elif choice == 3:
                    pygame.draw.line(screen, (153, 0, 0), (1200, 520), (1200, 540), 4)
                if hp_enemy <= 0:
                    print(level1[y][x])
                    print(enemy_id)
                    if len(enemies) - 1 >= enemy_id:
                        enemies.pop(enemy_id)
                    level1[y][x] = 0
                    print(level1[y][x])
                    in_fight = False
                    database.set_money(database.get_money() + reward)
                if motion:
                    if action == 0:  # проводим урон
                        action = -1
                        if probability(random.randint(90, 100)):
                            hp_enemy -= damage
                            text += f'Вы попали: -{damage}! '
                            motion = False
                        else:
                            text += 'Промах! '
                            motion = False
                    elif action == 2:  # пытаемся сбежать
                        action = -1
                        if probability(chance_escape):
                            text += 'Побег успешен! '
                            escape = True
                            in_fight = False
                        else:
                            text += 'Побег не удался! '
                            motion = False
                    elif action == 3:  # защищаемся
                        action = -1
                        pass
                else:  # ход противника
                    time.sleep(.5)
                    if probability(chance_enemy):
                        # атака прошла успешно
                        hp -= damage_enemy
                        text += f'Противник попал: -{damage_enemy}! '
                        motion = True
                    else:
                        text += 'Противник промахнулся! '
                        motion = True
        elif window == 3:  # отображение товаров у торговца
            screen.blit(field_choice, (500, 600))
            if type_trader == 1:  # weapons
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Дубина (10 монет)', False, (255, 255, 255)), (550, 650))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Меч (30 монет)', False, (255, 255, 255)), (550, 700))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Святой меч (40 монет)', False, (255, 255, 255)), (550, 750))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Ночная катана (90 монет)', False, (255, 255, 255)), (550, 800))
            elif type_trader == 0:  # food
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Хлеб (5 монет)', False, (255, 255, 255)), (550, 650))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Хлеб с ветчиной (15 монет)', False, (255, 255, 255)), (550, 700))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Малое зелье (50 монет)', False, (255, 255, 255)), (550, 750))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Большое зелье (70 монет)', False, (255, 255, 255)), (550, 800))
            elif type_trader == 2:  # others
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Деревяный щит (10 монет)', False, (255, 255, 255)), (550, 650))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Железный щит (25 монет)', False, (255, 255, 255)), (550, 700))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Сверкающие пятки  (50 монет)', False, (255, 255, 255)), (550, 750))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f'Денежный тотем  (70 монет)', False, (255, 255, 255)), (550, 800))
            if exit_button.draw():
                window = 1
            for index in range(len(plus_buttons2)):
                b = plus_buttons2[index]
                b.draw()
                b.enabled = True
                if b.check_click():
                    b.enabled = False
                    if type_trader == 1:
                        if index == 0:
                            if database.get_money() >= 10:
                                database.set_money(database.get_money() - 10)
                                database.set_weapons(2)
                        elif index == 1:
                            if database.get_money() >= 30:
                                database.set_money(database.get_money() - 30)
                                database.set_weapons(3)
                        elif index == 2:
                            if database.get_money() >= 40:
                                database.set_money(database.get_money() - 40)
                                database.set_weapons(4)
                        elif index == 3:
                            if database.get_money() >= 90:
                                database.set_money(database.get_money() - 90)
                                database.set_weapons(5)
                    elif type_trader == 0:
                        if index == 0:
                            if database.get_money() >= 5:
                                database.set_money(database.get_money() - 5)
                                foods = to_normal_foods(database.get_foods())
                                if 'bread' in foods:
                                    foods['bread'] += 1
                                else:
                                    foods['bread'] = 1
                                database.set_foods(str(foods))
                        elif index == 1:
                            if database.get_money() >= 15:
                                database.set_money(database.get_money() - 15)
                                foods = to_normal_foods(database.get_foods())
                                if 'bread_w' in foods:
                                    foods['bread_w'] += 1
                                else:
                                    foods['bread_w'] = 1
                                database.set_foods(str(foods))
                        elif index == 2:
                            if database.get_money() >= 50:
                                database.set_money(database.get_money() - 50)
                                foods = to_normal_foods(database.get_foods())
                                if 'small_potion' in foods:
                                    foods['small_potion'] += 1
                                else:
                                    foods['small_potion'] = 1
                                database.set_foods(str(foods))
                        elif index == 3:
                            if database.get_money() >= 70:
                                database.set_money(database.get_money() - 70)
                                foods = to_normal_foods(database.get_foods())
                                if 'big_potion' in foods:
                                    foods['big_potion'] += 1
                                else:
                                    foods['big_potion'] = 1
                                database.set_foods(str(foods))
                    elif type_trader == 1:
                        if index == 0:
                            if database.get_money() >= 10:
                                others = to_normal_others(database.get_others())
                                others['shield'] = 5
                                database.set_others(str(others))
                        elif index == 1:
                            if database.get_money() >= 25:
                                others = to_normal_others(database.get_others())
                                others['shield'] = 12
                                database.set_others(str(others))
                        elif index == 2:
                            if database.get_money() >= 50:
                                others = to_normal_others(database.get_others())
                                others['boots'] = 25
                                database.set_others(str(others))
                        elif index == 3:
                            if database.get_money() >= 70:
                                others = to_normal_others(database.get_others())
                                others['totem'] = True
                                database.set_others(str(others))
                    money_debug = True
        elif window == 4:  # обработка проигрыша
            screen.blit(only_black, (0, 0))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 200)
                        .render(f'Вы проиграли!', False, (89, 15, 21)), (450, 500))
            database.reload()

        for event in pygame.event.get():  # Слушатель на нажатия кнопки
            if event.type == pygame.QUIT:
                exit()
                pygame.quit()
                break
            if event.type == pygame.K_ESCAPE:
                pygame.display.set_mode((1280, 720))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11 and False:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                if window == 2 and event.key == pygame.K_s:
                    if y + 1 < le_x and level1[y + 1][x] != 1:
                        escape = False
                        y += 1
                        if level1[y][x] == 6:  # mimic
                            in_fight = True
                            init_enemy = True
                            type_enemy = 6
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                        for e in enemies:  # передвижение противников
                            m_x = len(level1)
                            m_y = len(level1[0])
                            if m_x == x and m_y == y:
                                level1[y][x] = 0
                                enemies.remove(e)
                            else:
                                moves = [(e.x, e.y)]
                                if e.x + 1 < m_x and level1[e.x + 1][e.y] == 0:
                                    moves.append((e.x + 1, e.y))
                                if e.x - 1 >= 0 and level1[e.x - 1][e.y] == 0:
                                    moves.append((e.x - 1, e.y))
                                if e.y + 1 < m_y and level1[e.x][e.y + 1] == 0:
                                    moves.append((e.x, e.y + 1))
                                if e.y - 1 >= 0 and level1[e.x][e.y - 1] == 0:
                                    moves.append((e.x, e.y - 1))
                                if len(moves) >= 1:
                                    ran = random.randint(0, len(moves) - 1)
                                    level1[e.x][e.y] = 0
                                    level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                                    e.set_coord(moves[ran][0], moves[ran][1])
                if window == 2 and event.key == pygame.K_w:
                    if level1[y - 1][x] != 1 and y - 1 >= 0:
                        escape = False
                        y -= 1
                        # if level1[y][x] == 5:  # enemy
                        #     in_fight = True
                        #     init_enemy = True
                        #     type_enemy = 5
                        if level1[y][x] == 6:  # mimic
                            in_fight = True
                            init_enemy = True
                            type_enemy = 6
                        # elif level1[y][x] == 7:  # boss
                        #     in_fight = True
                        #     init_enemy = True
                        #     type_enemy = 7
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                        for e in enemies:  # передвижение противников
                            m_x = len(level1)
                            m_y = len(level1[0])
                            if m_x == x and m_y == y:
                                level1[y][x] = 0
                                enemies.remove(e)
                            else:
                                moves = [(e.x, e.y)]
                                if e.x + 1 < m_x and level1[e.x + 1][e.y] == 0:
                                    moves.append((e.x + 1, e.y))
                                if e.x - 1 >= 0 and level1[e.x - 1][e.y] == 0:
                                    moves.append((e.x - 1, e.y))
                                if e.y + 1 < m_y and level1[e.x][e.y + 1] == 0:
                                    moves.append((e.x, e.y + 1))
                                if e.y - 1 >= 0 and level1[e.x][e.y - 1] == 0:
                                    moves.append((e.x, e.y - 1))
                                if len(moves) >= 1:
                                    ran = random.randint(0, len(moves) - 1)
                                    level1[e.x][e.y] = 0
                                    level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                                    e.set_coord(moves[ran][0], moves[ran][1])
                if window == 2 and event.key == pygame.K_d:
                    if x + 1 < le_y and level1[y][x + 1] != 1:
                        escape = False
                        x += 1
                        # if level1[y][x] == 5:  # enemy
                        #     in_fight = True
                        #     type_enemy = 5
                        if level1[y][x] == 6:  # mimic
                            in_fight = True
                            init_enemy = True
                            type_enemy = 6
                        # elif level1[y][x] == 7:  # boss
                        #     in_fight = True
                        #     type_enemy = 7
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                        for e in enemies:  # передвижение противников
                            m_x = len(level1)
                            m_y = len(level1[0])
                            if m_x == x and m_y == y:
                                level1[y][x] = 0
                                enemies.remove(e)
                            else:
                                moves = [(e.x, e.y)]
                                if e.x + 1 < m_x and level1[e.x + 1][e.y] == 0:
                                    moves.append((e.x + 1, e.y))
                                if e.x - 1 >= 0 and level1[e.x - 1][e.y] == 0:
                                    moves.append((e.x - 1, e.y))
                                if e.y + 1 < m_y and level1[e.x][e.y + 1] == 0:
                                    moves.append((e.x, e.y + 1))
                                if e.y - 1 >= 0 and level1[e.x][e.y - 1] == 0:
                                    moves.append((e.x, e.y - 1))
                                if len(moves) >= 1:
                                    ran = random.randint(0, len(moves) - 1)
                                    level1[e.x][e.y] = 0
                                    level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                                    e.set_coord(moves[ran][0], moves[ran][1])
                if window == 2 and event.key == pygame.K_a:
                    if level1[y][x - 1] != 1 and x - 1 >= 0:
                        escape = False
                        x -= 1
                        # if level1[y][x] == 5:  # enemy
                        #     in_fight = True
                        #     type_enemy = 5
                        if level1[y][x] == 6:  # mimic
                            in_fight = True
                            init_enemy = True
                            type_enemy = 6
                        # elif level1[y][x] == 7:  # boss
                        #     in_fight = True
                        #     type_enemy = 7
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                        for e in enemies:  # передвижение противников
                            m_x = len(level1)
                            m_y = len(level1[0])
                            if m_x == x and m_y == y:
                                level1[y][x] = 0
                                enemies.remove(e)
                            else:
                                moves = [(e.x, e.y)]
                                if e.x + 1 < m_x and level1[e.x + 1][e.y] == 0:
                                    moves.append((e.x + 1, e.y))
                                if e.x - 1 >= 0 and level1[e.x - 1][e.y] == 0:
                                    moves.append((e.x - 1, e.y))
                                if e.y + 1 < m_y and level1[e.x][e.y + 1] == 0:
                                    moves.append((e.x, e.y + 1))
                                if e.y - 1 >= 0 and level1[e.x][e.y - 1] == 0:
                                    moves.append((e.x, e.y - 1))
                                if len(moves) >= 1:
                                    ran = random.randint(0, len(moves) - 1)
                                    level1[e.x][e.y] = 0
                                    level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                                    e.set_coord(moves[ran][0], moves[ran][1])
                if window == 2 and in_fight:
                    if event.key == pygame.K_RIGHT:
                        if choice < 3:
                            choice += 1
                        else:
                            choice = 0
                    elif event.key == pygame.K_DOWN:
                        if choice == 0:
                            choice = 2
                        elif choice == 1:
                            choice = 3
                        elif choice == 2:
                            choice = 0
                        else:
                            choice = 1
                    elif event.key == pygame.K_LEFT:
                        if choice > 0:
                            choice -= 1
                        else:
                            choice = 3
                    elif event.key == pygame.K_UP:
                        if choice == 0:
                            choice = 2
                        elif choice == 1:
                            choice = 3
                        elif choice == 2:
                            choice = 0
                        elif choice == 3:
                            choice = 1
                    elif event.key == pygame.K_RETURN:
                        action = choice
                        if not in_food and action == 1:
                            in_food = True
                    elif event.key == pygame.K_BACKSPACE:
                        if in_food:
                            in_food = False

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()  # Инициализация
    pygame.display.set_caption('Throne of Shadows')
    main_module()

