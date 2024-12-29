def parse_file(fname):
    with open(fname, "r") as f:
        return [l.rstrip() for l in f.readlines() if l.strip()]

def match_word(grid, word):
    height = len(grid)
    width = len(grid[0])
    matches = 0
    for x in range(width):
        for y in range(height):
            matches += match_word_at(grid, word, x, y)
    return matches

def cross_match(grid):
    matches = 0
    height = len(grid)
    width = len(grid[0])
    for x in range(1, width-1):
        for y in range(1, height-1):
            if has_cross_match(grid, x, y):
                matches += 1
    return matches

def has_cross_match(grid, x, y):
    found = 0
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if dir_cross_match(grid, x, y, dx, dy):
                found += 1
            if found >= 2:
                return True
    return False

def dir_cross_match(grid, x, y, dx, dy):
    s_x = x - dx
    s_y = y - dy
    return matches_dir(grid, "MAS", s_x, s_y, dx, dy)


def match_word_at(grid, word, x, y):
    if grid[y][x] != word[0]:
        return 0
    matches = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and matches_dir(grid, word, x, y, dx, dy):
                matches += 1
    return matches

def matches_dir(grid, word, s_x, s_y, dx, dy):
    end_y = s_y+(dy*(len(word)-1))
    end_x = s_x+(dx*(len(word)-1))
    if end_y >= len(grid) or end_y < 0:
        return False
    if end_x >= len(grid[0]) or end_x < 0:
        return False
    x = s_x
    y = s_y
    for i, c in enumerate(word):
        if grid[y][x] != c:
            return False
        x += dx
        y += dy
    return True

def main(fname):
    grid = parse_file(fname)
    print(match_word(grid, "XMAS"))
    print(cross_match(grid))

main("in_4.txt")
