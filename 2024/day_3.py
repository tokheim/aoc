import re

mul_check = re.compile("mul\\(([0-9]+),([0-9]+)\\)")

def parse_text(text):
    pairs = mul_check.findall(text)
    valid_pairs = []
    for a, b in pairs:
        if len(a) <= 3 and len(b) <= 3:
            valid_pairs.append((int(a), int(b)))
    return valid_pairs

def parse_instructions(text):
    check = re.compile("(mul\\(([0-9]+),([0-9]+)\\)|do\\(\\)|don't\\(\\))")
    mul_active = True
    valid_pairs = []
    for match in check.findall(text):
        if match[0] == "do()":
            mul_active = True
            continue
        elif match[0] == "don't()":
            mul_active = False
            continue
        elif not mul_active:
            continue
        a, b = match[1], match[2]
        if len(a) <= 3 and len(b) <=3:
            valid_pairs.append((int(a), int(b)))
    return valid_pairs

def calc_mult(pairs):
    n = 0
    for a, b in pairs:
        n += a * b
    return n


def main(text):
    pairs = parse_instructions(text)
    print(calc_mult(pairs))

main("""
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""")

main("""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""")
