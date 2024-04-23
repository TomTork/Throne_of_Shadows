import json.decoder
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
        self.width, self.height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.midleft = (x1, y1)
        self.clicked = False
        self.x1 = x1
        self.y1 = y1

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

    def listener(self, screen, image):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(image, (0, 0))
            return True
        return False


class Button:
    def __init__(self, text, x_pos, y_pos, enabled=True, width=48, height=48, screen=None, font_size=36, color='grey'):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.width = width
        self.height = height
        self.screen = screen
        self.font_size = font_size
        self.color = color

    def draw(self):
        button_text = pygame.font.SysFont('assets/font.ttf', self.font_size).render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        pygame.draw.rect(self.screen, self.color, button_rect, 0, 5)
        pygame.draw.rect(self.screen, 'black', button_rect, 2, 5)
        self.screen.blit(button_text, (self.x_pos + 3, self.y_pos + 3))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        if click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        return False


def get_real_image(image, scale=0.8):  # Функция для изменения размера кнопки
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))


def n_text(text: str) -> list:
    if len(text) < 40:
        return [text]
    return [text[i:i+40] for i in range(0, len(text), 40)][-10:]


def weapon_to_name_and_damage(weapon_id: int) -> (str, int):
    match weapon_id:
        case 1:
            return "Кулаки", 1
        case 2:
            return "Дубина", 3
        case 3:
            return "Меч", 6
        case 4:
            return "Святой меч", 7
        case 5:
            return "Ночная катана", 10
        case _:
            return "Ошибка", 0


# "life": <int, ex.: +1; -1>; "vampire": <int, ex.: 1; 0>; "luck": <int, ex.: 1; 0>; "kvant": <int, ex.: 1; 0>;
# "win": <int, ex.: 1; 0>; "maniac": <int, ex.: 1; 0>
def to_normal_tarot(value: str) -> dict:
    if value != '':
        return json.loads(value.replace("'", '"'))
    return dict()


def to_normal_foods(food: str) -> dict:
    if food != '':
        return json.loads(food.replace("'", '"'))
    return dict()


def to_normal_others(others: str) -> dict:
    if others != "":
        return json.loads(others.replace("'", '"'))
    return dict()


def generate_money_from_chest() -> int:
    return random.randint(1, 4)


class ViewEnemy:
    def __init__(self, _id, hp, x, y):
        self._id = _id
        self.hp = hp
        self.x = x
        self.y = y
        self.previous = [x, y]

    def get_id(self):
        return self._id

    def get_hp(self):
        return self.hp

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_hp(self, hp):
        self.hp = hp

    def set_hp_by_id(self, __id):
        if self._id == __id:
            self.hp = 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_coord(self, x, y):
        self.previous = [self.x, self.y]
        self.set_x(x)
        self.set_y(y)


# состояние, картинка, жизни, урон, шанс нанести урон, шанс сбежать, награда
def generate_name_enemy(init=None):
    if init is None:
        ran = random.randint(0, 2)
        if ran == 0:
            return 'На вас напала Летучая мышь! ',\
                get_real_image(pygame.image.load('assets/enemies/bat.png')), 2, 1, 25, 50, 1
        return 'На вас напал Слизень! ', get_real_image(pygame.image.load('assets/enemies/slug.png')), 2, 1, 35, 45, 2


# Константы:
new_game_img = get_real_image(pygame.image.load('assets/buttons/button_new_game.png').convert_alpha())
button_new_game = Button2(20, y1=136, image=new_game_img, scale=1)

continue_img = get_real_image(pygame.image.load('assets/buttons/button_continue.png').convert_alpha())
button_continue = Button2(20, y1=232, image=continue_img, scale=1)

quit_img = get_real_image(pygame.image.load('assets/buttons/button_quit.png').convert_alpha())
button_quit = Button2(20, y1=338, image=quit_img, scale=1)

background = pygame.image.load('assets/map/s.png')
wait_fullscreen = False

button_cave = Button2(130, y1=770, image=pygame.image.load('assets/transparent/transparent150x150.png'), scale=1)
cave_img = pygame.image.load('assets/map/s_cave.png')

button_castle = Button2(1470, 400, image=pygame.image.load("assets/transparent/transparent300x300.png"), scale=1)
castle_img = pygame.image.load('assets/map/s_castle.png')

button_ferm = Button2(760, 470, image=pygame.image.load('assets/transparent/transparent200x200.png'), scale=1)
ferm_img = pygame.image.load('assets/map/s_ferm.png')

button_wizard = Button2(1500, 880, image=pygame.image.load('assets/transparent/transparent300x300.png'), scale=1)
wizard_img = pygame.image.load('assets/map/s_wizard.png')

only_black = pygame.image.load('assets/game/only_black.png')

field_choice = pygame.image.load('assets/backgrounds/field_choice.png')
exit_button = Button2(1052, 620, image=pygame.image.load('assets/buttons/in_game/48x48.png'), scale=1)

plus_preview = get_real_image(pygame.image.load('assets/buttons/in_game/plus.png'), scale=0.5)

plus_buttons = [
    Button2(1004, 640, image=pygame.image.load('assets/buttons/in_game/plus.png'), scale=1),
    Button2(1004, 680, image=pygame.image.load('assets/buttons/in_game/plus.png'), scale=1),
    Button2(1004, 720, image=pygame.image.load('assets/buttons/in_game/plus.png'), scale=1),
    Button2(1004, 760, image=pygame.image.load('assets/buttons/in_game/plus.png'), scale=1)
]

mimic_img = get_real_image(pygame.image.load('assets/enemies/mimic.jpg'))
dragon_img = get_real_image(pygame.image.load('assets/enemies/dragon.jpg'))