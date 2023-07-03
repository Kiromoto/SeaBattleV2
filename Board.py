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
    def __init__(self, hid=False, size=6) -> None:
        self.hid = hid
        self.size = size
        self.sunken = 0  # Счетчик затопленных кораблей
        self.field = [['0'] * size for _ in range(size)]
        self.busy = []  # Точка игрового поля с кораблем или выстрелом
        self.ships = []  # Точки игрового поля со всеми кораблями игрока

    def __str__(self):
        draw_field = '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            draw_field += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            draw_field = draw_field.replace('■', 'O')
        return draw_field

    def out(self, point):
        return not ((0 <= point.x < self.size) and (0 <= point.y < self.size))

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

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.sunken += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def reset(self):
        self.busy = []


b = Board(True)
# print(b.field)
print(b)
print('_____________________________________________________________________________')
print(f'{b.hid}')
print(f'{b.size}')
print(b.sunken)
print(b.busy)
print(b.ships)
print('_____________________________________________________________________________')
