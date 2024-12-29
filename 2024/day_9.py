import aoc_utils

def num_parse(line):
    return [int(c) for c in line]

def free_space_idxs(mem_line):
    cur_idx = 0
    for i, size in enumerate(mem_line):
        if i % 2 == 0:
            cur_idx += size
            continue
        for n in range(size):
            yield n+cur_idx
        cur_idx += size

def gen_blocks(mem_line):
    blocks = []
    fnum = 0
    cur_idx = 0
    for i, size in enumerate(mem_line):
        if i % 2 == 0:
            b = Block(cur_idx, cur_idx+size, fnum)
            blocks.append(b)
            fnum += 1
        else:
            b = Block(cur_idx, cur_idx+size)
            blocks.append(b)
        cur_idx += size
    return blocks

def clean_blocks(blocks):
    nonzero = [b for b in blocks if b.size != 0]
    merged = [nonzero[0]]
    for b in nonzero[1:]:
        if b.fnum == merged[-1].fnum:
            merged[-1].e_idx += b.size
        else:
            merged.append(b)
    return merged


def total_size(mem_line):
    return sum(mem_line)

def rev_filenum_idx_it(mem_line):
    filenum = int((len(mem_line)-1)/2)
    idx = total_size(mem_line) - 1
    is_file = len(mem_line) % 2 == 1
    for size in reversed(mem_line):
        if not is_file:
            idx -= size
        else:
            for n in range(size):
                yield filenum, idx-n
            filenum -= 1
            idx -= size
        is_file = not is_file

def fragment_mem(mem_line):
    free_idxs = list(free_space_idxs(mem_line))
    f_idxs = list(rev_filenum_idx_it(mem_line))
    free_idxs += [-1] * len(f_idxs)
    #print(f_idxs)
    mem = [0]*total_size(mem_line)
    for free_idx, (fnum, fidx) in zip(free_idxs, f_idxs):
        if free_idx < fidx and free_idx >= 0:
            mem[free_idx] = fnum
        else:
            mem[fidx] = fnum
    return mem

def fs_checksum(mem):
    n = 0
    for i, fnum in enumerate(mem):
        n += i*fnum
    return n

def first_of_size(blocks, size):
    for b in blocks:
        if b.size >= size:
            return b
    return None

def paint(mem, file_num, s_idx, size):
    for i in range(size):
        mem[s_idx+i] = file_num

def fragment_full(blocks):
    mem = [0] * sum(b.size for b in blocks)
    free_blocks = [b for b in blocks if b.free]
    file_blocks = [b for b in blocks if not b.free]
    for file_block in reversed(file_blocks):
        free_space = first_of_size(free_blocks, file_block.size)
        if free_space is None or free_space.s_idx > file_block.s_idx:
            paint(mem, file_block.fnum, file_block.s_idx, file_block.size)
        else:
            paint(mem, file_block.fnum, free_space.s_idx, file_block.size)
            free_space.s_idx += file_block.size
    return mem

def fragment_partial(blocks):
    mem = [0] * sum(b.size for b in blocks)
    free_blocks = list(reversed([b for b in blocks if b.free]))
    file_blocks = list(reversed([b for b in blocks if not b.free]))
    for file_block in file_blocks:
        while free_blocks and file_block.size > 0:
            cur_free = free_blocks[-1]
            if cur_free.s_idx > file_block.s_idx:
                break
            free_painted = min(cur_free.size, file_block.size)
            paint(mem, file_block.fnum, cur_free.s_idx, free_painted)
            cur_free.s_idx += free_painted
            if cur_free.size == 0:
                free_blocks.pop()
            file_block.e_idx -= free_painted
        paint(mem, file_block.fnum, file_block.s_idx, file_block.size)
    return mem


class Block(object):
    def __init__(self, s_idx, e_idx, fnum=-1):
        self.s_idx = s_idx
        self.e_idx = e_idx
        self.fnum = fnum

    @property
    def size(self):
        return self.e_idx - self.s_idx

    @property
    def free(self):
        return self.fnum == -1

def main(fname):
    mem_line = num_parse(aoc_utils.parse_block(fname)[0])
    mem = fragment_mem(mem_line)
    #print(mem)
    print(fs_checksum(mem))

    blocks = gen_blocks(mem_line)
    blocks = clean_blocks(blocks)
    mem = fragment_partial(blocks)
    print(fs_checksum(mem))

    blocks = gen_blocks(mem_line)
    blocks = clean_blocks(blocks)
    mem = fragment_full(blocks)
    #print(mem)
    print(fs_checksum(mem))

main("in/in_9_test.txt")
main("in/in_9.txt")
