import pygame


#начало игры, инициаллизация переменных, создание поля
pygame.init()
clock = pygame.time.Clock()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Joker Escape')
all_sprites = pygame.sprite.Group()

backgroundcolor = (0, 0, 0)