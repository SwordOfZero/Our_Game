# https://github.com/SwordOfZero/Our_Game.git
import pygame
import sys
import os
import Start_screen
import random


pygame.init()
FPS = 16
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Kuroi sekai')
running = True
clock = pygame.time.Clock()
pygame.display.flip()
music, sound_effects = 0, 0
tile_width = tile_height = 30
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
hero_weapon_group = pygame.sprite.Group()
player = None

pygame.mixer.init()
pygame.mixer.music.load('data/this_silence_is_mine.mp3')
pygame.mixer.music.play(-1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, groups=[tiles_group, all_sprites]):
        super().__init__(groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.y_speed = 5
        self.x_speed = 5
        self.image = player_sprites[0]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.frames = 0
        self.rotate = 0
        self.rotate_angles = [180, 270, 0, 90]
        self.sword = Attack(pos_x, pos_y)

    def add_sword(self):
        all_sprites.add(self.sword)
        hero_weapon_group.add(self.sword)

    def get_pos(self):
        return [self.pos_x, self.pos_y]

    def move(self, arrow):
        self.frames = (self.frames + 1) % 3
        buffer = [self.pos_x, self.pos_y]
        x, y = 0, 0
        if arrow[0]:
            y = -self.y_speed
            self.image = animate(player_sprites, 2, self.frames)
            self.rotate = 2
        elif arrow[2]:
            y = self.y_speed
            self.image = animate(player_sprites, 0, self.frames)
            self.rotate = 0
        elif arrow[1]:
            x = self.x_speed
            self.image = animate(player_sprites, 1, self.frames)
            self.rotate = 1
        elif arrow[3]:
            x = -self.x_speed
            self.image = animate(player_sprites, 3, self.frames)
            self.rotate = 3
        self.pos_x += x
        self.pos_y += y
        if ((self.pos_y >= level_y * tile_height) or (self.pos_y <= 0)) or \
                ((self.pos_x >= level_x * tile_width) or (self.pos_x <= 0)):
            self.pos_x = buffer[0]
            self.pos_y = buffer[1]
            x, y = 0, 0
        self.rect = self.rect.move(x, y)
        if pygame.sprite.spritecollideany(self, wall_group):
            x, y = -x, -y
            self.pos_x += x
            self.pos_y += y
            self.rect = self.rect.move(x, y)

    def hit(self):
        self.sword.update_position(self.pos_x, self.pos_y)
        self.sword.rotate(self.rotate_angles[self.rotate])

class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = tile_width
        self.height = tile_height
        self.image = hit_sprites[0]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.playing = False
        self.frames = 10
        self.rotate_angle = 0
        self.rot_current_pos = [0, 0]
        self.rot_positions = [[-15, -15], [-15, -15], [-15, 20], [15, -15]]

    def animation(self):
        if self.playing and self.frames != 0:
            self.frames -= 1
            self.image = hit_sprites[self.frames]
        elif self.playing:
            self.frames = 10
            self.playing = False

    def update_position(self, new_x, new_y):
        self.rect.move_ip((-(self.x - new_x), new_y - self.y))
        self.x = new_x
        self.y = new_y

    def rotate(self, rot):
        self.rot_current_pos[0], self.rot_current_pos[1] = self.rot_current_pos[0] * -1, self.rot_current_pos[1] * -1
        self.rect = self.rect.move(self.rot_current_pos)
        self.rotate_angle = -self.rotate_angle
        for i in range(len(hit_sprites)):
            hit_sprites[i] = pygame.transform.rotate(hit_sprites[i], self.rotate_angle)
        self.rotate_angle = rot
        for i in range(len(hit_sprites)):
            hit_sprites[i] = pygame.transform.rotate(hit_sprites[i], rot)
        self.rect = self.image.get_rect(left=self.rect.left, top=self.rect.top)
        self.rot_current_pos[0] = self.rot_positions[int(rot / 90)][0]
        self.rot_current_pos[1] = self.rot_positions[int(rot / 90)][1]
        self.rect = self.rect.move(self.rot_current_pos)

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


def animate(sprite_list, animation, frame):
    sprites = sprite_list
    num = animation
    frames = frame
    return sprites[(num * 3) + frames]


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
                Tile('wall', x, y, [tiles_group, all_sprites, wall_group])
            elif level[y][x] == '@':
                Tile('floor', x, y)
            elif level[y][x] == '~':
                Tile('water', x, y, [tiles_group, all_sprites, wall_group])
            elif level[y][x] == '$':
                Tile('spawn', x, y)
                new_player = Player(x * tile_width, y * tile_height)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def mouse(pos):
    image = load_image("mouse.png")
    screen.blit(image, pos)

def all_not_true(a):
    true_counter = 0
    for elem in a:
        if elem is True:
            true_counter += 1
    if true_counter == 1:
        return True
    else:
        return False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


player_sprites = [load_image(f"hero_{i // 3 + 1}{i % 3 + 1}.png") for i in range(0, 12)]
hit_sprites = [load_image(f"hit_{i}.png") for i in range(0, 10)]
tile_images = {
    'wall': load_image('wall.png'),
    'grass': load_image('grass.png'),
    'floor': load_image('floor.png'),
    'water': load_image('water.png'),
    'spawn': load_image('spawn.png')
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
player.add_sword()
size = WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode(size)
camera = Camera()
camera.start_position(player)
for sprite in all_sprites:
    camera.apply(sprite)
all_sprites.draw(screen)
global_frame = 0

while running:
    global_frame = (global_frame + 1) % FPS
    keys = pygame.key.get_pressed()
    way = [keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_DOWN], keys[pygame.K_LEFT]]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 122:
                player.hit()
                player.sword.playing = True
    if all_not_true(way) and not player.sword.playing:
        player.move(way)
    else:
        player.image = player_sprites[player.rotate * 3]
    player.sword.animation()
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