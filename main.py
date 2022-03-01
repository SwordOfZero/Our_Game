# https://github.com/SwordOfZero/Our_Game.git
#подключение библиотек
import pygame
import sys
import os
import Start_screen
import main_hero as hero
import my_functions as f
import camera_class as cam
import my_enemy as en


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
enemy = []
win = False
close = True

player = None #переменная игрока

#запуск музыки в стартовом меню
pygame.mixer.init()
pygame.mixer.music.load('data/this_silence_is_mine.mp3')
pygame.mixer.music.play(-1)

#курсор
def mouse(pos):
    image = f.load_my_image("mouse.png")
    screen.blit(image, pos)

#полное выключение
def terminate():
    pygame.quit()
    sys.exit()

def end_screen(win):
    screen.fill((0, 0, 0))
    pygame.mixer.music.stop()
    running = True
    end = pygame.font.Font(None, 30)
    text = ''
    if win:
        text = 'VICTORY'
    else:
        text = 'GAME OVER'
    screen_text = end.render(f'{text}', True, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(screen_text, (100, 100))
        pygame.display.flip()
        clock.tick(FPS)

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
info = pygame.font.Font(None, 30)
player, enemies, level_x, level_y = f.generate_level(f.load_level('map.txt'))
player.get_map_size(level_x, level_y)
f.all_sprites.add(player)
for i in enemies:
    enemy.append(en.Enemies(i[0], i[1]))
    enemy[-1].get_map_size(level_x, level_y)
    enemy[-1].add_sword()
    f.all_sprites.add(enemy[-1])
player.add_sword()
size = WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode(size)
camera = cam.Camera(level_x, level_y)
camera.start_position(player, player)
#отрисовка первого кадра игры
for sprite in f.all_sprites:
    camera.apply(sprite)
f.all_sprites.draw(screen)
pygame.mixer.music.load('data/The_Forgotten.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(music)
f.sound_effect_sword.set_volume(sound_effects)

#игра работает
while running:
    #кнопки
    keys = pygame.key.get_pressed()
    way = [keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_DOWN], keys[pygame.K_LEFT]]
    #удар и закрытие окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 122:
                player.hit(player.rotate)
                #запуск удара
    #если нажата стрелка и не происходит удар, то передвижение
    if f.all_not_true(way) and not player.sword.playing:
        player.move(way)
    else:
        #статичный кадр с нужным поворотом
        player.image = hero.player_sprites[player.rotate * 3]
    for elem in enemy:
        elem.get_hit(player.sword.playing)
        elem.brain(player.get_pos())
    player.sword.animation()
    for elem in enemy:
        elem.sword.animation()
    pygame.display.flip()
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    camera.check(player)
    f.all_sprites.draw(screen)
    player.timer()
    check = False
    enemy_col = 0
    for elem in enemy:
        if not elem.died:
            enemy_col += 1
        if elem.sword.playing:
            check = True
    if enemy_col == 0:
        running = False
        win = True
        close = False
    player.get_hit(check)
    if player.hp == 0:
        running = False
        close = False
    text1 = info.render(f'HP: {player.hp}', True, (255, 255, 255))
    text2 = info.render(f'ENEMIES: {enemy_col}', True, (255, 255, 255))
    screen.blit(text1, (0, 0))
    screen.blit(text2, (0, 30))

if not close:
    end_screen(win)

pygame.quit()
