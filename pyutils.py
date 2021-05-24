from typing import Sequence, Union, Tuple, Dict

import numpy as np
import scipy as sp
from scipy.sparse import hstack


def hasNumbers(inputString: str) -> bool:
    return any(char.isdigit() for char in inputString)


def select_nz(matrix, pattern: Sequence)->Sequence[int]:
    pattern = set(pattern)
    prev_ind = 0
    row_id = -2
    for ind in matrix.indptr:
        row_id += 1
        if ind == prev_ind:
            continue
        cols = set(matrix.indices[prev_ind:ind])
        if pattern.issubset(cols):
            yield row_id

        prev_ind = ind



def csr_hstack(res11, res12)->sp.sparse.csr_matrix:
 data = np.hstack([res11.data, res12.data])
 indices = np.hstack([res11.indices, res12.indices])
 indptr = np.hstack([res11.indptr, res12.indptr[1:] + res11.indptr[-1]])

 r1, c1 = res11.shape
 r2, c2 = res12.shape

 return sp.sparse.csr_matrix((data, indices, indptr),
                             shape=(r1 + r2, max(c1, c2)),
                             dtype=res11.dtype)


def append(prev_feature: Union[str, Tuple[str,str]], word: str) -> Tuple[str, str]:
    # append strings to tuple, flat structure guaranteed
    if isinstance(prev_feature, tuple):
        return prev_feature + (word,)
    elif isinstance(prev_feature, str):
        return prev_feature, word
    else:
        raise TypeError(f"{type(prev_feature)} is not supported")


def split_tail(val:Tuple)-> Tuple[str, str]:
    # splits tuple to body and tail
    if len(val) < 2:
        raise ValueError("too few elements")

    if len(val)==2:
        return val[0], val[1]
    return val[:-1], val[-1]


def put_or_throw(di:Dict, key, value):
    # do not allow to override values in dict
    v = di.get(key)
    if v is None:
        di[key] = value
        return
    assert v == value

