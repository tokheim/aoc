import aoc_utils

def parse_designs(tline):
    designs = [s.strip() for s in tline.split(",")]
    dispenser = TowelDispenser()
    for design in designs:
        dispenser.add_towel(design)
    return dispenser


class TowelDispenser(object):
    _END_IDX = 5
    def __init__(self):
        self.lookup = []

    def translate_color(self, c):
        if c == "w":
            return 0
        if c == "u":
            return 1
        if c == "b":
            return 2
        if c == "r":
            return 3
        if c == "g":
            return 4
        raise AssertionError("Unknown color "+str(c))

    def _gen_node(self, node):
        if len(node) > 0:
            return
        node.extend([[], [], [], [], [], 0])

    def add_towel(self, towel):
        indices = self.translate_pattern(towel)
        pos = self.lookup
        for idx in indices:
            self._gen_node(pos)
            pos = pos[idx]
        self._gen_node(pos)
        pos[TowelDispenser._END_IDX] = 1

    def matching_lengths(self, indices):
        matched = []
        pos = self.lookup
        for i, idx in enumerate(indices):
            pos = pos[idx]
            if len(pos) == 0:
                return matched
            elif pos[TowelDispenser._END_IDX] == 1:
                matched.append(i+1)
        return matched

    def translate_pattern(self, towelpattern):
        return [self.translate_color(c) for c in towelpattern]

def match_search(dispenser, idx_pattern):
    matched_lengths = dispenser.matching_lengths(idx_pattern)
    if len(matched_lengths) == 0:
        return False
    if matched_lengths[-1] == len(idx_pattern):
        return True
    for l in matched_lengths:
        if match_search(dispenser, idx_pattern[l:]):
            return True
    return False

def match_combo_search(dispenser, idx_pattern):
    possible_combos = [0]*len(idx_pattern)
    possible_combos.append(1)
    for i in range(len(idx_pattern)-1, -1, -1):
        matched = dispenser.matching_lengths(idx_pattern[i:])
        for m in matched:
            possible_combos[i] += possible_combos[i+m]
    return possible_combos[0]


def count_matching(patterns, dispenser):
    c = 0
    for pattern in patterns:
        idx_pattern = dispenser.translate_pattern(pattern)
        if match_search(dispenser, idx_pattern):
            c += 1
    return c

def count_combos(patterns, dispenser):
    c = 0
    for pattern in patterns:
        idx_pattern = dispenser.translate_pattern(pattern)
        combos = match_combo_search(dispenser, idx_pattern)
        c += combos
        #print("Towel", pattern, "has", combos, "possibilities")
    return c

def main(fname):
    available, desired = aoc_utils.parse_instructions(fname)
    dispenser = parse_designs(available[0])
    c = count_matching(desired, dispenser)
    print("possible", c)
    c = count_combos(desired, dispenser)
    print("combos", c)

main("in/in_19_test.txt")
main("in/in_19.txt")
