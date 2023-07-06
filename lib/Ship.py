from Dot import Dot


class ShipException(Exception):
    pass


class ShipLivesNegative(ShipException):
    def __str__(self):
        return "Жизнь корабля не может быть отрицательным числом!"


class Ship:
    def __init__(self, bow, ship_len: int, orient: int) -> None:
        self.__bow = bow  # bow - координаты носа корабля
        self.__ship_len = ship_len  # ship_len - длинна корабля
        self.__orient = orient  # orient - ориентация корабля в пространстве: 0 - вертикально, 1 - горизонтально
        self.__lives = ship_len  # lives - живучесть корабля = длинна корабля

    @property
    def dots(self):  # def dots - функция создания всех точек корабля
        self.__ship_dots = []
        for i in range(self.__ship_len):
            cur_x = self.__bow.x - 1
            cur_y = self.__bow.y - 1

            if self.__orient == 0:
                cur_x += i
            elif self.__orient == 1:
                cur_y += i

            self.__ship_dots.append(Dot(cur_x, cur_y))

        return self.__ship_dots

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, _new_lives: int):
        self.__lives = _new_lives
        if self.__lives < 0:
            raise ShipLivesNegative()
        else:
            return self.__lives

    def shooten(self, _shot):
        return _shot in self.__ship_dots

    def __repr__(self):
        return f'Ship(Dot({self.__bow.x}, {self.__bow.y}), length: {self.__ship_len}, orientation: {self.__orient})'
