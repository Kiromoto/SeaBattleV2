class User:
    def __init__(self, name, birth_date, rights) -> None:
        self.__name = name
        self.__birth_date = birth_date
        self.__rights = rights

    @property
    def name(self):
        return self.__name

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def rights(self):
        return self.__rights

    @rights.setter
    def rights(self, _new_rights):
        self.__rights = _new_rights
        return self.__rights


if __name__ == "__main__":
    user = User("Vasya", "10.10.10", 7)
    print(user.name)
    print(user.birth_date)
    user.rights = 9
    print(user.rights)
