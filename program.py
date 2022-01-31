import pygame
import os
import random
import sys
from pygame.locals import *

# начало игры, инициаллизация переменных, создание поля
pygame.init()
clock = pygame.time.Clock()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Joker Escape')
all_sprites = pygame.sprite.Group()

backgroundcolor = (0, 0, 0)
black_color = (0, 0, 0)
white_color = (255, 255, 255)


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        myFont = pygame.font.SysFont('serif', 22)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print("Some button was pressed!")
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


class Joker(pygame.sprite.Sprite):
    image = pygame.image.load("data\player.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Joker.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


jokerobj = Joker()


class Batman(pygame.sprite.Sprite):
    image = pygame.image.load('data\\batman white.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Batman.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, jokerobj):
            self.rect = self.rect.move(0, 1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# завершение
def terminate():
    # f = open("topscores", mode="rb")
    # l = list(map(int, [line.strip() for line in f]))
    # l.append(topScore)
    #
    # ff = open('topscores', 'w')
    # for elem in l:
    #     ff.write(str(elem) + "\n")
    #
    # ff.close()

    pygame.quit()
    sys.exit()


# завершение по кнопку escape
def waitForPlayerToPressKey():
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
