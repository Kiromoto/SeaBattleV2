from random import randint


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
        self.bow = bow  # bow - координаты носа коробля
        self.ship_len = ship_len  # ship_len - длинна коробля
        self.orient = orient  # orient - ориентация коробля в пространстве: 0 - вертикально, 1 - горизонтально
        self.lives = ship_len  # lives - живучесть коробля = длинна коробля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_len):
            cur_x = self.bow.x - 1
            cur_y = self.bow.y - 1

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:  # Board
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.sunken = 0  # Счетчик затопленных кораблей

        self.field = [['0'] * size for _ in range(size)]

        self.busy = []  # Точка игрового поля с кораблем или выстрелом
        self.ships = []  # Точки игрового поля со всеми кораблями игрока

    def __str__(self):
        draw_field = ''
        draw_field = draw_field + '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            draw_field += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            draw_field = draw_field.replace('■', 'O')
        return draw_field

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

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
        # d.x -= 1
        # d.y -= 1

        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                # if d in ship.dots:
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

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy, username=''):
        self.board = board
        self.enemy = enemy
        self.username = username

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        if self.enemy.busy:
            for i in reversed(range(len(self.enemy.busy))):
                d = self.enemy.busy[i]
                if self.enemy.field[d.x][d.y] == 'X':
                    near = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 0), (0, 1),
                            (1, -1), (1, 0), (1, 1)
                            ]
                    for dx, dy in near:
                        cur = Dot(d.x + dx, d.y + dy)
                        if not (self.enemy.out(cur)) and cur not in self.enemy.busy:
                            d = cur
                            print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                            return d
                            break

        d = Dot(randint(0, 5), randint(0, 5))
        while d in self.enemy.busy:
            d = Dot(randint(0, 5), randint(0, 5))

        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


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


class Game:
    def __init__(self, size=6):
        self.size = size
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        pl = self.random_board()
        co = self.random_board()
        co.hid = True  # True для скрытия поля компьютера от игрока!

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print('----------------------------')
        print(' Добро пожаловать, в игру!  ')
        print('         МОРСКОЙ БОЙ        ')
        print('----------------------------')
        print('         ИНСТРУКЦИЯ         ')
        print('1. Игрок ходит первым')
        print('2. Чтобы выстрелить в корабль')
        print('   ведите координаты x и y: ')
        print('   x - номер строки         ')
        print('   y - номер столбца        ')
        print('         УДАЧИ!!!           ')
        print('----------------------------')
        User.username = input('Введите Ваше имя: ')

    def show_both_board(self):
        draw_both_board = ''
        pr_board = self.us.board.__str__().replace('\n', ' ')
        pr_enemy = self.us.enemy.__str__().replace('\n', ' ')
        draw_both_board = draw_both_board + 'Доска пользователя:' + ' ' * 28 + 'Доска компьютера:\n'
        for i in range(0, len(pr_board), 28):
            draw_both_board += f'{pr_board[i:i + 27]}' + ' ' * 20 + f'{pr_enemy[i:i + 27]}\n'

        return draw_both_board[:-1]

    def loop(self):
        num = 0
        while True:
            print("-" * 74)
            print(self.show_both_board())

            if num % 2 == 0:
                print("-" * 74)
                print(" " * 47 + "Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 74)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.sunken == 7:
                print("-" * 74)
                print(self.show_both_board())
                print("-" * 74)
                print(" " * 47 + f"Пользователь {User.username} выиграл!")
                break

            if self.us.board.sunken == 7:
                print("-" * 74)
                print(self.show_both_board())
                print("-" * 74)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
