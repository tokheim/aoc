import aoc_utils

def parse_eq(tline):
    ans, num_string = tline.split(":")
    nums = num_string.strip().split()
    return int(ans), [int(n) for n in nums]

def parse_eqs(tlines):
    return [parse_eq(t) for t in tlines]

def concat(a, b):
    return int(str(a)+str(b))

def is_solvable(ans, nums, partial_res=0):
    if partial_res > ans:
        return False
    if len(nums) == 0:
        return partial_res == ans
    cur = nums[0]
    remainder = nums[1:]
    return is_solvable(ans, remainder, partial_res+cur) \
            or is_solvable(ans, remainder, partial_res*cur) \
            or (partial_res != 0 and is_solvable(ans, remainder, concat(partial_res,cur)))

def count_valid_eqs(eqs):
    n = 0
    for ans, nums in eqs:
        if is_solvable(ans, nums):
            n += ans
    return n

def main(fname):
    raw = aoc_utils.parse_block(fname)
    eqs = parse_eqs(raw)
    print(count_valid_eqs(eqs))

main("in/in_7_test.txt")
main("in/in_7.txt")


