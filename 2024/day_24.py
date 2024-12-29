import aoc_utils
import re
import random

_NUM_PATTERN = re.compile("([a-z])([0-9]+)")

class LogicGate(object):
    def __init__(self, left, right, op, name):
        self.left = left
        self.right = right
        self.op = op
        self.name = name

    def str_op(self):
        return self.op.name

    @property
    def value(self):
        return self.op.evaluate(self.left.value, self.right.value)

    def input_wires(self):
        vals = []
        if not isinstance(self.left, InputWire):
            vals.extend(self.left.input_wires())
        else:
            vals.append(self.left)
        if not isinstance(self.right, InputWire):
            vals.extend(self.right.input_wires())
        else:
            vals.append(self.right)
        return vals

    def child_gates(self):
        vals = []
        if not isinstance(self.left, InputWire):
            vals.append(self.left)
            vals.extend(self.left.child_gates())
        if not isinstance(self.right, InputWire):
            vals.append(self.right)
            vals.extend(self.right.child_gates())
        return vals

    def has_infinite_recursion(self, seen=None):
        if seen is None:
            seen = self.name
        elif self.name == seen:
            return True
        return self.left.has_infinite_recursion(seen) or self.right.has_infinite_recursion(seen)

    @property
    def head_val(self):
        m = _NUM_PATTERN.match(self.name)
        if m is None or m.groups()[0] != "z":
            return None
        return int(m.groups()[1])

    def __repr__(self):
        return "{}({}, {}, {})".format(self.str_op(), self.name, self.left, self.right)

    def __str__(self):
        return self.__repr__()

    def swap(self, other):
        o_l = other.left
        other.left = self.left
        o_r = other.right
        other.right = self.right
        self.left = o_l
        self.right = o_r
        o_op = other.op
        other.op = self.op
        self.op = o_op

class AndOp(object):
    def __init__(self):
        pass

    def evaluate(self, left, right):
        return left and right

    @property
    def name(self):
        return "AND"

class OrOp(object):
    def __init__(self):
        pass

    def evaluate(self, left, right):
        return left or right

    @property
    def name(self):
        return "OR"

class XorOp(object):
    def __init__(self):
        pass

    def evaluate(self, left, right):
        return left ^ right

    @property
    def name(self):
        return "XOR"

class InputWire(object):
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def reset(self):
        pass

    def __repr__(self):
        return "InputWire({})".format(self.name)

    def __str__(self):
        return self.__repr__()

    def copy(self, cache):
        if self.name in cache:
            return cache[self.name]
        w = InputWire(self.value, self.name)
        cache[w.name] = w
        return w

    def has_infinite_recursion(self, seen):
        return False

    @property
    def input_idx(self):
        m = _NUM_PATTERN.match(self.name)
        if m is not None and m.groups()[0] in ["x", "y"]:
            return int(m.groups()[1])
        return None

    @property
    def input_origin(self):
        m = _NUM_PATTERN.match(self.name)
        if m is not None:
            return m.groups()[0]
        return None

def parse_inputs(tlines):
    wires = []
    for tline in tlines:
        name, snum = tline.split(":")
        wires.append(InputWire(int(snum), name))
    return wires

def parse_raw_gates(tlines):
    gates = []
    for tline in tlines:
        split = tline.split(" ")
        gate = (split[0], split[1], split[2], split[4])
        gates.append(gate)
    return gates

def build_gate(left, op, right, name):
    f = None
    if op == "AND":
        f = AndOp()
    elif op == "OR":
        f = OrOp()
    elif op == "XOR":
        f = XorOp()
    else:
        raise AssertionError("unknown op"+str(op))
    return LogicGate(left, right, f, name)

def build_gates(text_gates, wires):
    out_map = dict((w.name, w) for w in wires)
    gates = []
    while len(text_gates) > 0:
        unmapped = []
        for l, op, r, name in text_gates:
            if l in out_map and r in out_map:
                g = build_gate(out_map[l], op, out_map[r], name)
                out_map[name] = g
                gates.append(g)
            else:
                unmapped.append((l, op, r, name))
        mapped = len(text_gates) - len(unmapped)
        if mapped == 0:
            raise AssertionError("Should have mapped something...")
        text_gates = unmapped
    return gates

