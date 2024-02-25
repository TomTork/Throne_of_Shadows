from database import Database
import pygame
import threading

database = Database()
window = 0  # Переменная, хранящая состояние окна
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


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
    global window, screen, database, clock
    from support import button_new_game, button_continue, \
        button_quit, background, wait_fullscreen, button_cave, \
        cave_img, button_castle, castle_img, button_ferm, ferm_img, \
        button_wizard, wizard_img, only_black

    threading.Thread(target=show_start_buttons(),
                     args=(1,), daemon=True).start()

    while True:  # Обработка работы pygame
        clock.tick(20)
        if window == 0:
            if button_new_game.draw():
                print("NEW GAME")
                database.reload()  # Очищение базы данных
                window = 1
                wait_fullscreen = True
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

        for event in pygame.event.get():  # Слушатель на нажатия кнопки
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("W!")
            if event.type == pygame.QUIT:
                exit()
                pygame.quit()
                break
            if event.type == pygame.K_ESCAPE:
                pygame.display.set_mode((1280, 720))
            if event.type == pygame.K_F11:
                print("TRUE")
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()  # Инициализация
    pygame.display.set_caption('Throne of Shadows')
    main_module()

