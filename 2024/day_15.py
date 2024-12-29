import aoc_utils
import numpy as np

def parse_moves(tlines):
    line = "".join(tlines)
    m_map = dict()
    m_map["<"] = aoc_utils.Coord(-1,0)
    m_map["^"] = aoc_utils.Coord(0, -1)
    m_map["v"] = aoc_utils.Coord(0, 1)
    m_map[">"] = aoc_utils.Coord(1, 0)

    cmds = []
    for c in line:
        cmds.append(m_map[c])
    return cmds

def parse_map(tlines):
    h = len(tlines)
    w = len(tlines[0])
    mat = np.zeros((h, w), dtype=int)
    player = None
    boxnum = 1
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            if c == "#":
                mat[y, x] = -1
            elif c == "O":
                mat[y, x] = boxnum
                boxnum += 1
            elif c == "@":
                player = aoc_utils.Coord(x, y)
    return Warehouse(mat, player)

class Warehouse(object):
    def __init__(self, mat, player):
        self.mat = mat
        self.player = player

    def gps_sum(self):
        score = 0
        last_num = -1
        for y in range(self.mat.shape[0]):
            for x in range(self.mat.shape[1]):
                v = self.mat[y, x]
                if v > 0 and v != last_num:
                    c = aoc_utils.Coord(x, y)
                    score += self.gps_coord(c)
                    last_num = v
        return score

    def gps_coord(self, pos):
        return (100*pos.y) + pos.x

    def widen(self):
        player = aoc_utils.Coord(self.player.x * 2, self.player.y)
        h, w = self.mat.shape
        newmat = np.zeros((h, 2*w), dtype=int)
        for y in range(h):
            for x in range(w):
                v = self.mat[y, x]
                newmat[y, 2*x] = v
                newmat[y, (2*x) + 1] = v
        return Warehouse(newmat, player)

    def perform_moves(self, cmds):
        for cmd in cmds:
            self.perform_move(cmd)

    def perform_move(self, direction):
        if self._can_push(self.player, direction):
            self._do_push(self.player, direction)
            self.player = self.player.add(direction)

    def box_coords(self, at):
        v = self.mat[at.y, at.x]
        if self.mat[at.y, at.x+1] == v:
            other = aoc_utils.Coord(at.x+1, at.y)
            return [at, other]
        if self.mat[at.y, at.x-1] == v:
            other = aoc_utils.Coord(at.x-1, at.y)
            return [other, at]
        return [at]

    def opposite_box_edges(self, p, direction):
        coords = self.box_coords(p)
        if direction.x == 0:
            return coords
        elif direction.x == 1:
            return [coords[-1]]
        else:
            return [coords[0]]

    def sorted_box_coords(self, p, direction):
        coords = self.box_coords(p)
        if direction.x == 0 or len(coords) == 1:
            return coords
        elif direction.x == 1:
            return [coords[-1], coords[0]]
        return coords



    def _can_push(self, pos, direction):
        to = pos.add(direction)
        if self.mat[to.y, to.x] == -1:
            return False
        elif self.mat[to.y, to.x] == 0:
            return True
        for c in self.opposite_box_edges(to, direction):
            possible = self._can_push(c, direction)
            if not possible:
                return False
        return True

    def _do_push(self, pos, direction):
        to = pos.add(direction)
        if self.mat[to.y, to.x] == -1:
            raise AssertionError("cant push")
        elif self.mat[to.y, to.x] > 0:
            for c in self.sorted_box_coords(to, direction):
                self._do_push(c, direction)
        self.mat[to.y, to.x] = self.mat[pos.y, pos.x]
        self.mat[pos.y, pos.x] = 0

def main(fname):
    textmap, textcmds = aoc_utils.parse_instructions(fname)
    cmds = parse_moves(textcmds)
    warehouse = parse_map(textmap)

    wide = warehouse.widen()

    warehouse.perform_moves(cmds)
    print(warehouse.gps_sum())

    wide.perform_moves(cmds)
    print(wide.gps_sum())

main("in/in_15_test.txt")
main("in/in_15.txt")
