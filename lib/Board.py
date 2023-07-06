from Dot import Dot


class BoardException(Exception):
    pass


class BoardShotOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"


class BoardShotBusyException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardShipAddWrongException(BoardException):
    # Исключение для ошибки размещения корабля!
    pass


class Board:  # Board
    def __init__(self, hid: bool = False, size: int = 6) -> None:
        self.__hid = hid
        self.__size = size
        self.__sunken = 0  # Счетчик затопленных кораблей
        self.__field = [['0'] * self.__size for _ in range(self.__size)]
        self.__busy = []  # Точка игрового поля с кораблем или выстрелом
        self.__ships = []  # Точки игрового поля со всеми кораблями игрока

    @property
    def hid(self):
        return self.__hid

    @hid.setter
    def hid(self, _hid: bool):
        self.__hid = _hid
        return self.__hid

    @property
    def sunken(self):
        return self.__sunken

    @property
    def field(self):
        return self.__field

    @property
    def busy(self):
        return self.__busy

    def __str__(self):
        draw_field = '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.__field):
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
                point = Dot(d.x + dx, d.y + dy)
                if not (self.out(point)) and point not in self.__busy:
                    if verb:
                        self.__field[point.x][point.y] = '.'
                    self.__busy.append(point)

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.__busy:
                raise BoardShipAddWrongException()
        for dot in ship.dots:
            self.__field[dot.x][dot.y] = "■"
            self.__busy.append(dot)

        self.__ships.append(ship)
        self.contour(ship)

    def shot(self, _shotpoint, _num: int):
        if self.out(_shotpoint):
            raise BoardShotOutException()

        if _shotpoint in self.__busy:
            raise BoardShotBusyException()

        self.__busy.append(_shotpoint)

        if _num % 2 == 0:
            space = ' ' * 47
        else:
            space = ''

        for ship in self.__ships:
            if ship.shooten(_shotpoint):
                ship.lives -= 1
                self.__field[_shotpoint.x][_shotpoint.y] = "X"
                if ship.lives == 0:
                    self.__sunken += 1
                    self.contour(ship, verb=True)
                    print(space + "Корабль уничтожен!")
                else:
                    print(space + "Корабль ранен!")
                return True

        # self.__field[_shotpoint.x][_shotpoint.y] = "T" # Так нужно обозначать промах в соответствии с условиями задачи
        self.__field[_shotpoint.x][
            _shotpoint.y] = "."  # Заменил обозначение промаха на точку, потому что так лучше воспринимать ход игры
        print(space + "Мимо!")
        return False

    def reset(self):
        self.__busy = []
