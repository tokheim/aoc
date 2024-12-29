import aoc_utils
import numpy as np

def parse_map(tlines):
    width = len(tlines[0])
    height = len(tlines)
    mat = np.zeros((height, width), dtype=int)
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            mat[y, x] = int(c)
    return mat

def trail_starts(mat):
    height, width = mat.shape
    start_list = []
    for y in range(height):
        for x in range(width):
            if mat[y,x] == 0:
                c = aoc_utils.Coord(x, y)
                start_list.append(c)
    return start_list

def peaks_from(s_coord, mat):
    to_check = set([s_coord])
    for i in range(1, 10):
        found = []
        for c in to_check:
            found.extend(reachable_points(c, mat, i))
        to_check = set(found)
    return to_check


def reachable_points(from_coord, mat, height):
    points = []
    lr = aoc_utils.Coord(mat.shape[1], mat.shape[0])
    for tc in from_coord.touching():
        if tc.within_bounds(lr) and mat[tc.y, tc.x] == height:
            points.append(tc)
    return points

def trails_to_peaks(s_coord, mat):
    point_scores = {}
    point_scores[s_coord] = 1
    for i in range(1, 10):
        found_scores = {}
        for c, score in point_scores.items():
            points = reachable_points(c, mat, i)
            merge_score(score, points, found_scores)
        point_scores = found_scores
    return sum(point_scores.values())

def merge_score(score_for_points, points, prev_scores):
    for p in points:
        score = prev_scores.get(p, 0) + score_for_points
        prev_scores[p] = score

def sum_trail_scores(mat):
    starts = trail_starts(mat)
    n = 0
    for s in starts:
        ends = peaks_from(s, mat)
        n += len(ends)
    return n

def sum_paths(mat):
    starts = trail_starts(mat)
    n = 0
    for s in starts:
        n += trails_to_peaks(s, mat)
    return n

def main(fname):
    mat = parse_map(aoc_utils.parse_block(fname))
    print(mat)
    n = sum_trail_scores(mat)
    print(n)
    n = sum_paths(mat)
    print(n)

main("in/in_10_test.txt")
main("in/in_10.txt")
