import aoc_utils
import numpy as np

def parse_map(tlines):
    h = len(tlines)
    w = len(tlines[0])
    mat = np.zeros((h, w), dtype=int)
    start = None
    end = None
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            if c == "#":
                mat[y, x] = -1
            elif c == "S":
                start = aoc_utils.Coord(x, y)
            elif c == "E":
                end = aoc_utils.Coord(x, y)
    return Track(mat, start, end)

class Track(object):
    def __init__(self, mat, start, end):
        self.mat = mat
        self.start = start
        self.end = end

    def traverse_costs(self):
        prev = self.start
        current = self.start
        cur_cost = 0
        while current != self.end:
            self.mat[current.y, current.x] = cur_cost
            next_node = self.next_visit(prev, current)
            prev = current
            current = next_node
            cur_cost += 1
        self.mat[self.end.y, self.end.x] = cur_cost
        count = np.sum(self.mat == 0)
        if count != 1:
            raise AssertionError("Assumed all nodes visited")

    def next_visit(self, prev, current):
        found = None
        for n in current.touching():
            if self.mat[n.y, n.x] < 0:
                continue
            elif n == prev:
                continue
            elif found is not None:
                raise AssertionError("Assumed single path")
            found = n
        if found is None:
            raise AssertionError("Dead end")
        return found

    @property
    def w(self):
        return self.mat.shape[1]

    @property
    def h(self):
        return self.mat.shape[0]

    @property
    def lr(self):
        return aoc_utils.Coord(self.w, self.h)

    def find_shortcuts(self, maxlength):
        shortcuts = []
        for y in range(self.h):
            for x in range(self.w):
                p = aoc_utils.Coord(x, y)
                found = self._shortcuts_at(p, maxlength)
                shortcuts.extend(found)
        return shortcuts

    def _shortcuts_at(self, start, maxlength):
        found = []
        startcost = self.mat[start.y, start.x]
        startdist = start.manhatten_dist()
        if startcost < 0:
            return found
        sf = ShortcutFinder(self.mat, maxlength)
        sf.run(start)
        for dst in sf.reached_states:
            pos = dst.state
            val = self.mat[pos.y, pos.x]
            if val < 0:
                continue
            saved = val - (startcost + dst.cost)
            if saved > 0:
                found.append(Shortcut(start, pos, saved))
        return found

class ShortcutFinder(aoc_utils.GridPathSolver):
    def __init__(self, mat, max_length):
        aoc_utils.GridPathSolver.__init__(self, mat)
        self.max_length = max_length

    def _gen_neighbour_nodes(self, node):
        c = node.state
        if node.cost >= self.max_length:
            return []
        neighbours = []
        for nc in c.touching():
            neighbours.append(aoc_utils.PathNode(nc, node.cost+1))
        return neighbours

    def _should_make_visit(self, state):
        return True


class Shortcut(object):
    def __init__(self, start, end, savings):
        self.start = start
        self.end = end
        self.savings = savings

def shortcut_stats(shortcuts):
    save_map = dict()
    for s in shortcuts:
        save_map[s.savings] = save_map.get(s.savings, 0) + 1
    all_items = sorted(list(save_map.items()))
    for savings, counts in all_items[-15:]:
        pass
        print("There are {} cheats that save {} picoseconds.".format(counts, savings))
    total = len([s for s in shortcuts if s.savings >= 100])
    print("There are {} cheats more than 100 picoseconds.".format(total))

def main(fname):
    tlines = aoc_utils.parse_block(fname)
    track = parse_map(tlines)
    track.traverse_costs()

    sf = ShortcutFinder(track.mat, 20)
    sf.run(aoc_utils.Coord(1, 1))

    shortcuts = track.find_shortcuts(2)
    print("===len 2  stats====")
    shortcut_stats(shortcuts)

    shortcuts = track.find_shortcuts(20)
    print("===len 20 stats===")
    shortcut_stats(shortcuts)

#main("in/in_20_test.txt")
main("in/in_20.txt")
