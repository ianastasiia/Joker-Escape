import pygame
import os
import sys

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