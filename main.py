import time
import generator
from database import Database
import pygame
from entity import Wall, Player, Enemy, Chest, Mimic, Boss, Exit, SBoss
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
long_escape = 0
money_render_state = False


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
        reward, motion, damage_enemy, x_enemy, y_enemy, enemy_id, escape, \
        money_render_state, long_escape
    from support import button_new_game, button_continue, \
        button_quit, background, wait_fullscreen, button_cave, \
        cave_img, button_castle, castle_img, button_ferm, ferm_img, \
        button_wizard, wizard_img, only_black, n_text, weapon_to_name_and_damage, \
        to_normal_foods, generate_money_from_chest, field_choice, exit_button, \
        Button, to_normal_others, ViewEnemy, generate_name_enemy, probability, \
        mimic_img, dragon_img
    weapon_id = database.get_weapons()
    weapon_debug = True
    food = to_normal_foods(database.get_foods())
    food_debug = True
    others = to_normal_others(database.get_others())
    others_debug = True
    name, damage = weapon_to_name_and_damage(weapon_id)
    happy = database.get_happy()
    happy_debug = True
    money = database.get_money()
    debt = database.get_debt()
    debt_debug = True
    money_debug = True
    plus_buttons2 = [
        Button(' +', 1004, 640, screen=screen, font_size=50),
        Button(' +', 1004, 690, screen=screen, font_size=50),
        Button(' +', 1004, 740, screen=screen, font_size=50),
        Button(' +', 1004, 790, screen=screen, font_size=50),
    ]

    enemies = [
        ViewEnemy(7, 24, len(level1) - 3, len(level1[0]) - 3),
        ViewEnemy(7, 24, 2, len(level1[0]) - 3),
        ViewEnemy(7, 24, len(level1) - 3, 2),
        ViewEnemy(10, 30, len(level1) - 7, 29)
    ]
    for i in range(30):
        x1 = random.randint(2, len(level1) - 3)
        y1 = random.randint(2, len(level1) - 3)
        if level1[x1][y1] == 0:
            enemies.append(ViewEnemy(5, random.randint(2, 4), x1, y1))
    for enemy in enemies:
        if enemy.get_id() == 5:
            level1[enemy.x][enemy.y] = 5
        elif enemy.get_id() == 7:
            level1[enemy.x][enemy.y] = 7
        elif enemy.get_id() == 10:
            level1[enemy.x][enemy.y] = 10
    level1[len(level1) - 2][len(level1[0]) - 2] = 8  # генерация выхода
    level1[len(level1) - 2][1] = 8
    level1[1][len(level1) - 2] = 8
    to_main_menu = Button('Выход в главное меню', 1610, 5, width=285, height=38, screen=screen)
    to_main_menu2 = Button('Выход в главное меню', 800, 700,
                           width=285, height=38, screen=screen, color=(33, 41, 55))
    to_main_continue = Button('Продолжить', 800, 700,
                              width=200, height=38, screen=screen, color=(33, 41, 55))
    while game_cycle:  # Обработка работы pygame
        clock.tick(15)
        if weapon_debug:
            name, damage = weapon_to_name_and_damage(database.get_weapons())
            weapon_debug = False
        if money_debug:
            money = database.get_money()
            money_debug = False
        if food_debug:
            food_debug = False
            food = to_normal_foods(database.get_foods())
        if others_debug:
            others_debug = False
            others = to_normal_others(database.get_others())
        if window == 0:
            show_start_buttons()
            if button_new_game.draw():
                database.reload()  # Очищение базы данных
                window = 1
                wait_fullscreen = True
            if button_continue.draw():
                if database.get_existing() == 0:  # create new game
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
            money_render_state = False
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

            if happy_debug:  # обновляем уровень счастья
                happy = database.get_happy()
                database.set_debt(database.get_debt() * 2)
                m = database.get_money()
                if m - database.get_debt() < 0:
                    database.set_happy(database.get_happy() // 2)
                else:
                    database.set_money(database.get_money() - database.get_debt())
                    if database.get_happy() * 2 <= 100:
                        database.set_happy(database.get_happy() * 2)
                    money_debug = True
                if happy <= 0:
                    window = 4
                happy_debug = False

            if debt_debug:  # обновляем уровень долга
                debt = database.get_debt()
                debt_debug = False

            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f'Уровень счастья граждан: {happy}', False, (255, 255, 255)), (10, 10))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f'Долг: {debt}', False, (255, 0, 0)), (10, 62))
            money_render_state = True
            to_main_menu.draw()
            to_main_menu.enabled = True
            if to_main_menu.check_click():
                to_main_menu.enabled = False
                window = 0
                pygame.display.set_mode((1280, 720))
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
                        elif level1[w][h] == 8:  # выход
                            happy_debug = True
                            Exit(h * 10 + 50, w * 10 + 50).draw(screen)
                        elif level1[w][h] == 10:  # супер босс
                            SBoss(h * 10 + 50, w * 10 + 50).draw(screen)
                        if w == y and h == x:
                            Player(x * 10 + 50, y * 10 + 50).draw(screen)
                        if level1[w][h] == 8 and w == y and h == x:
                            window = 1
                            money_debug = True
                        if not escape and (level1[y][x] == 5 or level1[y][x] == 6 or level1[y][x] == 7):
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                            in_fight = True
                            init_enemy = True
                            # type_enemy = level1[y][x]
                            x_enemy, y_enemy = y, x

            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f"hp: {hp} / 7", True, (255, 255, 255)), (900, 20))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f"money: {money}", True, (255, 255, 255)), (1000, 20))
            f_text = n_text(text)
            for line in range(len(f_text)):
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f_text[line], True, (255, 255, 255)), (900, 50 + line * 30))
            if in_fight:
                if hp <= 0:  # проверка на смерть
                    window = 4
                if init_enemy and level1[y][x] == 5:
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
                elif init_enemy and level1[y][x] == 6:  # наш противник - мимик
                    init_enemy = False
                    text += 'На вас напал мимик! '
                    image_enemy = mimic_img
                    hp_enemy = 4
                    damage_enemy = 4
                    chance_enemy = 55
                    chance_escape = 35
                    reward = 10
                    motion = True
                elif init_enemy and level1[y][x] == 7:
                    init_enemy = False
                    text += 'Вы угодили в лапы Дракона! '
                    image_enemy = dragon_img
                    hp_enemy = 24
                    damage_enemy = 6
                    chance_enemy = 90
                    chance_escape = 1
                    reward = 100
                    motion = True
                if image_enemy is None:
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
                screen.blit(image_enemy, (20, 20))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f' | enemy hp: {hp_enemy}', True, (255, 255, 255)), (1200, 20))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render('Выберите действие', False, (255, 255, 255)), (900, 450))
                # Атака(урон)=0 Еда=1
                # Побег=2       Защита=3

                if in_food:
                    food_debug = True
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
                    if len(enemies) - 1 >= enemy_id:
                        enemies.pop(enemy_id)
                    level1[y][x] = 0
                    in_fight = False
                    database.set_money(database.get_money() + reward)
                    money_debug = True
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
                        if probability(chance_escape) or ('boots' in others and probability(chance_escape + int(others['boots']))):
                            text += 'Побег успешен! '
                            escape = True
                            in_fight = False
                            long_escape = 4
                        else:
                            text += 'Побег не удался! '
                            motion = False
                    elif action == 3:  # защищаемся
                        action = -1
                        pass
                else:  # ход противника
                    time.sleep(.5)
                    if probability(chance_enemy) or ('shield' in others and probability(100 - int(others['shield']))):
                        # атака прошла успешно
                        hp -= damage_enemy
                        text += f'Противник попал: -{damage_enemy}! '
                        motion = True
                    else:
                        text += 'Противник промахнулся! '
                        motion = True
                    others_debug = True
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
                    if type_trader == 0:
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
                    if type_trader == 2:
                        if index == 0:
                            if database.get_money() >= 10:
                                others = to_normal_others(database.get_others())
                                others['shield'] = 5
                                database.set_others(str(others))
                                database.set_money(database.get_money() - 10)
                        elif index == 1:
                            if database.get_money() >= 25:
                                others = to_normal_others(database.get_others())
                                others['shield'] = 12
                                database.set_others(str(others))
                                database.set_money(database.get_money() - 25)
                        elif index == 2:
                            if database.get_money() >= 50:
                                others = to_normal_others(database.get_others())
                                others['boots'] = 25
                                database.set_others(str(others))
                                database.set_money(database.get_money() - 50)
                        elif index == 3:
                            if database.get_money() >= 70:
                                others = to_normal_others(database.get_others())
                                others['totem'] = 1
                                database.set_others(str(others))
                                database.set_money(database.get_money() - 70)
                    money_debug = True
                    others_debug = True
                    weapon_debug = True
        elif window == 4:  # обработка проигрыша
            if 'totem' in others and int(others['totem']) and probability(50):
                others['totem'] = 0
                database.set_others(str(others))
                window = 1
                # ПРОИГРЫВАЕМ ЗВУК СПАСЕНИЯ
            else:
                screen.blit(only_black, (0, 0))
                screen.blit(pygame.font.SysFont('assets/font.ttf', 200)
                            .render(f'Вы проиграли!', False, (89, 15, 21)), (450, 500))
                database.reload()
                to_main_menu2.draw()
                to_main_menu2.enabled = True
                if to_main_menu2.check_click():
                    to_main_menu2.enabled = False
                    window = 0
                    pygame.display.set_mode((1280, 720))
        if window == 1 and money_render_state or window == 3:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 36, 180, 22))
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f'Капитал: {money}', False, (255, 255, 255)), (10, 36))

        for event in pygame.event.get():  # Слушатель на нажатия кнопок
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
                        if level1[y][x] == 5:
                            type_enemy = 5
                            in_fight = True
                            init_enemy = True
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                        if level1[y][x] == 6:  # mimic
                            type_enemy = 6
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 7:  # boss
                            type_enemy = 7
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                            money_debug = True
                        if not in_fight:
                            enemies_move(enemies)  # передвижение противников
                if window == 2 and event.key == pygame.K_w:
                    if level1[y - 1][x] != 1 and y - 1 >= 0:
                        escape = False
                        y -= 1
                        if level1[y][x] == 5:
                            type_enemy = 5
                            in_fight = True
                            init_enemy = True
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                        if level1[y][x] == 6:  # mimic
                            type_enemy = 6
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 7:
                            type_enemy = 7
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                            money_debug = True
                        if not in_fight:
                            enemies_move(enemies)  # передвижение противников
                if window == 2 and event.key == pygame.K_d:
                    if x + 1 < le_y and level1[y][x + 1] != 1:
                        escape = False
                        x += 1
                        if level1[y][x] == 5:
                            type_enemy = 5
                            in_fight = True
                            init_enemy = True
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                        if level1[y][x] == 6:  # mimic
                            type_enemy = 6
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 7:
                            type_enemy = 7
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                            money_debug = True
                        if not in_fight:
                            enemies_move(enemies)  # передвижение противников
                if window == 2 and event.key == pygame.K_a:
                    if level1[y][x - 1] != 1 and x - 1 >= 0:
                        escape = False
                        x -= 1
                        if level1[y][x] == 5:
                            type_enemy = 5
                            in_fight = True
                            init_enemy = True
                            for e in range(len(enemies)):
                                if enemies[e].x == y and enemies[e].y == x:
                                    enemy_id = e
                                    break
                        if level1[y][x] == 6:  # mimic
                            type_enemy = 6
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 7:
                            type_enemy = 7
                            in_fight = True
                            init_enemy = True
                        if level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                            money_debug = True
                        if not in_fight:
                            enemies_move(enemies)  # передвижение противников
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
                            action = -1
                        if in_food:
                            time_foods = to_normal_foods(database.get_foods())
                            if action == 0:
                                if 'bread' in time_foods:
                                    if time_foods['bread'] >= 1:
                                        if probability(5):
                                            if hp < 7:
                                                text += 'Вы успешно восстановили жизнь! '
                                                hp += 1
                                            else:
                                                text += 'Вы б восстановили жизнь, да и так сыты! '
                                        else:
                                            text += 'Хлеб ничего вам не дал... '
                                        time_foods['bread'] -= 1
                                        database.set_foods(str(time_foods))
                                action = -1
                                food_debug = True
                            elif action == 1:
                                if 'bread_w' in time_foods:
                                    if time_foods['bread_w'] >= 1:
                                        if probability(7):
                                            if hp < 7:
                                                text += 'Вы успешно восстановили жизнь! '
                                                hp += 1
                                            else:
                                                text += ('Хотелось проверить, получится ли иметь больше жизней, '
                                                         'чем позволено игрой? Но вы же не кот! ')
                                        else:
                                            text += 'Безуспешно, но вкусно... '
                                        time_foods['bread_w'] -= 1
                                        database.set_foods(str(time_foods))
                                action = -1
                                food_debug = True
                            elif action == 2:
                                if 'small_potion' in time_foods:
                                    if time_foods['small_potion'] >= 1:
                                        if hp < 7:
                                            text += 'Восстановлена одна жизнь! '
                                            hp += 1
                                        else:
                                            text += 'Увы, но вы потратили зелье впустую! '
                                        time_foods['small_potion'] -= 1
                                        database.set_foods(str(time_foods))
                                action = -1
                                food_debug = True
                            elif action == 3:
                                if 'big_potion' in time_foods and time_foods['big_potion'] > 0:
                                    if hp < 7:
                                        text += 'Восстановлено! '
                                        if hp == 6:
                                            hp = 7
                                        else:
                                            hp += 2
                                    else:
                                        text += 'Какое расточительство! Жизни-то у вас полные! '
                                    time_foods['big_potion'] -= 1
                                    database.set_foods(str(time_foods))
                                action = -1
                                food_debug = True
                    elif event.key == pygame.K_BACKSPACE:
                        if in_food:
                            in_food = False

        pygame.display.update()


