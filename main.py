from database import Database
import pygame
import threading
import random
import time

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


if __name__ == '__main__':
    pygame.init()  # Инициализация
    pygame.display.set_caption('Throne of Shadows')
    from support import button_new_game, button_continue, button_quit

    threading.Thread(target=show_start_buttons(),
                     args=(1,), daemon=True).start()

    while True:  # Обработка работы pygame
        clock.tick(20)
        if window == 0:
            if button_new_game.draw():
                print("NEW GAME")
                database.reload()  # Очищение базы данных
                window = 1
            if button_continue.draw():
                print("CONTINUE")
                window = 1
                if database.get_existing() == 0:
                    # create new game
                    pass
            if button_quit.draw():
                print("QUIT")
                exit()
                pygame.quit()
                break
        elif window == 1:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            background = pygame.image.load('assets/map/s.png')
            screen.blit(background, (0, 0))

        for event in pygame.event.get():  # Слушатель на нажатия кнопки
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
