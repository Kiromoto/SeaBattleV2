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

    def shooten(self, shot):
        return shot in self.dots


s = Ship(Dot(3, 1), 3, 0)
print(s.dots)
