


class Dot:
    def __init__(self, x:int, y:int) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, point):
        return self.__x == point.x and self.__y == point.y

    def __repr__(self):
        return f'Dot({self.__x}, {self.__y})'