class LogicSystem(object):
    def __init__(self, gates, wires):
        wires = sorted(wires, key=lambda x: x.input_idx)
        self.x_wires = [w for w in wires if w.input_origin == "x"]
        self.y_wires = [w for w in wires if w.input_origin == "y"]
        self.gates = gates
        self.heads = [t for t in gates if t.head_val is not None]
        self.heads = sorted(self.heads, key=lambda x: x.head_val)
        self.gate_map = dict((g.name, g) for g in gates)

        self._working_combos = []

    def evaluate_heads(self):
        return self._to_decimal([g.value for g in self.heads])

    def _to_decimal(self, arr_val):
        val = 0
        digit = 1
        for elem in arr_val:
            val += digit * elem
            digit = digit * 2
        return val

    def binary_evaluate(self):
        return [g.value for g in self.heads]

    def check_inputs(self):
        for i, head in enumerate(self.heads):
            self.check_inputs_at(i)

    def gate_input_map(self):
        vals = {}
        for g in self.gates:
            inputs = set([t.name for t in g.input_wires()])
            vals[g.name] = inputs
        return vals

    def wire_add(self):
        carry = 0
        sumval = []
        for i in range(len(self.x_wires)):
            v = self.x_wires[i].value ^ self.y_wires[i].value ^ carry
            sumval.append(v)
            if self.x_wires[i].value + self.y_wires[i].value + carry >= 2:
                carry = 1
            else:
                carry = 0
        sumval.append(carry)
        return sumval

    @property
    def wires(self):
        return self.x_wires + self.y_wires

    def _failure_indices(self):
        correct = self.wire_add()
        headvals = self.binary_evaluate()
        wrong = []
        for i, (c, h) in enumerate(zip(correct, headvals)):
            if c != h:
                wrong.append(i)
        return wrong

    def scenario_test(self, idx):
        for w in self.wires:
            w.value = 0
        self.x_wires[idx].value = 1
        wrong = set(self._failure_indices())
        self.y_wires[idx].value = 1
        self.x_wires[idx].value = 0
        wrong.update(self._failure_indices())
        self.y_wires[idx].value = 0
        self.y_wires[idx-1].value = 1
        self.x_wires[idx-1].value = 1
        wrong.update(self._failure_indices())
        self.x_wires[idx-1].value = 0
        for w in self.y_wires[:idx-1]:
            w.value = 1
        self.x_wires[0].value = 1
        wrong.update(self._failure_indices())
        for w in self.x_wires[:idx-1]:
            w.value = 1
        wrong.update(self._failure_indices())
        for w in self.y_wires[1:idx]:
            w.value = 0
        wrong.update(self._failure_indices())
        return wrong

    def lsb_fix(self):
        safe = set()
        swaps = set()
        for i in range(len(self.heads)-1):
            if i > 0:
                swaps = self._try_fix(i, swaps, safe)
            print("solution up to {} swaps {}".format(i, swaps))
            safe.add(self.heads[i].name)
            safe.update([t.name for t in self.heads[i].child_gates()])
        return swaps

    def _try_fix(self, idx, swaps, safe, depth=1):
        wrong_idxs = self.scenario_test(idx)
        if len(wrong_idxs) == 0:
            return swaps
        if depth <= 0 or len(swaps) == 8:
            raise AssertionError("could not fix")
        if min(wrong_idxs) < idx:
            raise AssertionError("broke lower order at: "+str(idx)+" - "+str(wrong_idxs))
        suspicious_set = set()
        for wi in wrong_idxs:
            suspicious_set.add(self.heads[wi].name)
            suspicious_set.update([g.name for g in self.heads[wi].child_gates()])
        suspicious_set = suspicious_set - safe
        suspicious = list(suspicious_set)
        next_swaps = set(swaps)

        for i in range(len(suspicious)):
            a = suspicious[i]
            if a in swaps:
                continue
            next_swaps.add(a)
            for j in range(i+1, len(suspicious)):
                b = suspicious[j]
                if b in next_swaps:
                    continue
                self.gate_map[a].swap(self.gate_map[b])
                if self.gate_map[a].has_infinite_recursion() or self.gate_map[b].has_infinite_recursion():
                    self.gate_map[a].swap(self.gate_map[b])
                    continue
                next_swaps.add(b)
                try:
                    return self._try_fix(max(wrong_idxs), next_swaps, safe, depth=depth-1)
                except AssertionError:
                    pass
                next_swaps.remove(b)
                self.gate_map[a].swap(self.gate_map[b])
            next_swaps.remove(a)
        raise AssertionError("could not fix!")




def main(fname):
    raw_inputs, raw_gates = aoc_utils.parse_instructions(fname)
    wires = parse_inputs(raw_inputs)
    struct_gates = parse_raw_gates(raw_gates)
    gates = build_gates(struct_gates, wires)

    system = LogicSystem(gates, wires)
    print(system.evaluate_heads())

    swaps = system.lsb_fix()
    print(",".join(sorted(list(swaps))))


#main("in/in_24_test.txt")
main("in/in_24.txt")
