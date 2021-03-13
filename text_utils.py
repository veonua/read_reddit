from string import punctuation, whitespace
from typing import Tuple, Optional

from spacy_magic import looks_like_ticker
from tickers import digit_exceptions, math_signs


def preprocess_token(token) -> Optional[Tuple[str, bool]]:
    lemma = token.lemma_.strip(punctuation + whitespace + math_signs).lower()

    if not lemma or len(lemma) > 15 or token.is_punct:  # not token or token.is_stop
        return None

    if lemma[0].isdigit():
        if lemma not in digit_exceptions:
            return "▸" + token.shape_, False

    ticker = looks_like_ticker(token)

    if ticker:
        return ticker, True
    else:
        return lemma, False


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
    for ch in ['‘', '’']:
        val = val.replace(ch, "'")

    for ch in ["\u200e", "\u200b", "\u2060", "\u202d"]:
        val = val.replace(ch, " ")

    from markdown_utils import unmark
    return unmark(val)
