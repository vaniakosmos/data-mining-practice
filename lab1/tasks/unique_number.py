from lab1.utils import *


class NumberOfUniqueMapReduce(MapReduce):
    def _mapper(self, sub_seq: list) -> tuple:
        return sub_seq, None

    def _merge(self, keys: tuple) -> dict:
        out = {}
        for key, value in keys:
            if key not in out:
                out[key] = None
        return out

    def _reduce(self, keys: dict) -> list:
        return [len(keys)]

    def _make_sub_seqs(self, seq: list):
        return seq

    def _straight_func(self):
        return lambda seq: len(set(seq))

