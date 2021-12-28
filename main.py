# https://github.com/SwordOfZero/Our_Game.git
import pygame
import sys
import os
import Start_screen


pygame.init()
FPS = 24
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EPIC STORY')
running = True
clock = pygame.time.Clock()
pygame.display.flip()
music, sound_effects = 0, 0

pygame.mixer.init()
pygame.mixer.music.load('data/this_silence_is_mine.mp3')
pygame.mixer.music.play()


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
                print(event.pos)
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


pygame.mouse.set_visible(False)
start_screen()
pygame.mouse.set_visible(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(FPS)
    screen.fill((0, 0, 0))
pygame.quit()