class AI(Player):
    def ask(self):
        if g.us.board.busy:
            for i in range(len(g.us.board.busy), 0):
                d = g.us.board.busy[i]
                if g.us.board.field[d.x][d.y] == 'X':
                    near = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 0), (0, 1),
                            (1, -1), (1, 0), (1, 1)
                            ]
                    for dx, dy in near:
                        cur = Dot(d.x + dx, d.y + dy)
                        if not (g.us.board.out(cur)) and cur not in g.us.board.busy:
                            d = cur
                            print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                            return d
                            break
                else:
                    pass
        else:
            d = Dot(randint(0, 5), randint(0, 5))

        d = Dot(randint(0, 5), randint(0, 5))
        while d in g.us.board.busy:
            d = Dot(randint(0, 5), randint(0, 5))

        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d
        # if g.us.board.field[d.x][d.y] == 'X':
        #     near = [(-1, -1), (-1, 0), (-1, 1),
        #             (0, -1), (0, 0), (0, 1),
        #             (1, -1), (1, 0), (1, 1)
        #             ]
        #     for dx, dy in near:
        #         cur = Dot(d.x + dx, d.y + dy)
        #         if not (g.us.board.out(cur)) and cur not in g.us.board.busy:
        #             d = cur
        #             break
        # else:
        #     d = Dot(randint(0, 5), randint(0, 5))
        #     while d in self.board.busy:
        #         d = Dot(randint(0, 5), randint(0, 5))

        # print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        # return d