import aoc_utils

def find_player(tlines):
    for y, tline in enumerate(tlines):
        try:
            return y, tline.index("^")
        except ValueError:
            pass
    raise ValueError("player not found")

def walk_grid(tlines):
    width = len(tlines[0])
    mat = []
    for _ in tlines:
        mat.append([0]*width)
    return mat

def count_visits(mat):
    return sum(sum(t) for t in mat)

class Board(object):
    def __init__(self, tlines):
        self.tlines = tlines
        self.grid = walk_grid(tlines)
        y, x = find_player(tlines)
        self.y = y
        self.x = x
        self.dy = -1
        self.dx = 0
        self.dir_grid = walk_grid(tlines)

    @property
    def width(self):
        return len(self.tlines[0])

    @property
    def height(self):
        return len(self.tlines)

    @property
    def visits(self):
        return sum(sum(t) for t in self.grid)

    def will_exit_area(self):
        return not self.within_bounds(self.y+self.dy, self.x+self.dx)

    def within_bounds(self, y, x):
        return y >= 0 and y < self.height and x >= 0 and x < self.width

    def move(self):
        self.y += self.dy
        self.x += self.dx

    def has_obstacle(self, y, x):
        return self.tlines[y][x] == "#"

    def can_move(self):
        return not self.has_obstacle(self.y+self.dy, self.x+self.dx)

    def turn_dir(self):
        if self.dy != 0:
            return 0, -self.dy
        else:
            return self.dx, 0

    def turn(self):
        self.dy, self.dx = self.turn_dir()

    def simulate(self):
        self.grid[self.y][self.x] = 1
        while not self.will_exit_area():
            if self.can_move():
                self.move()
                self.grid[self.y][self.x] = 1
            else:
                self.turn()

    def loop_simulation(self):
        s_y = self.y
        s_x = self.x
        found_coords = set()
        grid_idx = 1
        while not self.will_exit_area():
            grid_idx += 1
            self.grid[self.y][self.x] = 1
            if not self.can_move():
                self.turn()
                continue
            elif self.run_loop_sim(grid_idx):
                found_coords.add((self.y+self.dy, self.x+self.dx))
            self.move()
        #found_coords.remove((s_y, s_x))
        return len(found_coords)

    def run_loop_sim(self, grid_idx):
        x = self.x
        y = self.y
        dy = self.dy
        dx = self.dx

        t_x = x + dx
        t_y = y + dy
        if self.grid[t_y][t_x] == 1:
            return False
        self.tlines[t_y][t_x] = "#"

        looped = self.check_loop(grid_idx)

        self.tlines[t_y][t_x] = "."
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        return looped

    def check_loop(self, grid_idx):
        while not self.will_exit_area():
            if self.dy == 1 and self.dir_grid[self.y][self.x] == grid_idx:
                return True
            elif self.dy == 1:
                self.dir_grid[self.y][self.x] = grid_idx

            if self.can_move():
                self.move()
            else:
                self.turn()
        return False


def main(fname):
    tlines = aoc_utils.parse_block(fname)
    tlines = [[c for c in t] for t in tlines]
    board = Board(tlines)
    #board.simulate()
    print(board.loop_simulation())
    #print(board.visits)

main("in/in_6_test.txt")
main("in/in_6.txt")
