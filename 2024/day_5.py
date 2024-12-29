import aoc_utils

def build_rule_lookup(lookup_lines):
    rules = {}
    for line in lookup_lines:
        a, b = line.split("|")
        if a not in rules:
            rules[a] = []
        rules[a].append(b)
    return rules

def is_legal(page_update, rules):
    seen = set()
    for page in page_update:
        checks = rules.get(page, [])
        for check in checks:
            if check in seen:
                return False
        seen.add(page)
    return True

def middle_page(page_update):
    return page_update[len(page_update)/2]

def check_updates(page_updates, rules):
    n = 0
    for raw_updt in page_updates:
        page_update = raw_updt.split(",")
        if is_legal(page_update, rules):
            n += int(middle_page(page_update))
    return n

def applicable_rules(page_update, rules):
    elems = set(page_update)
    applicable = {}
    for k, vals in rules.items():
        if k not in elems:
            continue
        needed = set()
        for v in vals:
            if v in elems:
                needed.add(v)
        if needed:
            applicable[k] = needed
    return applicable

def strip_rules(rules, items):
    for val_set in rules.values():
        for item in items:
            val_set.remove(item)
    return dict((k, v) for k, v in rules.items() if v)

def fix_update(page_update, all_rules):
    elems = set(page_update)
    rules = applicable_rules(page_update, all_rules)
    rev_corrected = []
    while elems:
        insertables = elems - set(rules.keys())
        for ins in insertables:
            rev_corrected.append(ins)
            elems.remove(ins)
        rules = strip_rules(rules, insertables)
    return list(reversed(rev_corrected))


def fixed_updates(page_updates, rules):
    n = 0
    for raw_updt in page_updates:
        page_update = raw_updt.split(",")
        if not is_legal(page_update, rules):
            fixed = fix_update(page_update, rules)
            #print(page_update, "-----", fixed)
            n += int(middle_page(fixed))
    return n

def main(fname):
    rules, page_updates = aoc_utils.parse_instructions(fname)
    rlookup = build_rule_lookup(rules)
    print(check_updates(page_updates, rlookup))
    print(fixed_updates(page_updates, rlookup))

main("in/in_5_test.txt")
main("in/in_5.txt")
