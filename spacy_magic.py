import re

import spacy
from spacy.lang.tokenizer_exceptions import URL_PATTERN
from spacy.matcher.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens.span import Span
from spacy.util import compile_infix_regex

from tickers import non_tickers, tickers, currency, orgs

def looks_like_ticker(val):
    # string = val.text
    norm = val.norm_
    le = len(norm)

    if val.ent_type_ == "STOCK":
        return True

    if 2 > le or le > 6 or val.ent_type_ not in ["MAYBE_STOCK"]:
        return False

    if val.is_oov:
        if norm in non_tickers:
            return False
        return True
    else:
        if norm in tickers:
            return True
        return False


def make_nlp():
    def custom_tokenizer(nlp):
        infixes = nlp.Defaults.infixes + tuple([r"^w"])
        infixes_re = compile_infix_regex(infixes)

        reddit_link = r"|([r|u]/\w)"

        nlp.tokenizer.infix_finditer = infixes_re.finditer
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
        patterns = [
            [{'LOWER': 'stock'}, {'LOWER': 'symbol'}, {'ORTH': ':'}, {'IS_SPACE': True, 'OP': '?'}, {'IS_UPPER': True}],
            [{'LEMMA': '$', "SPACY": False},
             {'IS_ALPHA': True, 'LENGTH': {"<": 7}, 'ORTH': {'NOT_IN': list(non_tickers)}}],
            [{'SHAPE': {'IN': ["XXX.X", "XX.X"]}}],
        ]
        self.matcher.add("stock_symbol", patterns)

    def __call__(self, doc):
        try:
            matches = list(self.matcher(doc))  # + list(self.phrase_matcher(doc))
            matches = set(
                [(m_id, start, end) for m_id, start, end in matches if start != end]
            )

            if matches:
                new_entities = set()
                for match_id, start, end in matches:
                    span = Span(doc, end-1, end, label="STOCK")
                    new_entities.add(span)

                doc.ents += tuple(new_entities)
        except ValueError as ex:
            print(str(doc))
            print(ex)
            raise

        return doc
