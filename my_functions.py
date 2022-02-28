import pygame
import sys
import os
import main_hero as hero


tile_width = tile_height = 30
tiles_group = pygame.sprite.Group() #создание группы тайлов
wall_group = pygame.sprite.Group() #создание группы стен
all_sprites = pygame.sprite.Group() #создание группы всез спрайтов
player_group = pygame.sprite.Group() #создание группы игрока
enemy_group = pygame.sprite.Group()
hero_weapon_group = pygame.sprite.Group() #создание группы оружия игрока
enemy_weapon_group = pygame.sprite.Group()

#класс тайлов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, groups=[tiles_group, all_sprites]):
        super().__init__(groups)
        #присвоение изображения тайлу и создание "физического тела" тайла
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

#анимация
def animate(sprite_list, animation, frame):
    sprites = sprite_list
    num = animation
    frames = frame
    return sprites[(num * 3) + frames]


def load_my_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

#загрузка уровня и создание гг
def generate_level(level):
    new_player, x, y, = None, None, None
    enemies = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y, [tiles_group, all_sprites, wall_group])
            elif level[y][x] == '@':
                Tile('floor', x, y)
            elif level[y][x] == '~':
                Tile('water', x, y, [tiles_group, all_sprites, wall_group])
            elif level[y][x] == '$':
                Tile('spawn', x, y)
                new_player = hero.Player(x * tile_width, y * tile_height)
            elif level[y][x] == 'e':
                Tile('spawn', x, y)
                enemies.append([x * tile_width, y * tile_height])
    # вернем игрока, а также размер поля в клетках
    return new_player, enemies, x, y


tile_images = {
    'wall': load_my_image('wall.png'),
    'grass': load_my_image('grass.png'),
    'floor': load_my_image('floor.png'),
    'water': load_my_image('water.png'),
    'spawn': load_my_image('spawn.png')
}

#чтение уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

#логическая операция "исключающее "или""
def all_not_true(a):
    true_counter = 0
    for elem in a:
        if elem is True:
            true_counter += 1
    if true_counter == 1:
        return True
    else:
        return False

def nor(a):
    true_counter = 0
    for elem in a:
        if elem is True:
            true_counter += 1
    if true_counter > 0:
        return True
    else:
        return False
