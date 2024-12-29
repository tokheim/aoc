import heapq
import numpy as np
import math

def parse_file(fname):
    with open(fname, "r") as f:
        return [l.rstrip() for l in f.readlines()]

def strip_empty_lead_trail(tlines):
    first = 0
    last = 0
    for i, tline in enumerate(tlines):
        if i == first and tline == "":
            first += 1
        if tline != "":
            last = i+1
    return tlines[first:last]

def split_by_nl(tlines):
    instructions = []
    cur_instruction = []
    for tline in tlines:
        if tline != "":
            cur_instruction.append(tline)
        elif len(cur_instruction) > 0:
            instructions.append(cur_instruction)
            cur_instruction = []
    if len(cur_instruction) > 0:
        instructions.append(cur_instruction)
    return instructions

def parse_block(fname):
    tlines = parse_file(fname)
    return strip_empty_lead_trail(tlines)

def parse_instructions(fname):
    tlines = parse_file(fname)
    return split_by_nl(tlines)

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Coord(self.x+other.x, self.y+other.y)

    def subtract(self, other):
        return Coord(self.x-other.x, self.y-other.y)

    def within_bounds(self, lr):
        return self.x >= 0 and self.y >= 0 and self.x < lr.x and self.y < lr.y

    def touching(self):
        coords = []
        for t in [-1, 1]:
            coords.append(Coord(self.x+t, self.y))
            coords.append(Coord(self.x, self.y+t))
        return coords

    def neighbours(self):
        coords = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x != 0 or y != 0:
                    coords.append(Coord(self.x+x, self.y+y))
        return coords

    def rotate_left(self):
        y = -self.x
        x = self.y
        return Coord(x, y)

    def rotate_right(self):
        y = self.x
        x = -self.y
        return Coord(x, y)

    def xdir(self):
        if self.x < 0:
            return -1
        elif self.x > 0:
            return 1
        return 0

    def ydir(self):
        if self.y < 0:
            return -1
        elif self.y > 0:
            return 1
        return 0


    def manhatten_dist(self):
        return abs(self.x) + abs(self.y)

    def idx(self):
        return (self.y, self.x)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.idx() == other.idx()
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.idx())

    def __str__(self):
        return "Coord(x={}, y={})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

class PathNode(object):
    def __init__(self, state, cost):
        self.cost = cost
        self.state = state

    def __lt__(self, other):
        return self.cost < other.cost

class GridPathSolver(object):
    def __init__(self, mat):
        self.mat = mat
        self.reset()

    def reset(self):
        self.visit_cost = np.full(self.mat.shape, -1, dtype=int)
        self.to_check = []
        self.reached_states = []

    def _should_terminate(self, last_node):
        return len(self.to_check) == 0

    def _idx(self, state):
        return state.idx()

    def _is_oob(self, state):
        for idx, dim in zip(state.idx(), self.mat.shape):
            if idx < 0 or idx >= dim:
                return True
        return False

    def _gen_neighbour_nodes(self, node):
        raise NotImplementedError()

    def _should_make_visit(self, state):
        raise NotImplementedError()

    def _has_visit(self, node):
        cost = self.visit_cost[self._idx(node.state)]
        return cost >= 0 and node.cost >= cost

    def _visitable_neighbours(self, node):
        neighbours = []
        for n in self._gen_neighbour_nodes(node):
            if self._is_oob(n.state) or self._has_visit(n):
                continue
            elif self._should_make_visit(n.state):
                neighbours.append(n)
        return neighbours


    def run(self, start):
        n = PathNode(start, 0)
        self.to_check.append(n)
        while not self._should_terminate(n):
            n = heapq.heappop(self.to_check)
            if self._has_visit(n):
                continue
            self.reached_states.append(n)
            self.visit_cost[self._idx(n.state)] = n.cost
            for neighbour in self._visitable_neighbours(n):
                heapq.heappush(self.to_check, neighbour)
        return n
