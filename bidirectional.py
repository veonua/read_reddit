from collections import defaultdict, Counter
from typing import Sequence, Tuple

import numpy as np


class BiDirectionalNode:

    def __init__(self):
        self.forward = defaultdict(Counter)
        self.backward_ = defaultdict(set)

    def __len__(self):
        return len(self.forward)

    def __getitem__(self, index: [Sequence, str, int]) -> [int, Counter]:
        if isinstance(index, Tuple):
            return self.forward[index[0]][index[1]]
        else:
            return self.forward[index]

    def __iter__(self):
        return self.forward.__iter__()

    def items(self):
        return self.forward.items()

    def back(self, index: [Sequence, str, int]) -> [int, Counter]:
        if isinstance(index, Tuple):
            return self.forward[index[1]][index[0]]

        return Counter({word: self.forward[word][index] for word in self.backward_[index]})

    def __setitem__(self, index, value: int):
        self.backward_[index[1]].add(index[0])
        self.forward[index[0]][index[1]] = value

    def backward_set(self, index: int) -> set:
        return self.backward_[index]

    def __repr__(self):
        return self.forward.__repr__()

    def __iadd__(self, other):
        if not isinstance(other, BiDirectionalNode):
            raise TypeError('Invalid input format.')

        for b, other_set in other.backward_.items():
            self.backward_[b] |= other_set

        for f, other_count in other.forward.items():
            self.forward[f] += other_count

        return self

    def __eq__(self, other):
        if not isinstance(other, BiDirectionalNode):
            raise TypeError('Invalid input format.')

        for b, other_set in other.backward_.items():
            if self.backward_[b] != other_set:
                return False

        for f, other_count in other.forward.items():
            if self.forward[f] != other_count:
                return False

        return True

    def inverse_transform(self, inverse_vocabulary: np.array):
        def apply_dict(X):
            return Counter({inverse_vocabulary[k]: v for k, v in X.items()})

        def apply_set(X):
            return {inverse_vocabulary[k] for k in X}

        result = BiDirectionalNode()
        result.backward_ = {inverse_vocabulary[k]: apply_set(v) for k, v in self.backward_.items()}
        result.forward = {inverse_vocabulary[k]: apply_dict(v) for k, v in self.forward.items()}
        return result