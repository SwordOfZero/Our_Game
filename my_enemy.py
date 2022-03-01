import my_functions as f
import pygame
import attack_class as atk

#класс игрока
class Enemies(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(f.enemy_group)
        self.enemy_sprites = [f.load_my_image(f"enemy_{i // 3 + 1}{i % 3 + 1}.png") for i in range(0, 12)]
        self.y_speed = 3 #скорость по х и у
        self.x_speed = 3
        self.image = self.enemy_sprites[0] #начальное изображение игрока
        self.pos_x = pos_x #установка начальной позиции по х и у
        self.pos_y = pos_y
        self.spawn = [pos_x, pos_y]
        self.rect = self.image.get_rect().move(pos_x, pos_y) #создание "тела" по размеру изображения
        self.frames = 0 #индекс кадра анимации
        self.rotate = 0 #индекс угла поворота игрока
        self.rotate_angles = [180, 270, 0, 90] #список углов поворота, зависящий от индекса
        self.sword = atk.Attack(pos_x, pos_y) #создание атаки для героя
        self.level_x = 0
        self.level_y = 0
        self.timer = 0
        self.hp = 3
        self.hptimer = 0
        self.died = False

    #функция, добавляющая атаку в группу всех спрайтов и оружия героя
    def add_sword(self):
        f.all_sprites.add(self.sword)
        f.enemy_weapon_group.add(self.sword)

    #получение текущей позиции игрока
    def get_pos(self):
        return [self.pos_x, self.pos_y]

    def get_map_size(self, lx, ly):
        self.level_x = lx
        self.level_y = ly

    def brain(self, player_coord):
        if self.timer != 0:
            self.timer -= 1
        if self.hptimer != 0:
            self.hptimer -= 1
        self.die()
        way = [False, False, False, False]
        player_coord = [self.pos_x - player_coord[0], self.pos_y - player_coord[1]]
        if not self.sword.playing:
            if abs(player_coord[0]) < 150 and abs(player_coord[1]) < 150:
                if player_coord[0] > 35:
                    way[3] = True
                elif player_coord[0] < -35:
                    way[1] = True
                if player_coord[1] > 35:
                    way[0] = True
                elif player_coord[1] < -35:
                    way[2] = True
            if f.nor([abs(self.pos_x - self.spawn[0]) > 300, abs(self.pos_y - self.spawn[1]) > 300]):
                self.rect = self.rect.move(self.spawn[0] - self.pos_x, self.spawn[1] - self.pos_y)
                self.pos_x, self.pos_y = self.spawn[0], self.spawn[1]
            self.move(way)
        if abs(player_coord[0]) < 37 and abs(player_coord[1]) < 37 and self.timer == 0:
            self.timer = 32
        if self.timer == 26 and abs(player_coord[0]) < 37 and abs(player_coord[1]) < 37:
            self.hit(self.rotate)

    #передвижение персонажа
    def move(self, arrow): #передаётся список из 4 да/нет переменных, отвечающих за нажатую кнопку
        self.frames = (self.frames + 1) % 3 #типо анимация
        buffer = [self.pos_x, self.pos_y] #сохранение позиции на всякий случай
        x, y = 0, 0
        if arrow[0]:
            y = -self.y_speed
            self.image = f.animate(self.enemy_sprites, 2, self.frames)
            self.rotate = 2
        elif arrow[2]:
            y = self.y_speed
            self.image = f.animate(self.enemy_sprites, 0, self.frames)
            self.rotate = 0
        if arrow[1]:
            x = self.x_speed
            self.image = f.animate(self.enemy_sprites, 1, self.frames)
            self.rotate = 1
        elif arrow[3]:
            x = -self.x_speed
            self.image = f.animate(self.enemy_sprites, 3, self.frames)
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
        if pygame.sprite.spritecollideany(self, f.wall_group) or \
                  len(pygame.sprite.spritecollide(self, f.enemy_group, False)) > 1:
            x, y = -x, -y
            self.pos_x += x
            self.pos_y += y
            self.rect = self.rect.move(x, y)

    #удар
    def hit(self, rot):
        self.sword.update_position(self.pos_x, self.pos_y) #перемещение меча
        self.sword.rotate(self.rotate_angles[rot]) #поворот в правильную сторону
        self.sword.playing = True
        f.sound_effect_sword.play()

    def get_hit(self, atacking):
        if pygame.sprite.spritecollideany(self, f.hero_weapon_group) and self.hptimer == 0 and atacking:
            self.hptimer = 16
            self.hp -= 1

    def die(self):
        if self.hp == 0:
            self.kill()
            self.died = True
            self.sword.kill()
            del self
