#загрузка библиотек
import pygame
import sys
import os

#громкомть звука
music, sound_effects = 1, 1
screen = 0

#загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


#получение экрана
def get_screen(s):
    global screen
    screen = s

#вернуть переменные звука
def take_sound():
    return music, sound_effects

#кнопки на экране
class StartScreenButtons:
    def __init__(self):
        self.options = [199, 445, 199, 241]
        self.start = [199, 366, 99, 141]
        self.credits = [199, 430, 299, 341]
        self.back_button = [49, 171, 499, 541]
        self.music_button_m = [484, 513, 113, 137]
        self.music_button_p = [678, 707, 113, 137]
        self.sound_button_m = [484, 513, 173, 197]
        self.sound_button_p = [678, 707, 173, 197]
        self.screen_number = 0
        self.start_flag = True

    def screens(self, screen_number=0):
#главный экран
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
#настройки
        elif screen_number == 1:
            image = load_image('options.jpg')
            screen.blit(image, (0, 0))
            sound = pygame.font.Font(None, 75)
            button = pygame.font.Font(None, 75)
            back_button1 = button.render('Back', True,
                              (255, 255, 255))
            screen.blit(back_button1, (50, 500))
            music_button = sound.render(f'{int(music * 100)}%', True,
                              (100, 255, 100))
            sound_button = sound.render(f'{int(sound_effects * 100)}%', True,
                                        (100, 255, 100))
            screen.blit(music_button, (530, 95))
            screen.blit(sound_button, (530, 160))
#титры
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

    #обработка событий
    def action(self, mouse_pos):
        global music
        global sound_effects
        if self.screen_number == 0: #если находимся в меню
            if self.options[0] < mouse_pos[0] < self.options[1] and \
                    self.options[2] < mouse_pos[1] < self.options[3]:
                self.screen_number = 1
            elif self.start[0] < mouse_pos[0] < self.start[1] and \
                    self.start[2] < mouse_pos[1] < self.start[3]:
                self.start_flag = False
            elif self.credits[0] < mouse_pos[0] < self.credits[1] and \
                    self.credits[2] < mouse_pos[1] < self.credits[3]:
                self.screen_number = 2
        elif self.screen_number == 1: #в окне настройки
            if self.back_button[0] < mouse_pos[0] < self.back_button[1] and \
                    self.back_button[2] < mouse_pos[1] < self.back_button[3]:
                self.screen_number = 0
            elif self.music_button_m[0] < mouse_pos[0] < self.music_button_m[1] and \
                    self.music_button_m[2] < mouse_pos[1] < self.music_button_m[3]:
                if music > 0:
                    music = (int(music * 100) - 5) / 100
            elif self.music_button_p[0] < mouse_pos[0] < self.music_button_p[1] and \
                    self.music_button_p[2] < mouse_pos[1] < self.music_button_p[3]:
                if music < 1:
                    music = (int(music * 100) + 5) / 100
            elif self.sound_button_m[0] < mouse_pos[0] < self.sound_button_m[1] and \
                    self.sound_button_m[2] < mouse_pos[1] < self.sound_button_m[3]:
                if sound_effects > 0:
                    sound_effects = (int(sound_effects * 100) - 5) / 100
            elif self.sound_button_p[0] < mouse_pos[0] < self.sound_button_p[1] and \
                    self.sound_button_p[2] < mouse_pos[1] < self.sound_button_p[3]:
                if sound_effects < 1:
                    sound_effects = (int(sound_effects * 100) + 5) / 100
        elif self.screen_number == 2: #окно с титрами
            self.screen_number = 0