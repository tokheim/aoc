def parse_reports(text):
    reports = []
    for l in text.split("\n"):
        if l.strip() == "":
            continue
        nums = [int(t) for t in l.split()]
        reports.append(nums)
    return reports

def is_safe(report):
    all_up = True
    all_down = True
    for ra, rb in zip(report[:-1], report[1:]):
        if rb > ra:
            all_down = False
        else:
            all_up = False
        dist = abs(rb-ra)
        if dist < 1 or dist > 3:
            return False
    return all_up or all_down

def general_direction_up(report):
    num_ups = 0
    num_downs = 0
    for ra, rb in zip(report[:-1], report[1:]):
        if rb > ra:
            num_ups += 1
        else:
            num_downs += 1
    return num_ups > num_downs

def safe_check(a, b, is_up):
    dist = abs(b-a)
    return ((b > a) == is_up) and dist >= 1 and dist <= 3

def is_safe_dampened(report):
    is_up = general_direction_up(report)
    for i, n in enumerate(report):
        if i == 0:
            continue
        if safe_check(report[i-1], n, is_up):
            continue
        without_cur = report[:i] + report[i+1:]
        without_prev = report[:i-1] + report[i:]
        return is_safe(without_cur) or is_safe(without_prev)
    return True

def num_safe(reports):
    n = 0
    for report in reports:
        if is_safe_dampened(report):
            n += 1
    return n

def main(text):
    reports = parse_reports(text)
    print(num_safe(reports))

main("""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""")

