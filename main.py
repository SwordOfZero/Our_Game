# https://github.com/SwordOfZero/Our_Game.git
import pygame
import sys
import os


pygame.init()
FPS = 14
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Белый круг на чёрном фоне')
running = True
clock = pygame.time.Clock()
pygame.display.flip()


class StartScreenButtons:
    def __init__(self):
        self.options = [199, 445, 199, 241]
        self.start = [199, 366, 99, 141]
        self.credits = [199, 430, 299, 341]
        self.back_button = [49, 171, 499, 541]
        self.screen_number = 0
        self.start_flag = True

    def screens(self, screen_number=0):
        if screen_number == 0:
            image = load_image('start_screen.jpg')
            screen.blit(image, (0, 0))
            f1 = pygame.font.Font(None, 75)
            text1 = f1.render('START', True,
                              (255, 0, 0))
            text2 = f1.render('OPTIONS', True,
                              (255, 0, 0))
            text3 = f1.render('CREDITS', True,
                              (255, 0, 0))
            screen.blit(text1, (200, 100))
            screen.blit(text2, (200, 200))
            screen.blit(text3, (200, 300))
        elif screen_number == 1:
            image = load_image('options.jpg')
            screen.blit(image, (0, 0))
            back_button = pygame.font.Font(None, 75)
            back_button1 = back_button.render('Back', True,
                              (255, 255, 255))
            screen.blit(back_button1, (50, 500))
        elif screen_number == 2:
            image = load_image('credits.png')
            screen.blit(image, (0, 0))
            intro_text = ["Разработчики:",
                          "  Киндеев Лев, Макаров Макар",
                          "Художники:",
                          "  Макаров Макар, Киндеев Лев",
                          "Отель:",
                          "  Триваго"]
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    def action(self, mouse_pos):
        if self.screen_number == 0:
            if self.options[0] < mouse_pos[0] < self.options[1] and \
                    self.options[2] < mouse_pos[1] < self.options[3]:
                self.screen_number = 1
            elif self.start[0] < mouse_pos[0] < self.start[1] and \
                    self.start[2] < mouse_pos[1] < self.start[3]:
                self.start_flag = False
            elif self.credits[0] < mouse_pos[0] < self.credits[1] and \
                    self.credits[2] < mouse_pos[1] < self.credits[3]:
                self.screen_number = 2
        elif self.screen_number == 1:
            if self.back_button[0] < mouse_pos[0] < self.back_button[1] and \
                    self.back_button[2] < mouse_pos[1] < self.back_button[3]:
                self.screen_number = 0
        elif self.screen_number == 2:
            self.screen_number = 0





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
    s = StartScreenButtons()
    x, y = (-70, -70)
    mouse_cursor = False
    while s.start_flag:
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

