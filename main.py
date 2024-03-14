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
print(le_x, le_y)
print(level1)
text = 'Привет, это проверка длинного и осмысленного текста. Поэтому, привет ещё раз! Невероятно и удивительно, невероятно и удивительно, невероятно и...'
in_fight = True
type_enemy = 0  # 5 - st. enemy; 6 - mimic; 7 - boss;
choice = 0
action = -1
# 0 1
# 2 3
action_stage = 1


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
        type_enemy, choice, action
    from support import button_new_game, button_continue, \
        button_quit, background, wait_fullscreen, button_cave, \
        cave_img, button_castle, castle_img, button_ferm, ferm_img, \
        button_wizard, wizard_img, only_black, n_text, weapon_to_name_and_damage,\
        to_normal_foods

    threading.Thread(target=show_start_buttons(),
                     args=(1,), daemon=True).start()

    while game_cycle:  # Обработка работы pygame
        clock.tick(15)
        if window == 0:
            if button_new_game.draw():
                print("NEW GAME")
                database.reload()  # Очищение базы данных
                window = 1
                wait_fullscreen = True
                fell_alive = True
                hp = 7
            if button_continue.draw():
                print("CONTINUE")
                window = 1
                wait_fullscreen = True
                if database.get_existing() == 0:
                    # create new game
                    pass
            if button_quit.draw():
                print("QUIT")
                exit()
                pygame.quit()
                break
        elif window == 1:
            if wait_fullscreen:
                pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                wait_fullscreen = False
            if button_cave.draw():  # Нажатие на кнопку cave, запуск игры
                screen.blit(cave_img, (0, 0))
                window = 2
            elif button_castle.draw():
                screen.blit(castle_img, (0, 0))
            elif button_ferm.draw():
                screen.blit(ferm_img, (0, 0))
            elif button_wizard.draw():
                screen.blit(wizard_img, (0, 0))
            else:
                if not button_cave.listener(screen, cave_img) \
                        and not button_castle.listener(screen, castle_img) \
                        and not button_ferm.listener(screen, ferm_img) \
                        and not button_wizard.listener(screen, wizard_img):
                    screen.blit(background, (0, 0))
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
            f_text = n_text(text)
            for line in range(len(f_text)):
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render(f_text[line], True, (255, 255, 255)), (900, 50 + line * 30))
            if in_fight:
                screen.blit(pygame.font.SysFont('assets/font.ttf', 36)
                            .render('Выберите действие', False, (255, 255, 255)), (900, 450))
                # Атака(урон)=0 Еда=1
                # Побег=2       Защита=3
                name, damage = weapon_to_name_and_damage(database.get_weapons())
                food = to_normal_foods(database.get_foods())
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
                    elif event.key == pygame.K_KP_ENTER:
                        action = choice

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()  # Инициализация
    pygame.display.set_caption('Throne of Shadows')
    main_module()

