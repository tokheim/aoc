import aoc_utils
import numpy as np

def parse_connections(tlines):
    pairs = []
    for tline in tlines:
        pairs.append(tline.split("-"))
    return pairs

class ConnectionMap(object):
    def __init__(self, mat, names):
        self.mat = mat
        self.names = names

    def find_clusters(self, desired_length = 3):
        found = []
        for idx in range(len(self.names)):
            arr = np.array(self.mat[idx])
            arr[:idx+1] = False
            found.extend(self._find_for(arr, [idx], desired_length))
        return self._translate_cluster_names(found)

    def _find_for(self, arr, prev, desired_length):
        if len(prev) >= desired_length:
            return [tuple(prev)]
        found = []
        carr = np.array(arr)
        for idx in np.where(arr)[0]:
            carr[idx] = False
            new_arr = self.mat[idx, :] * carr
            found.extend(self._find_for(new_arr, prev + [idx], desired_length))
        return found

    def largest_cluster(self):
        largest = tuple()
        for idx in range(len(self.names)):
            arr = np.array(self.mat[idx])
            arr[:idx+1] = False
            alt = self._find_largest(arr, [idx])
            if len(alt) > len(largest):
                largest = alt
        return self._translate_cluster_names([largest])[0]

    def _find_largest(self, arr, prev):
        largest = prev
        carr = np.array(arr)
        for idx in np.where(arr)[0]:
            carr[idx] = False
            new_arr = self.mat[idx, :] * carr
            alt = self._find_largest(new_arr, prev + [idx])
            if len(alt) > len(largest):
                largest = alt
        return largest


    def _translate_cluster_names(self, clusters):
        translated = []
        for cluster in clusters:
            names = [self.names[idx] for idx in cluster]
            translated.append(names)
        return translated

    @staticmethod
    def build(pairs):
        idx_map, names = ConnectionMap._elem_map(pairs)
        mat = ConnectionMap._pair_mat(pairs, idx_map)
        return ConnectionMap(mat, names)


    @staticmethod
    def _pair_mat(pairs, idx_map):
        mat = np.zeros((len(idx_map), len(idx_map)), dtype=bool)
        for a, b in pairs:
            ia = idx_map[a]
            ib = idx_map[b]
            mat[ia, ib] = True
            mat[ib, ia] = True
        for i in range(len(idx_map)):
            mat[i, i] = True
        return mat


    @staticmethod
    def _elem_map(pairs):
        elems = {}
        i = 0
        all_elems = [p[0] for p in pairs] + [p[1] for p in pairs]
        names = []
        for name in all_elems:
            if name not in elems:
                elems[name] = i
                i += 1
                names.append(name)
        return elems, names

def clusters_with_char(clusters, char):
    found = []
    for cluster in clusters:
        for n in cluster:
            if n.startswith(char):
                found.append(cluster)
                break
    return found

def main(fname):
    tlines = aoc_utils.parse_block(fname)
    pairs = parse_connections(tlines)
    cmap = ConnectionMap.build(pairs)
    clusters = cmap.find_clusters()
    interesting = clusters_with_char(clusters, "t")
    print("total", len(clusters), "with t", len(interesting))

    large_cluster = cmap.largest_cluster()
    print(",".join(sorted(large_cluster)))

main("in/in_23_test.txt")
main("in/in_23.txt")
