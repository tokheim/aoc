import re
import numpy
import aoc_utils

robot_pattern = re.compile("p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)")

class Robot(object):
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def move(self):
        self.p = self.p.add(self.v)

    def apply_teleports(self, map_size):
        x = self.p.x % map_size.x
        y = self.p.y % map_size.y
        self.p = aoc_utils.Coord(x, y)

def parse_robots(tlines):
    robots = []
    for tline in tlines:
        m = robot_pattern.match(tline)
        groups = [int(i) for i in m.groups()]
        p = aoc_utils.Coord(groups[0], groups[1])
        v = aoc_utils.Coord(groups[2], groups[3])
        robots.append(Robot(p, v))
    return robots

class Lobby(object):
    def __init__(self, robots, size):
        self.size = size
        self.robots = robots

    def _update_once(self):
        for r in self.robots:
            r.move()

    def update(self, steps):
        for i in range(steps):
            self._update_once()
        for r in self.robots:
            r.apply_teleports(self.size)

    def render(self):
        mat = numpy.zeros((self.size.y, self.size.x), dtype=int)
        for r in self.robots:
            mat[r.p.y, r.p.x] += 1
        return mat

    def count_islands(self):
        mat = self.render()
        c = 0
        for y in range(self.size.y):
            for x in range(self.size.x):
                if mat[y, x] != 0:
                    c += 1
                    self.remove_island(mat, aoc_utils.Coord(x, y))
        return c

    def remove_island(self, mat, pos):
        unchecked = [pos]
        br = aoc_utils.Coord(mat.shape[1], mat.shape[0])
        while unchecked:
            p = unchecked.pop()
            if not p.within_bounds(br):
                continue
            if mat[p.y, p.x] > 0:
                unchecked.extend(p.neighbours())
                mat[p.y, p.x] = 0

    def str_render(self):
        mat = self.render()
        lines = []
        for y in range(mat.shape[0]):
            linevals = [" "]*mat.shape[1]
            for x in range(mat.shape[1]):
                v = mat[y, x]
                if v == 0:
                    continue
                v = min(9, v)
                linevals[x] = "#"
            lines.append("".join(linevals))
        return "\n".join(lines)


    @property
    def quadrant_width(self):
        return (self.size.x - 1) / 2

    @property
    def quadrant_height(self):
        return (self.size.y - 1) / 2

    @property
    def safety_factor(self):
        mat = self.render()
        quads = self.cut_quadrants(mat)
        n = 1
        for quad in quads:
            n *= numpy.sum(quad)
        return n

    def cut_quadrants(self, mat):
        w = self.quadrant_width
        h = self.quadrant_height
        tl = mat[:h, :w]
        tr = mat[:h, w+1:]
        bl = mat[h+1:, :w]
        br = mat[h+1:, w+1:]
        return [tl, tr, bl, br]

def look_for_promising(lobby):
    best_counts = []
    counts = []
    for i in range(1, 10000):
        lobby.update(1)
        c = lobby.count_islands()
        counts.append((i, c))

        if i % 1000 == 0:
            counts = sorted(counts, key=lambda x: x[1])
            for n, c in counts[:5]:
                print(str(n) + ": " + str(c))
            best_counts.extend(counts[:5])
            counts = []
    best_counts = sorted(best_counts, key=lambda x: x[1])
    for n, c in best_counts:
         print("Best : " + str(n) + ", " + str(c))
    return best_counts

def render_at(lobby, steps):
    current = 0
    for step in sorted(steps):
        lobby.update(step-current)
        current = step
        print(lobby.str_render())
        print("at step "+str(step)+" islands "+str(lobby.count_islands()))
        raw_input("Press Enter to continue...")


def main(fname, sx, sy):
    tlines = aoc_utils.parse_block(fname)
    robots = parse_robots(tlines)
    mapsize = aoc_utils.Coord(sx, sy)
    lobby = Lobby(robots, mapsize)

    #look_for_promising(lobby)
    render_at(lobby, [5028, 79, 1594, 6644, 27450, 37853])

    #lobby.update(100)
    #print(lobby.safety_factor)

#main("in/in_14_test.txt", 11, 7)
main("in/in_14.txt", 101, 103)

