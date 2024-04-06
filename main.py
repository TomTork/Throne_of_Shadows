import generator
from database import Database
import pygame
import threading
from entity import Wall, Player, Enemy, Chest, Mimic, Boss

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

enemy = [1, '', 100]
# 0 1
# 2 3


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
        type_enemy, choice, action, text, in_food, type_trader
    from support import button_new_game, button_continue, \
        button_quit, background, wait_fullscreen, button_cave, \
        cave_img, button_castle, castle_img, button_ferm, ferm_img, \
        button_wizard, wizard_img, only_black, n_text, weapon_to_name_and_damage,\
        to_normal_foods, generate_money_from_chest, field_choice, exit_button,\
        Button, to_normal_others
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
                print("NEW GAME")
                database.reload()  # Очищение базы данных
                window = 1
                wait_fullscreen = True
            if button_continue.draw():
                print("CONTINUE")
                if database.get_existing() == 0:  # create new game
                    database.reload()
                window = 1
                wait_fullscreen = True
            if button_quit.draw():
                print("QUIT")
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
            for w in range(le_x):
                for h in range(le_y):
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
            screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                        .render(f"hp: {hp} / 7", True, (255, 255, 255)), (900, 10))
            f_text = n_text(text)
            for line in range(len(f_text)):
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f_text[line], True, (255, 255, 255)), (900, 50 + line * 30))
            if in_fight:
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
                        y += 1
                        if level1[y][x] == 5:  # enemy
                            in_fight = True
                            type_enemy = 5
                        elif level1[y][x] == 6:  # mimic
                            in_fight = True
                            type_enemy = 6
                        elif level1[y][x] == 7:  # boss
                            in_fight = True
                            type_enemy = 7
                        elif level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                if window == 2 and event.key == pygame.K_w:
                    if level1[y - 1][x] != 1 and y - 1 >= 0:
                        y -= 1
                        if level1[y][x] == 5:  # enemy
                            in_fight = True
                            type_enemy = 5
                        elif level1[y][x] == 6:  # mimic
                            in_fight = True
                            type_enemy = 6
                        elif level1[y][x] == 7:  # boss
                            in_fight = True
                            type_enemy = 7
                        elif level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                if window == 2 and event.key == pygame.K_d:
                    if x + 1 < le_y and level1[y][x + 1] != 1:
                        x += 1
                        if level1[y][x] == 5:  # enemy
                            in_fight = True
                            type_enemy = 5
                        elif level1[y][x] == 6:  # mimic
                            in_fight = True
                            type_enemy = 6
                        elif level1[y][x] == 7:  # boss
                            in_fight = True
                            type_enemy = 7
                        elif level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
                if window == 2 and event.key == pygame.K_a:
                    if level1[y][x - 1] != 1 and x - 1 >= 0:
                        x -= 1
                        if level1[y][x] == 5:  # enemy
                            in_fight = True
                            type_enemy = 5
                        elif level1[y][x] == 6:  # mimic
                            in_fight = True
                            type_enemy = 6
                        elif level1[y][x] == 7:  # boss
                            in_fight = True
                            type_enemy = 7
                        elif level1[y][x] == 2:
                            level1[y][x] = 0
                            money = generate_money_from_chest()
                            database.set_money(database.get_money() + money)
                            text += f'Получено {money}! '
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
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.KSCAN_KP_ENTER:
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

