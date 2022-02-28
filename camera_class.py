import my_functions as f

#камера
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, lx, ly):
        self.dx = 0
        self.dy = 0
        self.level_x = lx
        self.level_y = ly

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
    def start_position(self, target, player):
        width = 300
        height = 300
        #если слишком близко к краю, то регулирует положение камеры
        if 135 <= player.get_pos()[0] <= (self.level_x - 4) * f.tile_width - 15:
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        else:
            left = True
            if player.get_pos()[0] > (self.level_x / 2) * f.tile_width:
                left = False
            if left:
                pass
            else:
                self.dx = -((self.level_x / 2) * f.tile_width)
        if 135 <= player.get_pos()[1] <= (self.level_y - 4) * f.tile_height - 15:
            self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        else:
            up = True
            if player.get_pos()[1] > (self.level_y / 2) * f.tile_height:
                up = False
            if up:
                pass
            else:
                self.dy = -((self.level_y / 2) * f.tile_height + 30)

    def check(self, player):
        # обновляем положение всех спрайтов
        if 135 <= player.get_pos()[0] <= (self.level_x - 4) * f.tile_width - 15:
            self.update_x(player)
        else:
            self.dx = 0
        if 135 <= player.get_pos()[1] <= (self.level_y - 4) * f.tile_height - 15:
            self.update_y(player)
        else:
            self.dy = 0
        for sprite in f.all_sprites:
            self.apply(sprite)
