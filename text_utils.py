from string import punctuation, whitespace
from string import punctuation, whitespace
from typing import Tuple, Optional

from spacy_magic import looks_like_ticker
from synonyms import synonyms


def preprocess_token(token) -> Optional[Tuple[str, bool]]:
    lemma = token.lemma_.strip(punctuation + whitespace).lower()

    if not lemma or len(lemma) > 15 or token.is_punct:  # not token or token.is_stop
        return None

    if token.shape_.startswith('d'):  # token.is_digit:
        return "▸" + token.shape_, False

    if lemma in synonyms.keys():
        return synonyms[lemma], True
    else:
        is_ticker = lemma in synonyms.values() or looks_like_ticker(token)

    return lemma, is_ticker


def norm_doc(doc):
    complete_filtered_tokens = list(filter(None, [
        preprocess_token(token) for token in doc
    ]))

    lemmatized_sentence: str = " ".join([tt[0] for tt in complete_filtered_tokens])
    tickers: set = {tt[0] for tt in complete_filtered_tokens if tt[1]}

    return lemmatized_sentence, len(complete_filtered_tokens), tickers


def norm(val: str):
    if not val:
        return ''
    for ch in ["‘", "’"]:
        val = val.replace(ch, "'")

    from markdown_utils import unmark
    return unmark(val)
