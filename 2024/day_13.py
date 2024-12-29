import aoc_utils
import numpy
import re

delta_pattern = re.compile(".* X\\+([0-9]+), Y\\+([0-9]+)")
prize_pattern = re.compile(".* X=([0-9]+), Y=([0-9]+)")

class GameMachine(object):
    def __init__(self, delta_a, delta_b, prize):
        self.delta_a = delta_a
        self.delta_b = delta_b
        self.prize = prize

    def as_matrix(self):
        arr = numpy.asarray([
            self.delta_a.x,
            self.delta_b.x,
            self.prize.x,
            self.delta_a.y,
            self.delta_b.y,
            self.prize.y],
            dtype=float)
        return arr.reshape((2, 3))

    def position_after(self, a_presses, b_presses):
        x = self.delta_a.x * a_presses + self.delta_b.x * b_presses
        y = self.delta_a.y * a_presses + self.delta_b.y * b_presses
        return aoc_utils.Coord(x, y)

    def is_solution(self, a_presses, b_presses):
        pos = self.position_after(a_presses, b_presses)
        return pos.x == self.prize.x and pos.y == self.prize.y

    def floating_solve(self):
        mat = self.as_matrix()
        c = mat[1,0] / mat[0,0]
        mat[1, :] -= mat[0, :] * c
        b_presses = mat[1, 2] / mat[1, 1]

        mat[0, 2] -= b_presses * mat[0, 1]
        mat[0, 1] = 0
        a_presses = mat[0, 2] / mat[0, 0]
        return (a_presses, b_presses)

    def calc_solution(self):
        f_a, f_b = self.floating_solve()
        a = int(round(f_a))
        b = int(round(f_b))
        if self.is_solution(a, b):
            return a, b
        return None

def pattern_coord(line, pattern):
    m = pattern.match(line)
    x = m.groups()[0]
    y = m.groups()[1]
    return aoc_utils.Coord(int(x), int(y))

def parse_game(block):
    da = pattern_coord(block[0], delta_pattern)
    db = pattern_coord(block[1], delta_pattern)
    prize = pattern_coord(block[2], prize_pattern)
    return GameMachine(da, db, prize)

def shift_prizes(prev_games, coord):
    games = []
    for g in prev_games:
        prize = coord.add(g.prize)
        g = GameMachine(g.delta_a, g.delta_b, prize)
        games.append(g)
    return games

def calc_tokens(games):
    tokens = 0
    for g in games:
        solve = g.calc_solution()
        if solve:
            tokens += 3*solve[0] + solve[1]
    return tokens

def main(fname):
    blocks = aoc_utils.parse_instructions(fname)
    games = [parse_game(b) for b in blocks]
    tokens = calc_tokens(games)
    print(tokens)

    measure_val = 10000000000000
    measure_coord = aoc_utils.Coord(measure_val, measure_val)
    games = shift_prizes(games, measure_coord)
    tokens = calc_tokens(games)
    print(tokens)

main("in/in_13_test.txt")
main("in/in_13.txt")
