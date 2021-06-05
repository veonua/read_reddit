from __future__ import annotations

import logging
import itertools

from collections import defaultdict, Sequence, Counter
from dataclasses import dataclass, field
from typing import Tuple, Dict, Union, List, Any, MutableMapping, Optional
from copy import deepcopy

import dataclasses
import numpy as np

from pyutils import append, put_or_throw, split_tail


@dataclass
class Word:
    index: int
    links: Counter = field(default_factory=Counter)
    collocations: Dict[str, int] = field(default_factory=defaultdict)

    def freq(self) -> int:
        return sum(v for k, v in self.links.items())

    def __iadd__(self, other: Word):
        self.links += other.links
        # self.freq += other.freq
        return self


class WordLink(MutableMapping[Union[Tuple[str], str], Word]):
    START = '^'
    STOP = '\f'

    def __init__(self, mapping: WordLink = (), **kwargs):
        super().__init__()
        if mapping:
            # super(WordLink, self).__init__(mapping, **kwargs)
            self.content = deepcopy(mapping.content)
            self.reverse = mapping.reverse.copy()
            self.empty_spaces = mapping.empty_spaces.copy()
            self.backward_link = mapping.backward_link.copy()
            self.synonyms = deepcopy(mapping.synonyms)
            return

        self.content: Dict[Union[Tuple[str], str], Word] = dict()
        self.reverse: List[Union[Tuple[str], Optional[str]]] = list()
        self.backward_link: [int, set] = defaultdict(set)
        self.synonyms: Dict[str, int] = dict()
        self.empty_spaces: List[int] = []

        self[self.START] = Word(index=0)
        self[self.STOP] = Word(index=1)

    def rev(self, idx):
        return self.reverse[idx]

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)

    def __delitem__(self, key):
        word = self.content.pop(key, None)
        if word is not None:
            self.empty_spaces.append(word.index)
            self.reverse[word.index] = None
        self.dump()

    def most_common(self, n: int = 0):
        freq = np.array(
            [v.freq() if v.index > 2 else 0 for v in self.content.values()])  # skip START, STOP  #np.array()
        terms = np.array(list(self.content.keys()), dtype=object)
        idx = np.argsort(freq)
        if n > 0:
            idx = idx[-n:][::-1]
        else:
            idx = idx[:n]

        return list(zip(terms[idx], freq[idx]))

    def back(self, index: [Sequence, str, int]) -> [int, Counter]:
        # if isinstance(index, Tuple):
        #    return self[index[1]].links[index[0]]
        res = Counter()
        for word in self.backward_link[index].copy():
            try:
                res[word] = self[word].links[index]
            except KeyError: # dead limks to misspells
                self.backward_link[index].remove(word)

        return res

    def __setitem__(self, index, value: Word):
        if value.index == len(self.reverse):
            self.reverse.append(index)
        else:
            assert (not self.reverse[value.index] or self.reverse[value.index] == index)
            # self.reverse[value.index] = index

        self.content.__setitem__(index, value)

    def __contains__(self, item: [Tuple[str, str], str]) -> bool:
        if self.content.__contains__(item):
            return True

        if isinstance(item, tuple):
            parent, tail = split_tail(item)
            parent_n = self.content.get(parent, None)
            if parent_n and tail in parent_n.collocations:
                return True

        return item in self.synonyms

    def get_index(self, item: Union[Tuple[str, str], str]) -> int:
        if item in self.content:
            return self.content[item].index

        if isinstance(item, tuple):
            parent, tail = split_tail(item)
            res = self.content[parent].collocations.get(tail)
            if res:
                return res
        elif item in self.synonyms:
            return self.synonyms[item]

        raise IndexError(f'{item} is not found')

    def __getitem__(self, item: [str, Tuple[str, str]]) -> Word:
        val = None
        if isinstance(item, str):
            val = self.synonyms.get(item, None)
        elif isinstance(item, Tuple):
            parant, tail = split_tail(item)
            val = self.content[parant].collocations.get(tail, None)
        if val:
            item = self.reverse[val]

        return self.content[item]

    def __iadd__(self, other: WordLink):
        for word, stats in other.items():
            if word not in self:
                w = dataclasses.replace(stats)
                w.index = self._get_free_index()
                self[word] = w
            else:
                self[word] += stats

        for word, link in other.backward_link.items():
            if word not in self.backward_link:
                self.backward_link[word] = link
            else:
                self.backward_link[word] |= link

        return self

    def copy(self) -> WordLink:  # don't delegate w/ super - dict.copy() -> dict :(
        return type(self)(self)

    def backward_set(self, index: int) -> set:
        return self.backward_link[index]

    def link(self, w_str: Union[str, Tuple[str,str]], next_word: str):
        word = self.get_or_create(w_str)
        coll: int = word.collocations.get(next_word, None)
        if coll:  # never happens as collocations in parent method?
            return self.content[self.reverse[coll]]

        coll = self.synonyms.get(append(w_str, next_word), None)
        if coll:
            logging.warning(f'synonyms are deprecated {word} {next_word}')
            return self.content[self.reverse[coll]]

        word.links[next_word] += 1
        self.backward_link[next_word].add(w_str)  # todo: should add collocation if found later

        return self.get_or_create(next_word)

    def append_collocation(self, word: [str, Tuple[str]], next_word: [str, Tuple[str]], freq: int = 0,
                           synonyms: List[str] = list()):
        logging.info(f'+ {word}:{next_word} = {",".join(synonyms)}')

        first = self.get_or_create(word, exact=True)  # remove exact after we see how the synonyms work
        collocation = self.get_or_create(word, next_word)
        first.links.pop(next_word, None)
        put_or_throw(first.collocations, next_word, collocation.index)

        for syn in synonyms:
            pair2 = append(word, syn)
            if pair2 in self.content:
                raise NotImplemented("less frequent token is already added, need to handle this")
            first.links.pop(syn, None)
            put_or_throw(first.collocations, syn, collocation.index)

            # don't use synonyms for collocations anymore self.synonyms[pair2] = collocation.index

    # def get_canonical(self, val: [str, Tuple, int]) -> Union[str, Tuple[str, str]]:
    #     if isinstance(val, Tuple):
    #         parent, tail = split_tail(val)
    #         val = self.content[parent].collocations[tail]
    #     elif isinstance(val, str):
    #         val = self.synonyms[val]
    #
    #     return self.reverse[val]
    #
    # def set_canonical(self, right, wrong):
    #     # todo: use collocations insted of synonyms
    #     def do(_right, _wrong):
    #         assert right != wrong
    #         synonyms_idx = self.synonyms.pop(_right, None)
    #
    #         if _right in self.content:
    #             content_word = self.content[_right]
    #             self.reverse[content_word.index] = _right
    #             self.synonyms[_wrong] = content_word.index
    #
    #             wrong_word = self.content.pop(_wrong, None)
    #             if wrong_word:
    #                 logging.debug(f"pop {_wrong}, push {_right}")
    #                 assert wrong_word.index != content_word.index
    #                 self.empty_spaces.append(wrong_word.index)
    #                 self.reverse[wrong_word.index] = None
    #                 content_word += wrong_word
    #             return
    #
    #         content_word = self.content.get(_wrong, None)
    #         if synonyms_idx and content_word and synonyms_idx != content_word.index:
    #             raise NotImplementedError
    #
    #         if not content_word:
    #             if not synonyms_idx:
    #                 raise NotImplementedError
    #
    #             old = self.reverse[synonyms_idx]
    #             logging.debug(f"move {old} to synonyms")
    #             content_word = self.content.pop(old)
    #             self.synonyms[old] = content_word.index
    #
    #         self.content[_right] = content_word
    #         logging.debug(f"pop {_wrong}, push {_right}")
    #         self.content.pop(_wrong, None)
    #         self.reverse[content_word.index] = _right
    #         self.synonyms[_wrong] = content_word.index
    #
    #     if not isinstance(wrong, list):
    #         wrong = [wrong]
    #
    #     everything = [right] + wrong
    #     wrong = set(itertools.product(*map(set, zip(*everything)))) - {right}
    #
    #     for item in wrong:
    #         do(right, item)
    # assert len(self) == len(self.reverse)

    def dump(self):
        pass

    def get_or_create(self, item: Union[Tuple[str, str], str], item2: str = None, exact=False) -> Word:
        if item2 is not None:
            item = append(item, item2)

        if item in self.content:
            return self.content[item]

        if isinstance(item, tuple):
            parent, tail = split_tail(item)
            parent_n = self.content.get(parent, None)
            if parent_n:
                child_n = parent_n.collocations.get(tail, None)
                if child_n:
                    assert not exact
                    return self.content[self.reverse[child_n]]
        elif item in self.synonyms:
            assert not exact
            return self.content[self.reverse[self.synonyms[item]]]

        result = Word(index=self._get_free_index())
        self.__setitem__(item, result)
        return result

    def _get_free_index(self):
        if self.empty_spaces:
            return self.empty_spaces.pop()
        return len(self.reverse)

    def collocations(self, start: str, deep=True, search_synonyms=True):
        src = self if search_synonyms else self.content
        idxs = set(src[start].collocations.values())

        for i in idxs:
            token = self.reverse[i]
            yield token
            if deep:
                yield from self.collocations(token, search_synonyms=False)

    def reset_links(self):
        # misspell links from old reads need to be cleaned up in better way
        # now every read will start with new links
        for v in self.content.values():
            v.links = Counter()
        self.backward_link = defaultdict(set)

    def report(self, token:str, n=10):
        item = self[token]
        print( f"forward: {list(self.collocations(token))}\n" \
               f"candidates: {item.links.most_common(n)}\n" \
               f"back: {self.back(token).most_common(n)}")
