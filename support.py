import random
import pygame


# Вычисление вероятности какого-либо события
def probability(chance) -> bool:
    random_number = random.randint(1, 100)
    if random_number <= chance:
        return True
    return False


b_draw = False  # Параметр, служащий для НЕ переотрисовки кнопок


class Button2:  # Создание и отображение кнопки
    def __init__(self, x1=10, y1=0, image=None, scale=0.8):
        width, height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.midleft = (x1, y1)
        self.clicked = False

    def draw(self):
        global b_draw
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


def get_real_image(image, scale=0.8):  # Функция для изменения размера кнопки
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))


# Константы:
new_game_img = get_real_image(pygame.image.load('assets/buttons/button_new_game.png').convert_alpha())
button_new_game = Button2(20, y1=136, image=new_game_img, scale=1)

continue_img = get_real_image(pygame.image.load('assets/buttons/button_continue.png').convert_alpha())
button_continue = Button2(20, y1=232, image=continue_img, scale=1)

quit_img = get_real_image(pygame.image.load('assets/buttons/button_quit.png').convert_alpha())
button_quit = Button2(20, y1=338, image=quit_img, scale=1)