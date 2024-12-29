import aoc_utils
import numpy as np

class MonkeyPricer(object):
    def __init__(self, secret):
        self.secret = secret
        self.seed = secret

    def generate(self):
        self.secret = self.mixprune(64*self.secret)
        self.secret = self.mixprune(int(self.secret/32))
        self.secret = self.mixprune(2048*self.secret)
        return self.secret

    @property
    def val(self):
        return self.secret % 10

    def mixprune(self, val):
        return (self.secret ^ val) % 16777216

    def change_sequence(self, n):
        last_num = self.val
        changes = []
        for _ in range(n):
            self.generate()
            changes.append((self.val - last_num, self.val))
            last_num = self.val
        return changes

class ChangePriceAccumulator(object):
    def __init__(self, n_changes):
        self.n_changes = n_changes
        self.mat = np.zeros([20]*n_changes, dtype=int)

    def build_for(self, pricers, max_num):
        for p in pricers:
            seq = p.change_sequence(max_num)
            self._add_to_mat(seq)

    def _as_idx(self, sequence):
        return tuple([t + 10 for t in sequence])

    def _add_to_mat(self, sequence):
        seen_mat = np.zeros(self.mat.shape, dtype=bool)
        for i in range(len(sequence) + 1 - self.n_changes):
            v = sequence[i+self.n_changes-1][1]
            seq = self._as_idx([sequence[i+t][0] for t in range(self.n_changes)])
            if not seen_mat[seq]:
                seen_mat[seq] = True
                self.mat[seq] += v

    def price_for_seq(self, sequence):
        idx = self._as_idx(sequence)
        return self.mat[idx]


    @property
    def best_price(self):
        return np.max(self.mat)

    def _as_seq(self, idx):
        return [t - 10 for t in idx]

    @property
    def best_seq(self):
        n = self.mat.argmax()
        idx = np.unravel_index(n, self.mat.shape)
        return self._as_seq(idx)



def sum_secrets_at(pricers, num):
    n = 0
    for pricer in pricers:
        for _ in range(num):
            pricer.generate()
        n += pricer.secret
        pricer.secret = pricer.seed
    return n

def parse_pricers(tlines):
    pricers = []
    for tline in tlines:
        p = MonkeyPricer(int(tline))
        pricers.append(p)
    return pricers

def main(fname):
    tlines = aoc_utils.parse_block(fname)
    pricers = parse_pricers(tlines)
    n = sum_secrets_at(pricers, 2000)
    print("first n sum", n)

    cpa = ChangePriceAccumulator(4)
    cpa.build_for(pricers, 2000)
    print("Most bananas ", cpa.best_price, " sequence ", cpa.best_seq)
    p = cpa.price_for_seq([-2, 1, -1, 3])
    print("seq price", p)

main("in/in_22_test.txt")
main("in/in_22.txt")
