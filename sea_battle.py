from random import randint
from lib.Ship import Ship
from lib.Board import Board, Dot, BoardShipAddWrongException
from lib.Player import AI, User


class Game:
    def __init__(self, game_size=6) -> None:
        self.__game_size = game_size
        self.__ships_count = [3, 2, 2, 1, 1, 1, 1]
        player = self.random_board()
        computer = self.random_board()
        computer.hid = True  # True для скрытия поля компьютера от игрока!

        self.__ai = AI(computer, player)
        self.__us = User(player, computer)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size=self.__game_size)
        attempts = 0
        for s in self.__ships_count:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.__game_size), randint(0, self.__game_size)), s, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipAddWrongException:
                    pass
        board.reset()
        return board

    def show_both_board(self):
        draw_both_board = ''
        pr_board = self.__us.board.__str__().replace('\n', ' ')
        pr_enemy = self.__us.enemy.__str__().replace('\n', ' ')
        draw_both_board += 'Доска игрока:' + ' ' * 34 + 'Доска компьютера:\n'
        for i in range(0, len(pr_board), 28):
            draw_both_board += f'{pr_board[i:i + 27]}' + ' ' * 20 + f'{pr_enemy[i:i + 27]}\n'

        return draw_both_board[:-1]

    def greet(self):
        space = 23 * ' '
        print(74 * '-')
        print(space + ' Добро пожаловать, в игру!  ')
        print(space + '         МОРСКОЙ БОЙ        ')
        print(74 * '-')
        print(space + 'ИНСТРУКЦИЯ:')
        print(space + '1. Игрок ходит первым')
        print(space + '2. Чтобы выстрелить в корабль')
        print(space + '   ведите координаты x и y: ')
        print(space + 'x - номер строки, y - номер столбца')
        print(space + '         УДАЧИ!!!           ')
        print(74 * '-')
        User.username = str(input(space + 'Введите Ваше имя: '))

    def loop(self):
        num = 0
        while True:
            print("-" * 74)
            print(self.show_both_board())

            if num % 2 == 0:
                print("-" * 74)
                print(" " * 47 + "Ходит игрок!")
                repeat = self.__us.move(num)
            else:
                print("-" * 74)
                print("Ходит компьютер!")
                repeat = self.__ai.move(num)

            if self.__ai.board.sunken == self.__ships_count.__len__():
                print("-" * 74)
                print(self.show_both_board())
                print("-" * 74)
                print(" " * 47 + f"Игрок {User.username} выиграл!")
                break

            if self.__us.board.sunken == self.__ships_count.__len__():
                print("-" * 74)
                print(self.show_both_board())
                print("-" * 74)
                print("Компьютер выиграл!")
                break

            if not repeat:
                num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    g = Game()
    g.start()
