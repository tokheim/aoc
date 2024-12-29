import aoc_utils
import numpy as np

class Lock(object):
    def __init__(self, heights):
        self.heights = heights

    def __repr__(self):
        return "Lock"+str(self.heights)

    def __str__(self):
        return self.__repr__()

class Key(object):
    def __init__(self, heights):
        self.heights = heights

    def fits(self, lock):
        for kh, lh in zip(self.heights, lock.heights):
            if kh + lh > 5:
                return False
        return True

    def __repr__(self):
        return "Key"+str(self.heights)

    def __str__(self):
        return self.__repr__()

def is_lock(tlines):
    return tlines[0] == "#####"

def parse_heights(tlines):
    heights = []
    for x in range(len(tlines[0])):
        for y in range(len(tlines)):
            if tlines[y][x] != "#":
                heights.append(y-1)
                break
        if len(heights) <= x:
            heights.append(len(tlines)-2)
    return heights

def parse_schematics(tline_blocks):
    locks = []
    keys = []
    for tlines in tline_blocks:
        lock = is_lock(tlines)
        if not lock:
            tlines = list(reversed(tlines))
        heights = parse_heights(tlines)
        if lock:
            locks.append(Lock(heights))
        else:
            keys.append(Key(heights))
    return locks, keys

def unique_fitting_pairs(locks, keys):
    n = 0
    for lock in locks:
        for key in keys:
            if key.fits(lock):
                n += 1
    return n

def main(fname):
    tline_blocks = aoc_utils.parse_instructions(fname)
    locks, keys = parse_schematics(tline_blocks)
    print(unique_fitting_pairs(locks, keys))

main("in/in_25_test.txt")
main("in/in_25.txt")
