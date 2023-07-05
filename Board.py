# from sea_battle2 import BoardWrongShipException, BoardOutException, BoardUsedException
from Dot import Dot


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):  # Зачем это исключение?
    pass


class Board:  # Board
    def __init__(self, hid:bool=False, size:int=6) -> None:
        self.__hid = hid
        self.__size = size
        self.sunken = 0  # Счетчик затопленных кораблей
        self.field = [['0'] * self.__size for _ in range(self.__size)]
        self.busy = []  # Точка игрового поля с кораблем или выстрелом
        self.ships = []  # Точки игрового поля со всеми кораблями игрока

    @property
    def hid(self):
        return self.__hid

    @hid.setter
    def hid(self, _hid:bool):
        self.__hid = _hid
        return self.__hid

    def __str__(self):
        draw_field = '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            draw_field += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            draw_field = draw_field.replace('■', 'O')
        return draw_field

    def out(self, point):
        return not ((0 <= point.x < self.__size) and (0 <= point.y < self.__size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, _shotpoint):
        if self.out(_shotpoint):
            raise BoardOutException()

        if _shotpoint in self.busy:
            raise BoardUsedException()

        self.busy.append(_shotpoint)

        for ship in self.ships:
            if ship.shooten(_shotpoint):
                ship.lives -= 1
                self.field[_shotpoint.x][_shotpoint.y] = "X"
                if ship.lives == 0:
                    self.sunken += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[_shotpoint.x][_shotpoint.y] = "."
        print("Мимо!")
        return False

    def reset(self):
        self.busy = []


# b = Board(True)
# # print(b.field)
# print(b)
# print('_____________________________________________________________________________')
# print(f'{b.hid}')
# print(f'{b.size}')
# print(b.sunken)
# print(b.busy)
# print(b.ships)
# print('_____________________________________________________________________________')
