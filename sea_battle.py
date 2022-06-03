class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, ship_len, orient):
        self.bow = bow #bow - координаты носа коробля
        self.ship_len = ship_len #ship_len - длинна коробля
        self.orient = orient  #orient - ориентация коробля в пространстве: 0 - вертикально, 1 - горизонтально
        self.lives = ship_len #lives - живучесть коробля = длинна коробля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_len):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shot_func(self, shot):
        return shot in self.dots

class GameField:
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size

        self.sunken = 0 # Счетчик затопленных кораблей

        self.field = [['0']*size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        draw_field = ''
        draw_field = draw_field + '   | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            draw_field = +f'\n{i+1} | '




ff = GameField()

print(ff.field)






s = Ship(Dot(3, 1), 3, 0)
print(s.dots)
print(s.shot_func(Dot(4, 4)))