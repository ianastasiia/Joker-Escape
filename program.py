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
BatmanMinSize = 20
BatmanMaxSize = 50
BatmanMinSpeed = 1
BatmanMaxSpeed = 8
AddBatman = 6
PlayerMove = 5
FPS = 30


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


def drawText(text, font, surface, x, y, color):
    textobject = font.render(text, 1, color)
    textrect = textobject.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobject, textrect)


# завершение
def terminate():
    f = open("data\\topscores", mode="rb")
    l = list(map(int, [line.strip() for line in f]))
    l.append(topScore)

    ff = open('data\\topscores', 'w')
    for elem in l:
        ff.write(str(elem) + "\n")

    ff.close()

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


# касание спрайтов - коллайд
def playerHasHitBatman(player, batmans):
    for b in batmans:
        if player.colliderect(b['rect']):
            return True
    return False

    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             Landing(event.pos)
    #     screen.fill(pygame.Color("Black"))
    #     all_sprites.draw(screen)
    #     all_sprites.update()
    #     pygame.display.flip()


# в зависимости от уровня меняются характеристики
def PressButton():
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                global BatmanMinSize, BatmanMaxSize, BatmanMinSpeed, BatmanMaxSpeed, AddBatman
                if button1.pressed(pygame.mouse.get_pos()):
                    BatmanMinSize = 15
                    BatmanMaxSize = 80
                    BatmanMinSpeed = 1
                    BatmanMaxSpeed = 6
                    AddBatman = 35

                elif button2.pressed(pygame.mouse.get_pos()):
                    BatmanMinSize = 15
                    BatmanMaxSize = 70
                    BatmanMinSpeed = 1
                    BatmanMaxSpeed = 8
                    AddBatman = 20
                elif button3.pressed(pygame.mouse.get_pos()):
                    BatmanMinSize = 20
                    BatmanMaxSize = 70
                    BatmanMinSpeed = 3
                    BatmanMaxSpeed = 11
                    AddBatman = 13
                return


# инициализация файлов
font = pygame.font.SysFont('serif', 48)

BatmanImg = pygame.image.load('data\\batman white.png')
playerImg = pygame.image.load('data\player.png')
backgroundImg = pygame.image.load('data\joker.jpg')

level1 = pygame.image.load('data\level 1.png')
level2 = pygame.image.load('data\level 2.png')
level3 = pygame.image.load('data\level 3.png')

player = playerImg.get_rect()

pygame.mixer.music.load('data\Chlorine.mp3')
gameOverSound = pygame.mixer.Sound('data\Joker Laugh.mp3')

drawText('JOKER vs. BATMAN', font, screen, (width // 6), (height // 3), white_color)
drawText('Press a key to start.', font, screen, (width // 4.5), (height // 3) + 50, white_color)

pygame.display.update()
waitForPlayerToPressKey()

# Создание кнопок с выбором уровня
screen.fill(black_color)
button1 = Button()
button2 = Button()
button3 = Button()
Level_1 = button1.create_button(screen, (0, 0, 255), 35, 450, 150, 50, 10, "Easy Level", black_color)
Level_2 = button2.create_button(screen, (255, 0, 0), 225, 450, 150, 50, 10, "Medium Level", black_color)
Level_3 = button3.create_button(screen, (255, 255, 0), 415, 450, 150, 50, 10, "Hard Level", black_color)

screen.blit(level1, (50, 165))
screen.blit(level2, (235, 170))
screen.blit(level3, (410, 175))

PressButton()

pygame.mouse.set_visible(False)
topScore = 0

# главный поток игры
while True:
    batmans = []
    score = 0
    moveLeft, moveRight, moveUp, moveDown = False, False, False, False
    reverse, slow = False, False
    player.topleft = (width // 2, height - 50)
    BatmanCount = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEMOTION:
                player.move_ip(event.pos[0] - player.centerx, event.pos[1] - player.centery)

            if event.type == KEYDOWN:
                if event.key == ord('w') or event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == ord('d') or event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == ord('s') or event.key == K_DOWN:
                    moveUp = False
                    moveDown = True
                if event.key == ord('a') or event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == ord('x'):
                    slow = True
                if event.key == ord('z'):
                    reverse = True
            # работа с клавишами
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == ord('w') or event.key == K_UP:
                    moveUp = False
                if event.key == ord('d') or event.key == K_RIGHT:
                    moveRight = False
                if event.key == ord('s') or event.key == K_DOWN:
                    moveDown = False
                if event.key == ord('a') or event.key == K_LEFT:
                    moveLeft = False
                if event.key == ord('x'):
                    slow = False
                    score = 0
                if event.key == ord('z'):
                    reverse = False
                    score = 0

        if not reverse and not slow:
            BatmanCount += 1
        if BatmanCount == AddBatman:
            BatmanCount = 0
            BatmanSize = random.randint(BatmanMinSize, BatmanMaxSize)
            newBatman = {
                'speed': random.randint(BatmanMinSpeed, BatmanMaxSpeed),
                'rect': pygame.Rect(random.randint(0, width - BatmanSize), 0 - BatmanSize, BatmanSize, BatmanSize),
                'surface': pygame.transform.scale(BatmanImg, (BatmanSize, BatmanSize)),
            }

            batmans.append(newBatman)

        if moveUp and player.top > 0:
            player.move_ip(0, -1 * PlayerMove)
        if moveRight and player.right < width:
            player.move_ip(PlayerMove, 0)
        if moveDown and player.bottom < height:
            player.move_ip(0, PlayerMove)
        if moveLeft and player.left > 0:
            player.move_ip(-1 * PlayerMove, 0)

        pygame.mouse.set_pos(player.centerx, player.centery)

        for b in batmans:
            if not slow and not reverse:
                b['rect'].move_ip(0, b['speed'])
            elif slow:
                b['rect'].move_ip(0, 1)
            elif reverse:
                b['rect'].move_ip(0, -5)

        for b in batmans[:]:
            if b['rect'].top > height:
                batmans.remove(b)

        screen.fill(backgroundcolor)

        drawText('Score: %s' % (score), font, screen, 10, 0, (255, 255, 255))
        drawText('Top Score: %s' % (topScore), font, screen, 10, 40, (255, 255, 255))

        screen.blit(playerImg, player)

        for b in batmans:
            screen.blit(b['surface'], b['rect'])

        pygame.display.update()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        if playerHasHitBatman(player, batmans):
            if score > topScore:
                topScore = score
            break

        clock.tick(FPS)

    # завершение игры
    pygame.mixer.music.stop()
    gameOverSound.play()

    screen.fill(black_color)
    screen.blit(backgroundImg, (0, 0))

    f = open("data\\topscores", mode="rb")
    l = list(map(int, [line.strip() for line in f]))

    drawText('GAME OVER', font, screen, (width // 3.5), (height // 3.5), white_color)
    drawText('Press a key to play again.', font, screen, (width // 7), (height // 3.5) + 50, white_color)
    drawText('Last top scores', font, screen, (width // 3.5), (height // 3.5) + 130, white_color)
    drawText(str(topScore), font, screen, (width // 2.2), (height // 3.5) + 180, white_color)
    drawText(str(l[-1]), font, screen, (width // 2.2), (height // 3.5) + 220, white_color)
    drawText(str(l[-2]), font, screen, (width // 2.2), (height // 3.5) + 260, white_color)
    drawText(str(l[-3]), font, screen, (width // 2.2), (height // 3.5) + 300, white_color)
    drawText(str(l[-4]), font, screen, (width // 2.2), (height // 3.5) + 340, white_color)

    f.close()
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
