from random import randint
from Ship import Ship
from Board import Board, Dot, BoardException, BoardOutException, BoardUsedException, BoardWrongShipException



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
    def __init__(self, game_size=6):
        self.game_size = game_size
        self.ships_count = [3, 2, 2, 1, 1, 1, 1]
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
        board = Board(size=self.game_size)
        attempts = 0
        for s in self.ships_count:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.game_size), randint(0, self.game_size)), s, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.reset()
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
        draw_both_board += 'Доска пользователя:' + ' ' * 28 + 'Доска компьютера:\n'
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
