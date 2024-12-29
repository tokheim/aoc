import aoc_utils
import heapq
import numpy as np

_MAX_COST = 1e9

def parse_maze(tlines):
    h = len(tlines)
    w = len(tlines[0])
    mat = np.zeros((h, w), dtype=int)
    s = None
    e = None
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            if c == "#":
                mat[y, x] = 1
            elif c == "S":
                s = aoc_utils.Coord(x, y)
            elif c == "E":
                e = aoc_utils.Coord(x, y)
    return Maze(mat, s, e)


class Maze(object):
    def __init__(self, mat, s, e):
        self.wall_mask = mat
        self.s = s
        self.e = e

    @property
    def initial_state(self):
        direction = aoc_utils.Coord(1, 0)
        return DeerState(self.s, direction)

    @property
    def walkable_mask(self):
        h, w = self.wall_mask.shape
        mask = np.ones((h, w, 4), dtype=int) * _MAX_COST
        mask[self.wall_mask == 1, :] = -1
        return mask

class PathRes(object):
    def __init__(self, best_states):
        self.best_map = {}
        for s in best_states:
            self.best_map[self._key(s)] = s

    def _key(self, state):
        return (state.pos, state.direction)

    def best_states_at(self, coord):
        best = []
        cost = _MAX_COST
        direction = aoc_utils.Coord(1, 0)
        for _ in range(4):
            s = self.best_map.get((coord, direction))
            if s is not None and s.cost < cost:
                best = [s]
                cost = s.cost
            elif s is not None and s.cost == cost:
                best.append(s)
            direction = direction.rotate_right()
        return best

    def nodes_in_best_path(self, coord):
        to_check = self.best_states_at(coord)
        best_nodes = set()
        while to_check:
            state = to_check.pop()
            bs = self.best_map.get(self._key(state))
            if bs is not None and bs.cost == state.cost:
                best_nodes.add(bs.pos)
                to_check.extend(bs.previous_moves())
        return best_nodes

class PathSolver(object):
    def __init__(self, walkable_mask, initial_state):
        self.walkable_mask = walkable_mask
        self.queue = [initial_state]
        self.best_states = []

    def _dir_idx(self, direction):
        if direction.y == 1:
            return 0
        elif direction.y == -1:
            return 1
        elif direction.x == 1:
            return 2
        return 3

    def _state_idx(self, state):
        return (state.pos.y, state.pos.x, self._dir_idx(state.direction))

    def run(self):
        while self.queue:
            state = heapq.heappop(self.queue)
            self._visit_node(state)
        return PathRes(self.best_states)

    def _visit_node(self, state):
        idx = self._state_idx(state)
        if self.walkable_mask[idx] <= state.cost and state.cost > 0:
            return
        self.walkable_mask[idx] = state.cost
        self.best_states.append(state)
        for next_state in state.next_moves():
            if self.walkable_mask[self._state_idx(next_state)] > 0:
                heapq.heappush(self.queue, next_state)




class DeerState(object):
    def __init__(self, pos, direction, cost=0):
        self.pos = pos
        self.direction = direction
        self.cost = cost

    def walk(self):
        return DeerState(self.pos.add(self.direction), self.direction, self.cost+1)

    def turn_l(self):
        return DeerState(self.pos, self.direction.rotate_left(), self.cost+1000)

    def turn_r(self):
        return DeerState(self.pos, self.direction.rotate_right(), self.cost+1000)

    def next_moves(self):
        return [self.walk(), self.turn_l(), self.turn_r()]

    def previous_moves(self):
        return [
                DeerState(self.pos.subtract(self.direction), self.direction, self.cost-1),
                DeerState(self.pos, self.direction.rotate_left(), self.cost-1000),
                DeerState(self.pos, self.direction.rotate_right(), self.cost-1000)
                ]

    def __lt__(self, other):
        return self.cost < other.cost

def main(fname):
    tlines = aoc_utils.parse_block(fname)
    maze = parse_maze(tlines)
    solver = PathSolver(maze.walkable_mask, maze.initial_state)
    path_res = solver.run()
    print(path_res.best_states_at(maze.e)[0].cost)
    print(len(path_res.nodes_in_best_path(maze.e)))

main("in/in_16_test.txt")
main("in/in_16.txt")
