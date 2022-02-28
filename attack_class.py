import my_functions as f
import pygame


class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.hit_sprites = [f.load_my_image(f"hit_{i}.png") for i in range(0, 10)]
        self.x = x #х и у
        self.y = y
        self.width = f.tile_width #ширина и высота
        self.height = f.tile_height
        self.image = self.hit_sprites[0] #стартовое изображение
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
            self.image = self.hit_sprites[self.frames]
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
        # обнуление позиции
        self.rot_current_pos[0], self.rot_current_pos[1] = self.rot_current_pos[0] * -1, self.rot_current_pos[1] * -1
        self.rect = self.rect.move(self.rot_current_pos)
        self.rotate_angle = -self.rotate_angle
        for i in range(len(self.hit_sprites)):
            self.hit_sprites[i] = pygame.transform.rotate(self.hit_sprites[i], self.rotate_angle)
        self.rotate_angle = rot
        #поворот в нужную сторону
        for i in range(len(self.hit_sprites)):
            self.hit_sprites[i] = pygame.transform.rotate(self.hit_sprites[i], rot)
        self.rect = self.image.get_rect(left=self.rect.left, top=self.rect.top)
        self.rot_current_pos[0] = self.rot_positions[int(rot / 90)][0]
        self.rot_current_pos[1] = self.rot_positions[int(rot / 90)][1]
        #смещение в нужную сторону
        self.rect = self.rect.move(self.rot_current_pos)

