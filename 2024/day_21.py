import aoc_utils
import numpy as np

class RobotAction(object):
    def __init__(self, char):
        self.char = char

    @property
    def direction(self):
        if self.char == "<":
            return aoc_utils.Coord(-1, 0)
        if self.char == ">":
            return aoc_utils.Coord(1, 0)
        if self.char == "^":
            return aoc_utils.Coord(0, 1)
        if self.char == "v":
            return aoc_utils.Coord(0, -1)
        return aoc_utils.Coord(0, 0)

    @property
    def is_advance(self):
        return self.char == "A"

    @staticmethod
    def as_action(direction):
        if direction.x > 0:
            return RobotAction(">")
        elif direction.x < 0:
            return RobotAction("<")
        elif direction.y > 0:
            return RobotAction("^")
        return RobotAction("v")

    @staticmethod
    def path_to_actions(path):
        actions = []
        for p_elem in path:
            action = RobotAction.as_action(p_elem)
            actions = actions + ([action]*p_elem.manhatten_dist())
        actions.append(RobotAction("A"))
        return actions

    def __repr__(self):
        return "RobotAction("+self.char+")"



class Keypad(object):
    def __init__(self, key_grid, layout, pos):
        self.key_grid = key_grid
        self.layout = layout
        self.pos = pos
        self.output = []

    def apply(self, action):
        if action.is_advance:
            return self._push()
        else:
            self.pos = self.pos.add(action.direction)
            return None

    def _push(self):
        output = None
        for k, pos in self.key_grid.items():
            if pos == self.pos:
                self.output.append(k)
                output = k
        return output


    def reset(self):
        self.pos = self.key_grid["A"]
        self.output = []

    def paths_to(self, key, from_pos = None, minimize=True):
        if from_pos is None:
            from_pos = self.pos
        key_pos = self.key_grid[key]
        paths = self._calc_paths(key_pos, from_pos)
        if minimize:
            min_path = min(paths, key=lambda x: len(x))
            return [p for p in paths if len(p) == len(min_path)]
        return paths

    def actions_for_text(self, text, from_pos = None):
        cur_pos = from_pos
        if from_pos is None:
            cur_pos = self.pos
        actions = [[]]
        for c in text:
            paths = self.paths_to(c, from_pos=cur_pos)
            cur_pos = self.key_grid[c]
            new_actions = [RobotAction.path_to_actions(p) for p in paths]

            actions = self._amend_actions(actions, new_actions)
        return actions

    def _amend_actions(self, old_actions, new_actions):
        out_actions = []
        for oa in old_actions:
            for na in new_actions:
                out_actions.append(oa + na)
        return out_actions

    def _calc_paths(self, to_pos, from_pos):
        delta = to_pos.subtract(from_pos)
        paths = []
        if delta.xdir() != 0:
            walked = self._safe_walk(to_pos, from_pos, aoc_utils.Coord(delta.xdir(), 0))
            if walked.add(from_pos) == to_pos:
                return [[walked]]
            elif walked.manhatten_dist() != 0:
                for p in self._calc_paths(to_pos, walked.add(from_pos)):
                    paths.append([walked] + p)
        if delta.ydir() != 0:
            walked = self._safe_walk(to_pos, from_pos, aoc_utils.Coord(0, delta.ydir()))
            if walked.add(from_pos) == to_pos:
                return [[walked]]
            elif walked.manhatten_dist() != 0:
                for p in self._calc_paths(to_pos, walked.add(from_pos)):
                    paths.append([walked] + p)
        if len(paths) == 0:
            paths.append([])
        return paths

    def _safe_walk(self, to_pos, from_pos, direction):
        pos = from_pos
        n = 0
        while self.layout[pos.y+direction.y, pos.x+direction.x]:
            pos = pos.add(direction)
            n += 1
            if direction.x != 0 and pos.x == to_pos.x:
                break
            elif direction.y != 0 and pos.y == to_pos.y:
                break
        return aoc_utils.Coord(direction.x * n, direction.y * n)

    @staticmethod
    def build_from(textgrid, startchar):
        h = len(textgrid)
        w = len(textgrid[0])
        layout = np.ones((h, w), dtype=bool)
        key_grid = {}
        start_pos = None
        for y, line in enumerate(reversed(textgrid)):
            for x, c in enumerate(line):
                pos = aoc_utils.Coord(x, y)
                key_grid[c] = pos
                if c == startchar:
                    start_pos = pos
                if c == " ":
                    layout[y, x] = False
        return Keypad(key_grid, layout, start_pos)



    @staticmethod
    def number_keypad():
        text = ["789", "456", "123", " 0A"]
        return Keypad.build_from(text, "A")

    @staticmethod
    def arrow_keypad():
        text = [" ^A", "<v>"]
        return Keypad.build_from(text, "A")

