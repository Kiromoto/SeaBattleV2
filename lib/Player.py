from random import randint
from Board import BoardException
from Dot import Dot


class Player:
    def __init__(self, board, enemy, username: str = '') -> None:
        self.__board = board
        self.__enemy = enemy
        self.__username = username

    @property
    def board(self):
        return self.__board

    @property
    def enemy(self):
        return self.__enemy

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, _username: str):
        self.__username = _username
        return self.__username

    def ask(self):
        raise NotImplementedError()

    def move(self, _num: int):
        while True:
            try:
                return self.enemy.shot(self.ask(), _num)
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        if self.enemy.busy:
            for i in reversed(range(len(self.enemy.busy))):
                point = self.enemy.busy[i]
                if self.enemy.field[point.x][point.y] == 'X':
                    near = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 0), (0, 1),
                            (1, -1), (1, 0), (1, 1)
                            ]
                    for dx, dy in near:
                        point = Dot(point.x + dx, point.y + dy)
                        if not (self.enemy.out(point)) and point not in self.enemy.busy:
                            print(f"Ход компьютера: {point.x + 1} {point.y + 1}")
                            return point
                            break

        point = Dot(randint(0, 5), randint(0, 5));
        while point in self.enemy.busy:
            point = Dot(randint(0, 5), randint(0, 5))

        print(f"Ход компьютера: {point.x + 1} {point.y + 1}");
        return point


class User(Player):
    def ask(self):
        while True:
            cords = input(" " * 47 + f"Ваш ход, {User.username}: ").split()

            if len(cords) != 2:
                print(" " * 47 + " Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" " * 47 + " Введите числа! ")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)
