# https://github.com/SwordOfZero/Our_Game.git
#подключение библиотек
import pygame
import sys
import os
import Start_screen


pygame.init()
FPS = 16 #установка кадров в секунду
size = WIDTH, HEIGHT = 800, 600 #размер окна
screen = pygame.display.set_mode(size) #создание экрана
pygame.display.set_caption('Kuroi sekai') #название окна
running = True #переменная, отвечающая за запуск и последующую работу игры
clock = pygame.time.Clock() #создание внутриигровых "часов"
pygame.display.flip() #обновление экрана
music, sound_effects = 0, 0 #создание переменных, отвечающих за громкость звуковых эффектов и музыки
tile_width = tile_height = 30 #ширина/высота тайлов
tiles_group = pygame.sprite.Group() #создание группы тайлов
wall_group = pygame.sprite.Group() #создание группы стен
all_sprites = pygame.sprite.Group() #создание группы всез спрайтов
player_group = pygame.sprite.Group() #создание группы игрока
hero_weapon_group = pygame.sprite.Group() #создание группы оружия игрока
player = None #переменная игрока

#запуск музыки в стартовом меню
pygame.mixer.init()
pygame.mixer.music.load('data/this_silence_is_mine.mp3')
pygame.mixer.music.play(-1)


#класс тайлов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, groups=[tiles_group, all_sprites]):
        super().__init__(groups)
        #присвоение изображения тайлу и создание "физического тела" тайла
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.y_speed = 5 #скорость по х и у
        self.x_speed = 5
        self.image = player_sprites[0] #начальное изображение игрока
        self.pos_x = pos_x #установка начальной позиции по х и у
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y) #создание "тела" по размеру изображения
        self.frames = 0 #индекс кадра анимации
        self.rotate = 0 #индекс угла поворота игрока
        self.rotate_angles = [180, 270, 0, 90] #список углов поворота, зависящий от индекса
        self.sword = Attack(pos_x, pos_y) #создание атаки для героя

    #функция, добавляющая атаку в группу всех спрайтов и оружия героя
    def add_sword(self):
        all_sprites.add(self.sword)
        hero_weapon_group.add(self.sword)

    #получение текущей позиции игрока
    def get_pos(self):
        return [self.pos_x, self.pos_y]

    #передвижение персонажа
    def move(self, arrow): #передаётся список из 4 да/нет переменных, отвечающих за нажатую кнопку
        self.frames = (self.frames + 1) % 3 #типо анимация
        buffer = [self.pos_x, self.pos_y] #сохранение позиции на всякий случай
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
        self.pos_x += x #новая позиция
        self.pos_y += y
        #если новая позиция вне экрана, то возвращается предыдущая позиция
        if ((self.pos_y >= level_y * tile_height) or (self.pos_y <= 0)) or \
                ((self.pos_x >= level_x * tile_width) or (self.pos_x <= 0)):
            self.pos_x = buffer[0]
            self.pos_y = buffer[1]
            x, y = 0, 0
        self.rect = self.rect.move(x, y)
        #то же самое, только проверяется пересечение со стенами
        if pygame.sprite.spritecollideany(self, wall_group):
            x, y = -x, -y
            self.pos_x += x
            self.pos_y += y
            self.rect = self.rect.move(x, y)

    #удар
    def hit(self):
        self.sword.update_position(self.pos_x, self.pos_y) #перемещение меча
        self.sword.rotate(self.rotate_angles[self.rotate]) #поворот в правильную сторону

#класс атаки
class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x #х и у
        self.y = y
        self.width = tile_width #ширина и высота
        self.height = tile_height
        self.image = hit_sprites[0] #стартовое изображение
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.playing = False #происходит удар или нет
        self.frames = 10 #количество кадров анимации
        self.rotate_angle = 0 #угол поворота
        self.rot_current_pos = [0, 0] #текущий угол поворота
        self.rot_positions = [[-15, -15], [-15, -15], [-15, 20], [15, -15]] #смещение в зависимости от угла

    #анимация удара
    def animation(self):
        if self.playing and self.frames != 0:
            self.frames -= 1
            self.image = hit_sprites[self.frames]
        elif self.playing:
            self.frames = 10
            self.playing = False

    #новая позиция удара
    def update_position(self, new_x, new_y):
        self.rect.move_ip((-(self.x - new_x), new_y - self.y))
        self.x = new_x
        self.y = new_y

    #поворот
    def rotate(self, rot):
        #обнуление позиции
        self.rot_current_pos[0], self.rot_current_pos[1] = self.rot_current_pos[0] * -1, self.rot_current_pos[1] * -1
        self.rect = self.rect.move(self.rot_current_pos)
        self.rotate_angle = -self.rotate_angle
        for i in range(len(hit_sprites)):
            hit_sprites[i] = pygame.transform.rotate(hit_sprites[i], self.rotate_angle)
        self.rotate_angle = rot
        #поворот в нужную сторону
        for i in range(len(hit_sprites)):
            hit_sprites[i] = pygame.transform.rotate(hit_sprites[i], rot)
        self.rect = self.image.get_rect(left=self.rect.left, top=self.rect.top)
        self.rot_current_pos[0] = self.rot_positions[int(rot / 90)][0]
        self.rot_current_pos[1] = self.rot_positions[int(rot / 90)][1]
        #смещение в нужную сторону
        self.rect = self.rect.move(self.rot_current_pos)


#камера
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

    #обновлени х
    def update_x(self, target):
        width = 300
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)

    #обновлени у
    def update_y(self, target):
        height = 300
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    #концентрация на гг в начале игры
    def start_position(self, target):
        width = 300
        height = 300
        #если слишком близко к краю, то регулирует положение камеры
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


#анимация
def animate(sprite_list, animation, frame):
    sprites = sprite_list
    num = animation
    frames = frame
    return sprites[(num * 3) + frames]


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


#загрузка уровня и создание гг
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


#курсор
def mouse(pos):
    image = load_image("mouse.png")
    screen.blit(image, pos)

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


#загрузка картинки
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


#загрузка изображений героя, тайлов и удара
player_sprites = [load_image(f"hero_{i // 3 + 1}{i % 3 + 1}.png") for i in range(0, 12)]
hit_sprites = [load_image(f"hit_{i}.png") for i in range(0, 10)]
tile_images = {
    'wall': load_image('wall.png'),
    'grass': load_image('grass.png'),
    'floor': load_image('floor.png'),
    'water': load_image('water.png'),
    'spawn': load_image('spawn.png')
}


#полное выключение
def terminate():
    pygame.quit()
    sys.exit()

#стартовый экран
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

#отключение курсора, стартовый экран, включение курсора
pygame.mouse.set_visible(False)
start_screen()
pygame.mouse.set_visible(True)
#создание уровня, камеры и гг
player, level_x, level_y = generate_level(load_level('map.txt'))
all_sprites.add(player)
player.add_sword()
size = WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode(size)
camera = Camera()
camera.start_position(player)
#отрисовка первого кадра игры
for sprite in all_sprites:
    camera.apply(sprite)
all_sprites.draw(screen)
global_frame = 0

#игра работает
while running:
    #счётчик кадров
    global_frame = (global_frame + 1) % FPS
    #кнопки
    keys = pygame.key.get_pressed()
    way = [keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_DOWN], keys[pygame.K_LEFT]]
    #удар и закрытие окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 122:
                player.hit()
                #запуск удара
                player.sword.playing = True
    #если нажата стрелка и не происходит удар, то передвижение
    if all_not_true(way) and not player.sword.playing:
        player.move(way)
    else:
        #статичный кадр с нужным поворотом
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