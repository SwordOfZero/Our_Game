import my_functions as f
import pygame
import attack_class as atk

player_sprites = [f.load_my_image(f"hero_{i // 3 + 1}{i % 3 + 1}.png") for i in range(0, 12)]
#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(f.player_group)
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
        self.sword = atk.Attack(pos_x, pos_y) #создание атаки для героя
        self.level_x = 0
        self.level_y = 0
        self.hp = 10
        self.hptimer = 0

    #функция, добавляющая атаку в группу всех спрайтов и оружия героя
    def add_sword(self):
        f.all_sprites.add(self.sword)
        f.hero_weapon_group.add(self.sword)

    #получение текущей позиции игрока
    def get_pos(self):
        return [self.pos_x, self.pos_y]

    def get_map_size(self, lx, ly):
        self.level_x = lx
        self.level_y = ly

    #передвижение персонажа
    def move(self, arrow): #передаётся список из 4 да/нет переменных, отвечающих за нажатую кнопку
        self.frames = (self.frames + 1) % 3 #типо анимация
        buffer = [self.pos_x, self.pos_y] #сохранение позиции на всякий случай
        x, y = 0, 0
        if arrow[0]:
            y = -self.y_speed
            self.image = f.animate(player_sprites, 2, self.frames)
            self.rotate = 2
        elif arrow[2]:
            y = self.y_speed
            self.image = f.animate(player_sprites, 0, self.frames)
            self.rotate = 0
        elif arrow[1]:
            x = self.x_speed
            self.image = f.animate(player_sprites, 1, self.frames)
            self.rotate = 1
        elif arrow[3]:
            x = -self.x_speed
            self.image = f.animate(player_sprites, 3, self.frames)
            self.rotate = 3
        self.pos_x += x #новая позиция
        self.pos_y += y
        #если новая позиция вне экрана, то возвращается предыдущая позиция
        if ((self.pos_y >= self.level_y * f.tile_height) or (self.pos_y <= 0)) or \
                ((self.pos_x >= self.level_x * f.tile_width) or (self.pos_x <= 0)):
            self.pos_x = buffer[0]
            self.pos_y = buffer[1]
            x, y = 0, 0
        self.rect = self.rect.move(x, y)
        #то же самое, только проверяется пересечение со стенами
        if pygame.sprite.spritecollideany(self, f.wall_group) or pygame.sprite.spritecollideany(self, f.enemy_group):
            x, y = -x, -y
            self.pos_x += x
            self.pos_y += y
            self.rect = self.rect.move(x, y)

    #удар
    def hit(self, rot):
        self.sword.update_position(self.pos_x, self.pos_y) #перемещение меча
        self.sword.rotate(self.rotate_angles[rot]) #поворот в правильную сторону
        if not self.sword.playing:
            f.sound_effect_sword.play()
        self.sword.playing = True

    def get_hit(self, atacking):
        if pygame.sprite.spritecollideany(self, f.enemy_weapon_group) and self.hptimer == 0 and atacking:
            self.hptimer = 18
            self.hp -= 1

    def timer(self):
        if self.hptimer != 0:
            self.hptimer -= 1