from lab1.utils import *


class AverageMapReduce(MapReduce):
    def _mapper(self, sub_seq: list) -> tuple:
        return 0, sum(sub_seq), len(sub_seq)

    def _merge(self, keys: tuple) -> dict:
        out = {}
        for key, s, l in keys:
            if key not in out:
                out[key] = (s, l)
            else:
                out[key] = (s + out[key][0], l + out[key][1])
        return out

    def _reduce(self, keys: dict) -> list:
        out = []
        for key, value in keys.items():
            s, l = value
            out.append(s / l)
        return out

    def _make_sub_seqs(self, seq: list):
        return slice_seq(seq, 10)

    def _straight_func(self):
        return lambda seq: sum(seq)/len(seq)
