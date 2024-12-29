def parse_line(l):
    nums = l.split()
    return int(nums[0]), int(nums[1])


def parse_lines(text):
    left = []
    right = []
    for l in text.split("\n"):
        if l.strip() ==  "":
            continue
        a, b = parse_line(l)
        left.append(a)
        right.append(b)
    return left, right

def calc_sort_dists(left, right):
    left = sorted(left)
    right = sorted(right)
    distance = 0
    for l, r in zip(left, right):
        distance += abs(l-r)
    return distance

def similarity_score(left, right):
    r_lookup = {}
    for num in right:
        prev = r_lookup.get(num, 0)
        r_lookup[num] = prev + 1

    dist = 0
    for num in left:
        if num in r_lookup:
            dist += num * r_lookup[num]
    return dist


def main(text):
    l, r = parse_lines(text)
    #print(calc_sort_dists(l, r))
    print(similarity_score(l, r))

main(
"""
3   4
4   3
2   5
1   3
3   9
3   3
"""
)