class KeypadChainer(object):
    def __init__(self, keypads):
        self.keypads = keypads

    def _translate_to_arrows(self, path):
        terms = []
        for direction in path:
            if direction.xdir() > 0:
                terms.append(">")
            elif direction.xdir() < 0:
                terms.append("<")
            elif direction.ydir() > 0:
                terms.append("^")
            elif direction.ydir() < 0:
                terms.append("v")
            terms.extend(["A"]*direction.manhatten_dist())
        return terms

    def apply_to_chain(self, text_actions):
        actions = [RobotAction(t) for t in text_actions]
        for action in actions:
            self._apply_at_level(action, 0)

    def _apply_at_level(self, action, level):
        output = self.keypads[level].apply(action)
        if output is not None and level < len(self.keypads) - 1:
            next_action = RobotAction(output)
            self._apply_at_level(next_action, level + 1)

    @property
    def deepest_level(self):
        return len(self.keypads) - 1

    def actions_to_output(self, text, minimize=True):
        cur_texts = [text]
        for keypad in reversed(self.keypads):
            actions_opts = self._action_opts_for_kp(cur_texts, keypad)
            cur_texts = []
            minlen = min(len(a) for a in actions_opts)
            for actions in actions_opts:
                text = "".join([a.char for a in actions])
                if len(text) == minlen and minimize:
                    cur_texts.append(text)
        return sorted(cur_texts, key=lambda x: len(x))

    def _action_opts_for_kp(self, texts, keypad):
        new_actions = []
        for text in texts:
            new_actions.extend(keypad.actions_for_text(text))
        return new_actions

    def min_complexity_to_output_at_level(self, in_text, from_level, level_char_cache):
        if from_level < 0:
            return len(in_text)
        key = (in_text, from_level)
        if key in level_char_cache:
            return level_char_cache[key]
        action_opts = self.keypads[from_level].actions_for_text(in_text)
        min_complex = float("inf")
        for action_opt in action_opts:
            cur_complex = 0
            texts = ("".join([a.char for a in action_opt])).split("A")
            for text in texts[:-1]:
                text = text + "A"
                cur_complex += self.min_complexity_to_output_at_level(text, from_level-1, level_char_cache)
            min_complex = min(min_complex, cur_complex)
        level_char_cache[key] = min_complex
        return min_complex


    def min_complexity_to_output(self, text):
        level_char_cache = {}
        return self.min_complexity_to_output_at_level(text, self.deepest_level, level_char_cache)

    @property
    def chain_output(self):
        return "".join(self.keypads[-1].output)

    def reset(self):
        for k in self.keypads:
            k.reset()

    @staticmethod
    def build(num_directional = 2):
        chain = []
        for _ in range(num_directional):
            chain.append(Keypad.arrow_keypad())
        chain.append(Keypad.number_keypad())
        return KeypadChainer(chain)

def calc_complexity(codes, chain):
    complexity = 0
    for code in codes:
        #texts = chain.actions_to_output(code)
        numval = int(code.replace("A", ""))
        #shortest = texts[0]
        #num_short = len([t for t in texts if len(t) == len(shortest)])
        min_complex = chain.min_complexity_to_output(code)
        print("{} alt: {}".format(code, min_complex))
        complexity += min_complex * numval
    return complexity


def main(fname):
    codes = aoc_utils.parse_block(fname)
    chain = KeypadChainer.build()
    complexity = calc_complexity(codes, chain)
    print("complexity", complexity)

    chain = KeypadChainer.build(25)
    complexity = calc_complexity(codes, chain)
    print("complexity", complexity)

main("in/in_21_test.txt")
main("in/in_21.txt")
