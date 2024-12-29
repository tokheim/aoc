import aoc_utils
import numpy as np
import heapq

class PathNode(object):
    def __init__(self, pos, time):
        self.pos = pos
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

class MemorySpacePather(object):
    def __init__(self, cor_mask, start, end):
        self.cor_mask = cor_mask
        self.start = start
        self.end = end
        self.reset()

    def reset(self):
        self.visited = np.zeros(self.cor_mask.shape, dtype=int)
        self.queue = []

    def within_bounds(self, pos):
        h, w = self.cor_mask.shape
        return pos.x >= 0 and pos.x < w and pos.y >= 0 and pos.y < h

    def find_best_path(self, last_corrupt):
        self.queue.append(PathNode(self.start, 0))
        found = None
        while self.queue:
            node = heapq.heappop(self.queue)
            if not self._is_visitable(node.pos, last_corrupt):
                continue
            if node.pos == self.end:
                found = node
                break
            self._visit_node(node)
        self.reset()
        if found:
            return found.time
        return -1

    def _visit_node(self, node):
        if self.visited[node.pos.y, node.pos.x] > 0:
            return
        self.visited[node.pos.y, node.pos.x] = 1
        for neighbour in node.pos.touching():
            if self.within_bounds(neighbour):
                n_node = PathNode(neighbour, node.time + 1)
                heapq.heappush(self.queue, n_node)


    def _is_visitable(self, pos, last_corrupt):
        val = self.cor_mask[pos.y, pos.x]
        return val == 0 or val > last_corrupt

def binary_last_viable_search(pather, minval, maxval):
    if minval == maxval:
        return minval
    test = maxval - int((maxval - minval) / 2)
    time = pather.find_best_path(test)
    print("Tested ", test, " res ", time, " seek size ", maxval-minval)
    if time > 0:
        return binary_last_viable_search(pather, test, maxval)
    else:
        return binary_last_viable_search(pather, minval, test-1)

def coord_for_dropped(mat, n):
    idx = np.argmax(mat==n)
    y = idx / mat.shape[0]
    x = idx % mat.shape[1]
    return x, y

def parse_bytemap(tlines, w, h):
    mat = np.zeros((h, w), dtype=int)
    for i, tline in enumerate(tlines, start=1):
        vals = tline.split(",")
        x = int(vals[0])
        y = int(vals[1])
        mat[y, x] = i
    return mat

def main(fname, wh, dropped_bytes):
    tlines = aoc_utils.parse_block(fname)
    mat = parse_bytemap(tlines, wh+1, wh+1)
    start = aoc_utils.Coord(0, 0)
    end = aoc_utils.Coord(wh, wh)
    pather = MemorySpacePather(mat, start, end)
    n = pather.find_best_path(dropped_bytes)
    print("found best path", n)

    n = binary_last_viable_search(pather, 0, len(tlines)+1)
    x, y = coord_for_dropped(mat, n+1)
    print("coord blocking exit", x, y)

main("in/in_18_test.txt", 6, 12)
main("in/in_18.txt", 70, 1024)
