import aoc_utils
import math

class Register(object):
    def __init__(self):
        self._vals = [0]*3

    def get(self, idx):
        return self._vals[idx]

    def set(self, idx, val):
        self._vals[idx] = val

    def reset(self, a_val):
        self._vals = [0]*3
        self._vals[0] = a_val

class Instruction(object):
    @property
    def opcode(self):
        return self._OPCODE

    def __init__(self, register):
        self.register = register

    def perform(self, operand):
        raise NotImplementedError()

    def _combo_operand(self, operand):
        if operand >= 4 and operand < 7:
            return self.register.get(operand-4)
        return operand

class Program(object):
    def __init__(self, code, opmapper, pointer=0):
        self.code = code
        self.pointer = pointer
        self.opmapper = opmapper

    def reset(self):
        self.pointer = 0

    @property
    def has_halted(self):
        return self.pointer >= len(self.code) - 1

    def tick(self):
        opcode = self.code[self.pointer]
        operand = self.code[self.pointer+1]
        jump = self.opmapper.instruction(opcode).perform(operand)
        if jump > 0:
            self.pointer += jump
        else:
            self.pointer = -jump

    def run_to_end(self):
        while not self.has_halted:
            self.tick()

class XdvInstruction(Instruction):
    def __init__(self, register, opcode, store_idx):
        Instruction.__init__(self, register)
        self._opcode = opcode
        self.store_idx = store_idx

    @property
    def opcode(self):
        return self._opcode

    def perform(self, operand):
        numerator = self.register.get(0)
        literal_operand = self._combo_operand(operand)
        denominator = math.pow(2, literal_operand)
        self.register.set(self.store_idx, int(numerator / denominator))
        return 2

class BxlInstruction(Instruction):
    _OPCODE = 1
    def __init__(self, register):
        Instruction.__init__(self, register)

    def perform(self, operand):
        other = self.register.get(1)
        newval = (operand ^ other)
        self.register.set(1, newval)
        return 2

class BstInstruction(Instruction):
    _OPCODE = 2
    def __init__(self, register):
        Instruction.__init__(self, register)

    def perform(self, operand):
        opval = self._combo_operand(operand)
        val = opval % 8
        self.register.set(1, val)
        return 2

class JnzInstruction(Instruction):
    _OPCODE = 3
    def __init__(self, register):
        Instruction.__init__(self, register)

    def perform(self, operand):
        if self.register.get(0) == 0:
            return 2
        return -operand

class BxcInstruction(Instruction):
    _OPCODE = 4
    def __init__(self, register):
        Instruction.__init__(self, register)

    def perform(self, operand):
        bval = self.register.get(1)
        cval = self.register.get(2)
        self.register.set(1, bval^cval)
        return 2

class OutInstruction(Instruction):
    _OPCODE = 5
    def __init__(self, register):
        Instruction.__init__(self, register)
        self.stdout_buffer = []

    def perform(self, operand):
        opval = self._combo_operand(operand)
        self.stdout_buffer.append(opval % 8)
        return 2

    def print_buffer(self):
        strvals = [str(i) for i in self.stdout_buffer]
        return ",".join(strvals)

    def reset(self):
        self.stdout_buffer = []

class OpMapper(object):
    def __init__(self, instructions):
        self._map = {}
        for i in instructions:
            self._map[i.opcode] = i

    def instruction(self, opcode):
        return self._map[opcode]

    @staticmethod
    def build(register):
        adv = XdvInstruction(register, 0, 0)
        bxl = BxlInstruction(register)
        bst = BstInstruction(register)
        jnz = JnzInstruction(register)
        bxc = BxcInstruction(register)
        out = OutInstruction(register)
        bdv = XdvInstruction(register, 6, 1)
        cdv = XdvInstruction(register, 7, 2)
        return OpMapper([adv, bxl, bst, jnz, bxc, out, bdv, cdv])

class SmartSeeker(object):
    def __init__(self, out_seeker, desired_out):
        self.out_seeker = out_seeker
        self.desired_out = desired_out

    def seek(self):
        seek_to = int(math.pow(8, 16))
        n = 0
        for i in range(len(self.desired_out)):
            n = n*8
            check_from = len(self.desired_out) - 1 -i
            n = self.out_seeker.seek(self.desired_out[check_from:], n, seek_to)
        print("Desired out: ", self.desired_out)
        print("Found complete number with "+str(n))



class OutputSeeker(object):
    def __init__(self, program, stdout, register):
        self.program = program
        self.stdout = stdout
        self.register = register

    def reset_experiment(self, n):
        self.program.reset()
        self.stdout.reset()
        self.register.reset(n)

    def seek(self, desired_out, seek_from, seek_to):
        n = seek_from
        while n <= seek_to:
            self.reset_experiment(n)
            res = self.run_for_match(desired_out)
            if res:
                print("found match", str(n), " out: ", self.stdout.print_buffer())
                return n
            n += 1
        raise AssertionError("could not find valid register val")

    def run_for_match(self, desired_out):
        i = 0
        while not self.program.has_halted:
            self.program.tick()
            if len(self.stdout.stdout_buffer) > i:
                if i >= len(desired_out):
                    return False
                if self.stdout.stdout_buffer[i] != desired_out[i]:
                    return False
                i += 1
        return i == len(desired_out)

def parse_vals(tline):
    vals = tline.split(":")[1].split(",")
    return [int(v) for v in vals]

def gen_register(tlines):
    register = Register()
    for i, tline in enumerate(tlines):
        register.set(i, parse_vals(tline)[0])
    return register

def main(fname):
    reg_vals, raw_code = aoc_utils.parse_instructions(fname)
    register = gen_register(reg_vals)
    opmapper = OpMapper.build(register)
    stdout = opmapper.instruction(OutInstruction._OPCODE)

    parsed_code = parse_vals(raw_code[0])
    program = Program(parsed_code, opmapper)
    program.run_to_end()

    print(stdout.print_buffer(), "len: ", len(stdout.stdout_buffer), len(parsed_code))

    out_seek = OutputSeeker(program, stdout, register)
    smart_seeker = SmartSeeker(out_seek, parsed_code)
    n = smart_seeker.seek()

main("in/in_17_test.txt")
main("in/in_17.txt")
