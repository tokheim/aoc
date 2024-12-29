import aoc_utils
import numpy


def parse_map(tlines, cc):
    w, h = len(tlines[0]), len(tlines)
    mat = numpy.zeros((h, w), dtype=int)
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            n = cc.color_for(c)
            mat[y, x] = n
    return mat

class ColorConverter(object):
    def __init__(self):
        self._map = {}

    @staticmethod
    def gen_from(arr):
        cc = ColorConverter()
        for i, v in enumerate(arr):
            cc._map[v] = i
        return cc

    def color_for(self, c):
        if c in self._map:
            return self._map[c]
        n = len(self._map)
        self._map[c] = n
        return n

    def letter_for(self, n):
        for k, v in self._map.items():
            if n == v:
                return k
        raise ValueError("unknown color "+str(n))

def generate_gardens(mat, cc):
    walked = numpy.zeros(mat.shape, dtype=int)
    gardens = []
    for y in range(mat.shape[0]):
        for x in range(mat.shape[1]):
            if walked[y, x] == 0:
                c = aoc_utils.Coord(x=x, y=y)
                letter = cc.letter_for(mat[y, x])
                garden = gen_garden_at(c, mat, letter)
                walked += garden.mat
                gardens.append(garden)
    return gardens

def gen_garden_at(coord, mat, letter):
    lr = aoc_utils.Coord(mat.shape[1], mat.shape[0])
    scan_val = mat[coord.y, coord.x]
    to_check = [coord]
    garden_mat = numpy.zeros(mat.shape, dtype=int)
    while to_check:
        c = to_check.pop()
        if c.within_bounds(lr) and mat[c.y, c.x] == scan_val and garden_mat[c.y, c.x] == 0:
            garden_mat[c.y, c.x] = 1
            to_check.extend(c.touching())
    return GardenMap(garden_mat, coord, letter)

class GardenMap(object):
    def __init__(self, mat, tl_point, letter):
        self.mat = mat
        self.tl_point = tl_point
        self.letter = letter

    def snap_map_to_edge(self):
        xvals = numpy.max(self.mat, axis=0)
        yvals = numpy.max(self.mat, axis=1)
        y_min = numpy.argmax(yvals)
        x_min = numpy.argmax(xvals)
        h = numpy.sum(yvals)
        w = numpy.sum(xvals)
        origo = aoc_utils.Coord(x_min, y_min)
        mat = self.mat[y_min:y_min+h, x_min:x_min+w]
        return GardenMap(mat, self.tl_point.subtract(origo), self.letter)

    def interior_gardens(self):
        if not self.touches_map_edge:
            raise AssertionError("Interior gardens assumes zoomed in map")
        cc = ColorConverter.gen_from(["i_"+self.letter, self.letter])
        all_gardens = generate_gardens(self.mat, cc)
        return [g for g in all_gardens if not g.touches_map_edge]

    @property
    def touches_map_edge(self):
        xvals = numpy.max(self.mat, axis=0)
        if xvals[0] != 0 or xvals[-1] != 0:
            return True
        yvals = numpy.max(self.mat, axis=1)
        return yvals[0] != 0 or yvals[-1] != 0

    @property
    def sides(self):
        c = self.outer_sides
        interiors = self.interior_gardens()
        for ig in interiors:
            c += ig.outer_sides
        return c

    @property
    def outer_sides(self):
        start_delta = aoc_utils.Coord(x=1, y=0)
        delta = start_delta
        turns = 0
        pos = self.tl_point
        while turns < 3 or pos != self.tl_point or delta != start_delta:
            #print(turns, pos, delta)
            preferred_turn = pos.add(delta).add(delta.rotate_left())
            if self.is_garden(preferred_turn):
                turns += 1
                pos = preferred_turn
                delta = delta.rotate_left()
            elif self.is_garden(pos.add(delta)):
                pos = pos.add(delta)
            else:
                turns += 1
                delta = delta.rotate_right()
        return turns


    def is_garden(self, c):
        h, w = self.mat.shape
        if c.y < 0 or c.x < 0 or c.y >= h or c.x >= w:
            return False
        return self.mat[c.y, c.x] != 0

    @property
    def area(self):
        return numpy.sum(self.mat)

    @property
    def perimiter(self):
        c = 0
        for y in range(self.mat.shape[0]):
            c += self._crossings(self.mat[y, :])
        for x in range(self.mat.shape[1]):
            c += self._crossings(self.mat[:, x])
        return c

    def _crossings(self, vect):
        prev_state = 0
        c = 0
        for v in vect:
            if v != prev_state:
                prev_state = v
                c += 1
        if prev_state != 0:
            c += 1
        return c



def main(fname):
    tlines = aoc_utils.parse_block(fname)
    cc = ColorConverter()
    mat = parse_map(tlines, cc)
    gardens = generate_gardens(mat, cc)
    gardens = [g.snap_map_to_edge() for g in gardens]
    total = sum(g.area * g.perimiter for g in gardens)
    print(total)
    total = sum(g.area * g.sides for g in gardens)
    print(total)

main("in/in_12.txt")