def enemies_move(enemies):  # функция для обработки передвижения противников
    global level1, x, y, escape, long_escape
    for e in enemies:
        m_x = len(level1)
        m_y = len(level1[0])
        if m_x == x and m_y == y:
            level1[y][x] = 0
            enemies.remove(e)
        else:
            if e.get_id() == 5:
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
            elif e.get_id() == 7 and long_escape == 0:
                moves = []
                if level1[e.x - 1][e.y] == 1 and level1[e.x][e.y - 1] == 1 and e.previous != [e.x + 1, e.y]:
                    level1[e.x][e.y] = 0
                    level1[e.x + 1][e.y] = e.get_id()
                    e.set_coord(e.x + 1, e.y)
                elif level1[e.x - 1][e.y] == 1 and level1[e.x][e.y - 1] == 1 and e.previous == [e.x + 1, e.y]:
                    level1[e.x][e.y] = 0
                    level1[e.x][e.y + 1] = e.get_id()
                    e.set_coord(e.x, e.y + 1)
                else:
                    if e.x > y and level1[e.x - 1][e.y] == 0:
                        moves.append((e.x - 1, e.y))
                    if e.y > x and level1[e.x][e.y - 1] == 0:
                        moves.append((e.x, e.y - 1))
                    if e.x < y and level1[e.x + 1][e.y] == 0:
                        moves.append((e.x + 1, e.y))
                    if e.y < x and level1[e.x][e.y + 1] == 0:
                        moves.append((e.x, e.y + 1))
                    if level1[e.x + 1][e.y] == 1 and level1[e.x][e.y - 1] == 1:
                        moves.append((e.x, e.y + 1))
                    if len(moves) >= 1:
                        ran = random.randint(0, len(moves) - 1)
                        level1[e.x][e.y] = 0
                        level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                        e.set_coord(moves[ran][0], moves[ran][1])
                    else:
                        moves = [(e.x, e.y)]
                        if e.x + 1 < m_x and level1[e.x + 1][e.y] == 0 and e.previous != [e.x + 1, e.y]:
                            moves.append((e.x + 1, e.y))
                        if e.x - 1 >= 0 and level1[e.x - 1][e.y] == 0 and e.previous != [e.x - 1, e.y]:
                            moves.append((e.x - 1, e.y))
                        if e.y + 1 < m_y and level1[e.x][e.y + 1] == 0 and e.previous != [e.x, e.y + 1]:
                            moves.append((e.x, e.y + 1))
                        if e.y - 1 >= 0 and level1[e.x][e.y - 1] == 0 and e.previous != [e.x, e.y - 1]:
                            moves.append((e.x, e.y - 1))
                        if len(moves) >= 1:
                            ran = random.randint(0, len(moves) - 1)
                            level1[e.x][e.y] = 0
                            level1[moves[ran][0]][moves[ran][1]] = e.get_id()
                            e.set_coord(moves[ran][0], moves[ran][1])
            elif e.get_id() == 7 and long_escape != 0:
                long_escape -= 1

if __name__ == '__main__':
    pygame.init()  # Инициализация
    pygame.display.set_caption('Throne of Shadows')
    main_module()

