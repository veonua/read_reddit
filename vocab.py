import logging
from typing import List, Tuple, Any

from pyutils import append


class Vocab:
    START = ''
    STOP = '\f'

    def __init__(self):
        self.reverse: List[str] = list()
        self.vocabulary = dict()
        self.synonyms = dict()
        self[self.START] = 0
        self[self.STOP] = 1

    def keys(self):
        return self.vocabulary.keys()

    def rev(self, idx):
        return self.reverse[idx]

    def __contains__(self, key: [str, Tuple[str]]):
        return key in self.synonyms or key in self.vocabulary

    def __getitem__(self, key: [str, Tuple[str]]):
        if key in self.synonyms:
            return self.synonyms[key]
        if key in self.vocabulary:
            return self.vocabulary[key]
        else:
            value = len(self.vocabulary)
            self.__setitem__(key, value)
            return value

    def __setitem__(self, key, value):
        self.vocabulary[key] = value
        if value == len(self.reverse):
            self.reverse.append(key)
        else:
            self.reverse[value] = key

    def __len__(self):
        return self.vocabulary.__len__()

    def add_synonyms(self, word: [str, Tuple[str]], next_word: [str, Tuple[str]], synonyms: List[Any]):
        logging.info(f'== {word}:{next_word} = {",".join(synonyms)}')

        pair = append(word, next_word)
        idx = self[pair]
        for syn in synonyms:
            pair2 = append(word, syn)
            self.synonyms[pair2] = idx

    def append(self, word, next_word):
        pair = append(word, next_word)
        logging.info(f'+ {pair})')

        return self[pair]

    def copy(self):
        copy = Vocab()
        copy.reverse = self.reverse.copy()
        copy.vocabulary = self.vocabulary.copy()
        copy.synonyms = self.synonyms.copy()
        return copy