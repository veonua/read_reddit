import re
from typing import Optional
import intervaltree

import spacy
from spacy.lang.tokenizer_exceptions import URL_PATTERN
from spacy.matcher.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens.span import Span
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

from synonyms import synonyms
from tickers import non_tickers, tickers, currency, orgs, currency_signs


def looks_like_ticker(val) -> Optional[str]:
    # string = val.text
    norm = val.norm_

    if norm in synonyms.keys():
        return synonyms[norm]
    elif norm in synonyms.values():
        return norm

    if val.ent_type_ == "STOCK":
        return norm

    le = len(norm)
    if 2 > le or le > 6 or val.ent_type_ not in ["MAYBE_STOCK"]:
        return None

    if val.is_oov:
        if norm in non_tickers:
            return None
        return norm
    else:
        if norm in tickers:
            return norm
        return None


def make_nlp():
    def custom_tokenizer(nlp):
        infixes = nlp.Defaults.infixes + tuple([r"([^'a-zA-Z0-9\.,])"])
        prefixes = nlp.Defaults.prefixes + tuple(currency_signs)
        suffixes = tuple(r'[\.]') + nlp.Defaults.suffixes
        reddit_link = r"|([r|u]/\w)"

        nlp.tokenizer.infix_finditer = compile_infix_regex(infixes).finditer
        nlp.tokenizer.prefix_search  = compile_prefix_regex(prefixes).search
        nlp.tokenizer.suffix_search  = compile_suffix_regex(suffixes).search

        nlp.tokenizer.url_match = re.compile("(?u)" + URL_PATTERN + reddit_link).match

    nlp = spacy.load("en_core_web_md", exclude=["ner"])
    stock_symbol_shapes_ruler = EntityRuler(nlp)

    stock_symbol_shapes_ruler.name = "stock_symbol_shapes_ruler"
    patterns_stock_symbol_shapes = [
        {"label": "CURRENCY", "pattern": [{'LOWER': {"IN": list(currency)}}]},
        {"label": "ORG", "pattern": [{"LEMMA": {"IN": list(orgs)}}]},
        {"label": "MAYBE_STOCK",
         "pattern": [{'POS': {"IN": ["PROPN", "NOUN"]}, 'IS_UPPER': True, 'IS_ALPHA': True, 'LENGTH': {">=": 2}}]},
    ]
    stock_symbol_shapes_ruler.add_patterns(patterns_stock_symbol_shapes)

    custom_tokenizer(nlp)

    nlp.add_pipe(EntityRuler2(nlp.vocab), before='ner')
    nlp.add_pipe(stock_symbol_shapes_ruler, before='ner')
    return nlp


class EntityRuler2(object):
    def __init__(self, vocab):
        self.matcher = Matcher(vocab, validate=True)
        # Add match ID "HelloWorld" with unsupported attribute CASEINSENSITIVE
        stock_patterns = [
            [{'LOWER': 'stock'}, {'LOWER': 'symbol'}, {'ORTH': ':'}, {'IS_SPACE': True, 'OP': '?'}, {'IS_UPPER': True}],
            [{'LEMMA': '$', "SPACY": False},
             {'IS_ALPHA': True, 'LENGTH': {"<": 7}, 'ORTH': {'NOT_IN': list(non_tickers)}}],
            [{'SHAPE': {'IN': ["XXX.X", "XX.X"]}}],
        ]

        abbr_patterns = [
            [{'LOWER': 's'}, {'ORTH': '&'}, {'LOWER': 'p'}],
            [{'LOWER': 's'}, {'ORTH': '&'}, {'LOWER': 'p500'}],
            [{'LOWER': 'p'}, {'ORTH': '/'}, {'LOWER': 'e'}],
            [{'LOWER': 'p'}, {'ORTH': '/'}, {'LOWER': 'es'}],
            [{'LOWER': 'p'}, {'ORTH': '/'}, {'IS_UPPER': True, 'LENGTH': {"<": 3}}]
        ]

        self.matcher.add("STOCK", stock_patterns)
        self.matcher.add("ABBR", abbr_patterns)

    def __call__(self, doc):
        try:
            matches = list(self.matcher(doc))  # + list(self.phrase_matcher(doc))
            if not matches:
                return doc

            matches = set(
                [(start, end, m_id) for m_id, start, end in matches if start != end]
            )

            tree = intervaltree.IntervalTree.from_tuples(matches)
            tree.merge_overlaps(data_reducer=lambda x, higher: higher)

            STOCK = doc.vocab.strings['STOCK']
            ABBR = doc.vocab.strings['ABBR']

            new_entities = set()
            abbrs = []
            for start, end, match_id in tree:
                if match_id == STOCK:
                    span = Span(doc, end-1, end, label="STOCK")
                    new_entities.add(span)
                elif match_id == ABBR:
                    span = doc[start:end]
                    abbrs.append(span)

            doc.ents += tuple(new_entities)
            with doc.retokenize() as retokenizer:
                for span in abbrs:
                    retokenizer.merge(span)

        except ValueError as ex:
            print(str(doc))
            print(ex)
            raise

        return doc
