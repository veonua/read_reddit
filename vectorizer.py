from collections import Counter
from typing import Tuple, Union

import numpy as np
import scipy.sparse as sp
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import _VectorizerMixin, _make_int_array

from WordLink import WordLink, TemporaryVocabulary
from bidirectional import BiDirectionalNode
from pyutils import append
from rapidfuzz import process, fuzz

score_cutoff = fuzz.ratio('significant', 'insignificant') + 0.000001


class MyVectorizer(_VectorizerMixin, BaseEstimator):
    def __init__(self, dtype=np.int64,
                 input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None,
                 lowercase=True, preprocessor=None, tokenizer=None,
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), analyzer='word', n_features=(2 ** 20),
                 binary=False, ):
        self.vocabulary = WordLink()
        self.input = input
        self.encoding = encoding
        self.decode_error = decode_error
        self.strip_accents = strip_accents
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer
        self.analyzer = analyzer
        self.lowercase = lowercase
        self.token_pattern = token_pattern
        self.stop_words = stop_words
        self.n_features = n_features
        self.ngram_range = ngram_range
        self.binary = binary
        self.dtype = dtype

    def _warn_for_unused_params(self):
        pass

    def fit(self, raw_documents, y=None):
        """Learn a vocabulary dictionary of all tokens in the raw documents.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.

        Returns
        -------
        self
        """
        self._warn_for_unused_params()
        self.fit_transform(raw_documents)
        return self

    def fit_transform(self, raw_documents, y=None) -> [sp.csr_matrix, WordLink]:
        """Learn the vocabulary dictionary and return document-term matrix.

        This is equivalent to fit followed by transform, but more efficiently
        implemented.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.

        Returns
        -------
        X : array of shape (n_samples, n_features)
            Document-term matrix.
        """
        # We intentionally don't call the transform method to make
        # fit_transform overridable without unwanted side effects in
        # TfidfVectorizer.
        if isinstance(raw_documents, str):
            raise ValueError(
                "Iterable over raw text documents expected, "
                "string object received.")

        vocabulary : WordLink = self.vocabulary
        new_vocabulary = TemporaryVocabulary(vocabulary)
        j_indices = []
        indptr = _make_int_array()
        values = _make_int_array()
        indptr.append(0)
        # analyze = self.build_analyzer()
        stop_words = self.get_stop_words() or {}

        for analyzed_doc in raw_documents:
            feature_counter = Counter()
            prev_str : Union[Tuple[str], str] = WordLink.START
            prev_index: int = 0

            doc = analyzed_doc + [WordLink.STOP]
            for word in doc:
                skip = False
                if word in stop_words: continue

                collocation = append(prev_str, word)
                if collocation in vocabulary: # optimization: combine with get_index
                    prev_index = vocabulary.get_index(collocation)
                    prev_str = vocabulary.reverse[prev_index]
                    skip = True # allows every word in collocation to hit feature_counter
                elif collocation in new_vocabulary:
                    raise NotImplementedError('that is strange')

                if prev_index > 1:
                    if self.binary:
                        feature_counter[prev_index] = 1
                    else:
                        feature_counter[prev_index] += 1

                if skip: continue
                prev_index = new_vocabulary.link(prev_str, word).index
                prev_str = word

            j_indices.extend(feature_counter.keys())
            values.extend(feature_counter.values())
            indptr.append(len(j_indices))

        j_indices = np.asarray(j_indices, dtype=np.intc)
        indptr = np.frombuffer(indptr, dtype=np.intc)
        values = np.frombuffer(values, dtype=np.intc)

        X = sp.csr_matrix((values, j_indices, indptr),
                          shape=(len(indptr) - 1, len(new_vocabulary)),
                          dtype=self.dtype)
        X.sort_indices()

        return X, new_vocabulary


    def reduce(self, vocabulary:WordLink):
        import queue

        for word, v in vocabulary.content.items():
            if v.index < 2: continue
            links = v.links.copy()
            del (links['\f'])
            del (links['pron'])
            del (links[word])

            collocations = [(k, 9999) for k in v.collocations.keys()] + links.most_common(5) # todo: replace with real frequency

            queue1 = queue.Queue()
            for next_word, freq in collocations:
                queue1.put(next_word)
                synonyms = []
                while not queue1.empty():
                    common_next_word = queue1.get()
                    if not common_next_word or common_next_word[0] == '▸': continue  # special number tokens

                    matches = process.extract(common_next_word, list(links.keys()),
                                              score_cutoff=score_cutoff, processor=False)  # processor=None,
                    for match in matches:
                        m_word = match[0]
                        freq2 = links[m_word]
                        if freq <= freq2: continue  # undefined right result
                        if m_word[0] == '▸': continue  # special number tokens
                        if len(m_word) > 2 and m_word[1] == '/': continue  # r/bitcoin
                        if match[1] > 99.99: continue  # emoticons
                        # TODO: filter out 'office <-> er'
                        if next_word == m_word:
                            assert False

                        queue1.put(m_word)
                        if next_word not in v.collocations.keys():
                            links[next_word] += freq2
                        del links[m_word]
                        synonyms.append(m_word)

                if synonyms:
                    self.vocabulary.append_collocation(word, next_word, synonyms=synonyms)
                    del links[next_word] # collocation already added, no need to process it further

            most = links.most_common(2)
            idx = 0
            if idx < len(most) - 1:
                first = most[idx]
                second = most[idx + 1]

                if not second or first[1] < 42:
                    continue

                if first[1] >= second[1] * 1.4:
                    self.vocabulary.append_collocation(word, first[0], freq=first[1])

    @property
    def inverse_vocabulary(self):
        return np.array(self.vocabulary.reverse)

    def inverse_transform(self, X):
        """Return terms per document with nonzero entries in X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Document-term matrix.

        Returns
        -------
        X_inv : list of arrays of shape (n_samples,)
            List of arrays of terms.
        """
        # self._check_vocabulary()

        if isinstance(X, BiDirectionalNode):
            return X.inverse_transform(self.inverse_vocabulary)

        if sp.issparse(X):
            # We need CSR format for fast row manipulations.
            X = X.tocsr()
        else:
            # We need to convert X to a matrix, so that the indexing
            # returns 2D objects
            X = np.asmatrix(X)
        n_samples = X.shape[0]

        return [self.inverse_vocabulary[X[i, :].nonzero()[1]].ravel()
                for i in range(n_samples)]
