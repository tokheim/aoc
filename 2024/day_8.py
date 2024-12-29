import aoc_utils

def identify_antenna_groups(tlines):
    antenna_map = {}
    for y, tline in enumerate(tlines):
        for x, c in enumerate(tline):
            if c == ".":
                continue
            elif c not in antenna_map:
                antenna_map[c] = []
            antenna_map[c].append((x, y))
    return antenna_map

def gen_antenna_pairs(antenna_map):
    node_pairs = []
    for antennas in antenna_map.values():
        for i, a in enumerate(antennas):
            for b in antennas[i+1:]:
                node_pairs.append((a, b))
    return node_pairs

def list_single_antinodes(antenna_pairs):
    antinodes = set()
    for a, b in antenna_pairs:
        found = calc_antinodes(a, b)
        antinodes = antinodes.union(found)
    return antinodes

def list_harmonic_antinodes(antenna_pairs, tlines):
    height = len(tlines)
    width = len(tlines[0])
    antinodes = set()
    for a, b in antenna_pairs:
        found = calc_h_antinodes(a, b, width, height)
        antinodes = antinodes.union(found)
        found = calc_h_antinodes(b, a, width, height)
        antinodes = antinodes.union(found)
    return antinodes

def calc_h_antinodes(a, b, width, height):
    a_x, a_y = a
    b_x, b_y = b
    d_x = b_x - a_x
    d_y = b_y - a_y
    nodes = []
    i_x, i_y = b_x, b_y
    while within_bounds(i_x, i_y, width, height):
        nodes.append((i_x, i_y))
        i_x += d_x
        i_y += d_y
    return nodes

def calc_antinodes(a, b):
    a_x, a_y = a
    b_x, b_y = b
    d_x = b_x - a_x
    d_y = b_y - a_y
    nodes = []
    nodes.append((b_x+d_x, b_y+d_y))
    nodes.append((a_x-d_x, a_y-d_y))
    return nodes

def within_bounds(x, y, width, height):
    if x < 0 or x >= width:
        return False
    return y >= 0 and y < height

def filter_oob_coords(coords, tlines):
    height = len(tlines)
    width = len(tlines[0])
    ok = []
    for c_x, c_y in coords:
        if within_bounds(c_x, c_y, width, height):
            ok.append((c_x, c_y))
    return ok

def main(fname):
    tlines = aoc_utils.parse_block(fname)
    antenna_map = identify_antenna_groups(tlines)
    antenna_pairs = gen_antenna_pairs(antenna_map)

    antinodes = list_single_antinodes(antenna_pairs)
    antinodes = filter_oob_coords(antinodes, tlines)
    print("single", len(antinodes))

    h_antinodes = list_harmonic_antinodes(antenna_pairs, tlines)
    print("harmonic", len(h_antinodes))

main("in/in_8_test.txt")
main("in/in_8.txt")
