# https://github.com/SwordOfZero/Our_Game.git
import pygame
import sys
import os
import Start_screen
import random


pygame.init()
FPS = 24
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EPIC STORY')
running = True
clock = pygame.time.Clock()
pygame.display.flip()
music, sound_effects = 0, 0
tile_width = tile_height = 30
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None

pygame.mixer.init()
pygame.mixer.music.load('data/this_silence_is_mine.mp3')
pygame.mixer.music.play(-1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.l = 5
        self.m = 10
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)

    def f(self):
        if self.pos_y >= level_y * tile_height or self.pos_y <= 0:
            self.l = self.l * -1
        self.pos_y += self.l
        if self.pos_x >= level_x * tile_width or self.pos_x <= 0:
            self.m = self.m * -1
        self.pos_x += self.m
        print(self.pos_y)
        self.rect = self.rect.move(self.m, self.l)

    def get_pos(self):
        return [self.pos_x, self.pos_y]


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        width = 300
        height = 300
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    def update_x(self, target):
        width = 300
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)

    def update_y(self, target):
        height = 300
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    def start_position(self, target):
        width = 300
        height = 300
        if 135 <= player.get_pos()[0] <= (level_x - 4) * tile_width - 15:
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        else:
            left = True
            if player.get_pos()[0] > (level_x / 2) * tile_width:
                left = False
            if left:
                pass
            else:
                self.dx = -((level_x / 2) * tile_width)
        if 135 <= player.get_pos()[1] <= (level_y - 4) * tile_height - 15:
            self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        else:
            up = True
            if player.get_pos()[1] > (level_y / 2) * tile_height:
                up = False
            if up:
                pass
            else:
                self.dy = -((level_y / 2) * tile_height + 30)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('floor', x, y)
            elif level[y][x] == '~':
                Tile('water', x, y)
            elif level[y][x] == '$':
                Tile('floor', x, y)
                new_player = Player(x * tile_width, y * tile_height)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def mouse(pos):
    image = load_image("mouse.png")
    screen.blit(image, pos)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


player_image = load_image('wall.png')
tile_images = {
    'wall': load_image('wall.png'),
    'grass': load_image('grass.png'),
    'floor': load_image('floor.png'),
    'water': load_image('water.png')
}


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global sound_effects
    global music
    Start_screen.get_screen(screen)
    s = Start_screen.StartScreenButtons()
    x, y = (-70, -70)
    mouse_cursor = False
    while s.start_flag:
        music, sound_effects = Start_screen.take_sound()
        pygame.mixer.music.set_volume(music)
        s.screens(s.screen_number)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                s.action(event.pos)
            if pygame.mouse.get_focused() and event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if pygame.mouse.get_focused():
                mouse_cursor = True
            else:
                mouse_cursor = False
        if mouse_cursor:
            mouse((x, y))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.mixer.music.stop()


pygame.mouse.set_visible(False)
start_screen()
pygame.mouse.set_visible(True)
player, level_x, level_y = generate_level(load_level('map.txt'))
all_sprites.add(player)
size = WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode(size)
camera = Camera()
camera.start_position(player)
for sprite in all_sprites:
    camera.apply(sprite)
all_sprites.draw(screen)

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_SPACE]:
        player.f()
    pygame.display.flip()
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    # обновляем положение всех спрайтов
    if 135 <= player.get_pos()[0] <= (level_x - 4) * tile_width - 15:
        camera.update_x(player)
    else:
        camera.dx = 0
    if 135 <= player.get_pos()[1] <= (level_y - 4) * tile_height - 15:
        camera.update_y(player)
    else:
        camera.dy = 0
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)

pygame.quit()