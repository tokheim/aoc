def parse_stones(tline):
    stones = []
    for n in tline.split(" "):
        stones.append(int(n))
    return stones

def apply_rule(stone):
    if stone == 0:
        return [1]
    s_stone = str(stone)
    if len(s_stone) % 2 == 0:
        mid = len(s_stone) / 2
        return [int(s_stone[:mid]), int(s_stone[mid:])]
    return [stone*2024]

def blink(stones):
    new_stones = []
    for s in stones:
        new_stones.extend(apply_rule(s))
    return new_stones

def sim(stones, steps=25):
    for _ in range(steps):
        stones = blink(stones)
    return stones

def stone_simmer(stone, steps, sim_cache):
    if steps == 1:
        return [len(apply_rule(stone))]
    if stone in sim_cache:
        simmed_steps = sim_cache[stone]
        if len(simmed_steps) > steps:
            return simmed_steps[:steps]
    new_stones = apply_rule(stone)
    simmed_steps = [0] * steps
    simmed_steps[0] = len(new_stones)
    for s in new_stones:
        counts = stone_simmer(s, steps-1, sim_cache)
        for i, c in enumerate(counts):
            simmed_steps[i+1] += c
    sim_cache[stone] = simmed_steps
    return simmed_steps



def cached_sim(stones, steps):
    sim_cache = {}
    n = 0
    for i, stone in enumerate(stones):
        counts = stone_simmer(stone, steps, sim_cache)
        n += counts[-1]
    return n

def main(tline):
    stones = parse_stones(tline)
    n = cached_sim(stones, steps=25)
    #print(stones)
    print("sim25", n)
    n = cached_sim(stones, steps=75)
    print("sim75", n)

#main("125 17")
main("0 4 4979 24 4356119 914 85734 698829")
