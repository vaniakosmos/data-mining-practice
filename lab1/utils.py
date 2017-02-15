def slice_seq(seq: list, parts=10):
    l = len(seq)
    temp = l // parts
    p = temp if l % parts == 0 else temp + 1
    out = []
    for i in range(parts):
        sub = seq[i*p: (i+1)*p]
        if len(sub) != 0:
            out.append(sub)
    return out


def print_title(title: str, length=89):
    half = (length - len(title) - 2) // 2
    corrector = 1 if len(title) % 2 == 0 else 0
    print(f"{'#'*length}")
    print(f"{'#'*half} {title} {'#'*(half + corrector)}")
    print(f"{'#'*length}\n")


class MapReduce(object):
    def _mapper(self, sub_seq: list) -> tuple:
        pass

    def _merge(self, keys: tuple) -> dict:
        pass

    def _reduce(self, keys: dict) -> list:
        pass

    def _make_sub_seqs(self, seq: list) -> list:
        pass

    def _straight_func(self):
        pass

    def calculate(self, seq):
        sub_seq_list = self._make_sub_seqs(seq)
        func = self._straight_func()

        keys = tuple(map(self._mapper, sub_seq_list))
        print(f"Mapped:  {keys}")

        keys = self._merge(keys)
        print(f"Merged:  {keys}")

        keys = self._reduce(keys)
        print(f"Reduced: {keys}")
        print(f"Actual answer: {func(seq)}")
        print()
