from lab1.utils import *


class MaximumMapReduce(MapReduce):
    def _mapper(self, sub_seq: list) -> tuple:
        return 0, max(sub_seq)

    def _merge(self, keys: tuple) -> dict:
        out = {}
        for key, value in keys:
            if key not in out:
                out[key] = value
            else:
                out[key] = max(value, out[key])
        return out

    def _reduce(self, keys: dict) -> list:
        out = []
        for key, value in keys.items():
            out.append(value)
        return out

    def _make_sub_seqs(self, seq: list):
        return slice_seq(seq, 10)

    def _straight_func(self):
        return max
