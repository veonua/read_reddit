from glob import glob

import dill
import pandas as pd

from WordLink import WordLink
from pyutils import csr_hstack
from vectorizer import MyVectorizer
from bidirectional import BiDirectionalNode
from stop_words import ENGLISH_STOP_WORDS

import unittest


class MyTestCase(unittest.TestCase):

    def test_make_default_token_dict(self):
        t1 = BiDirectionalNode()
        t1[0, 5] += 1
        t1[0, 5] += 1
        t1[0, 2] += 1
        t1[1, 5] += 3

        self.assertEqual(t1[0, 0] , 0)
        self.assertEqual(t1[0, 2] , 1)
        self.assertEqual(t1[0, 5] , 2)
        self.assertEqual(t1[1, 5] , 3)

    def test_vect(self):
        docs = [
            'hi do anyone have a source for historical datum on this index pron be not sure how far back the data go but go back to the ▸ddx or ▸ddx would be great thank',
            "over ▸d,dddx Test 1 pron would't Test 2 pron wouldn't Test 3 pron would'nt Test 4 pron wouldn Test 5 pron would not Test 6 pron wouldn't Test 7 pron would Test 8 pron would",
            'have pron sign a security agreement and attach pron to collateral pron own free of any lein neither a borrower nor a lender be pron can not but pron can minimize damage by ask for collateral and stuff for example when pron post bond for someone pron can put pron house as collateral in case someone try to skip with pron money would not want to lose a house over ▸dx',
            'there be always a chance that pron will get away with the money so pron should hedge pron bet and',
            'pron thread look like pron ask a question as a reminder generic advice posts beginner question will be remove if pron post appear to break the rule please remove pron and post in the daily advice thread that be stickie pron be a bot and this action be perform automatically please contact the moderator of this subreddit message compose to r investing if pron have any question or concern',
            'definitely not lend tree have pron vhecke crowd lend like twino pron take something worth ▸ddd as collateral say a watch or jewelry then if pron do not pay pron sell pron this be what pawn shop do',
            'remind pron of pron business law class last semester yeah pretty much how much be pron try to loan because if pron be not that much then the effort of go through something like this be not worth pron',
            'stop thank satoshi about this pron do not mean this',
            'pron do not matter because pron be not pron return',
            '▸d billion eiquya bitcoin good investment of the decade with one',
            'わ か り ま せ ん',
            'pron love this',
            'the be sick do anyone know that pron would skyrocket that much',
            'thx satoshi i owe pron something',
            'wonder what pron will say in ▸dddd',
            'knowledge be know that there be no year ▸d so technically the new decade begin january ▸d ▸dddd not ▸dddd wisdom be know that pron start this system in the middle pron be socially construct anyway and pron feel right to treat ▸d to ▸dd as a decade so that be what pron do',
            'happy new year and a wealthy new decade thx satoshi for this awesome decade happy new year and ye thanks craig bring on the hater and no censorship hypocrite people try to silence pron pron lol xoxoxo 🤖',
            'pron be not talk about the future pron be talk about ▸dddd ▸dddd performance the graphic imply bitcoin go from around ▸d.dddd in ▸dddd to the current ▸d,dddxxx in ▸dddd consider the first price transaction be ▸dd in pizza for ▸dd,ddd bitcoin the first price could be argue to be ▸.ddd in ▸dddd so a ▸d,ddd,ddd gain then again bitcoin technically start at ▸d so the gain approach infinity on the first usd denominate transaction for anyone who mine while bitcoin be technically worthless not include mining cost',
            '何',
            'index start at ▸d',
            'pron treat pron ▸d ▸d as a decade to be precise even if pron start in year ▸d or year ▸d that would not really change perception of a decade change because the digit in the ten spot be what definitely determine the decade',
            'no hate here for the genius who can not remember pron own recovery phrase to unlock the fortune pron need to access just pity 🙁',
            'tsk tsk tsk faketoshi shill smfh',
            'do pron depreciate that quick though pron do not think inflation have result in that much depreciation in the past decade but pron could be wrong',
            'what be a kanji really use to spell nani instead of hiragana']

        dd = [doc.split(" ") for doc in docs]

        vec1 = MyVectorizer(stop_words=ENGLISH_STOP_WORDS, lowercase=False)
        res11, vocabulary11 = vec1.fit_transform(dd[:10])
        res12, vocabulary12 = vec1.fit_transform(dd[10:])

        res1 = csr_hstack(res11, res12)
        vocabulary11 += vocabulary12
        #vec1.vocabulary = vocabulary11

        vec2 = MyVectorizer(stop_words=ENGLISH_STOP_WORDS, lowercase=False)
        res2, vocabulary2 = vec2.fit_transform(dd)

        self.assertEqual( list(vocabulary11.keys()) , list(vocabulary2.keys()))
    #    assert (res1 != res2).nnz == 0

#        self.assertEqual( set(dd[0]) - ENGLISH_STOP_WORDS , set(vec1.inverse_transform(res11[0])[0]))
        vec2.reduce(vocabulary2)

        synonyms = vec2.vocabulary[('pron')].collocations
        self.assertIn(("wouldn't"), synonyms)
        self.assertIn(("would't"), synonyms)
        self.assertEqual(synonyms["would'nt"], synonyms["wouldn't"])
        self.assertIn(('pron', "wouldn't"), vec2.vocabulary)

        res2, vocabulary2 = vec2.fit_transform(dd)
        vec2.vocabulary = vocabulary2.copy()

        misspells = {"would'nt", "wouldn't", "would't"}
        fixes = {('pron', "wouldn't")}
        self.assertEqual(set(dd[1]) - ENGLISH_STOP_WORDS - misspells | fixes, set(vec2.inverse_transform(res2[1])[0]))

        #self.assertIn(('pron', "wouldn"), synonyms)


    def test_df(self):
        skip = 0
        with open('vocab_.57', 'rb') as f:
            vocab:WordLink = dill.load(f)
            skip = 7
            #vocab.reset_links()

        vectorizer = MyVectorizer(stop_words=ENGLISH_STOP_WORDS, lowercase=False)
        vectorizer.vocabulary = vocab

        #vectorizer.vocabulary.append_collocation('warren', 'buffett', synonyms=["bufet", 'buffet', 'buffets'])
        #vectorizer.vocabulary.append_collocation('cathie', 'wood', synonyms=["woods"])
        # vocab4.set_canonical(right=('warren', 'buffett'),
        #                      wrong=[('waren', 'bufet'), ('warrenn', 'buffet'), ('warenn', 'bufett')])
        #
        # vocab4.set_canonical(right=('cathie', 'wood'),
        #                      wrong=[('cathy', 'woods'), ('kathy', 'woods'), ('auntie', 'woods')])

        files = glob("../data/*.parquet")

        id = 0
        for file in files:
            id += 1
            if id <= skip:
                continue

            df = pd.read_parquet(f"{file}").sort_values("created")
            # df.loc[df['author'] == 'lntipbot', 'is_bot'] = 'lntipbot'
            # df.loc[df['author'] == 'remindditbot', 'is_bot'] = 'remindditbot'
            # df.loc[df['author'] == 'RemindMeBot', 'is_bot'] = 'RemindMeBot'

            df = df[df['is_bot'].isna()].drop(columns=['is_bot'])
            len(df)
            self.tdf(vectorizer, id, df)

        with open('vectorizer', 'wb') as f:
            dill.dump(vectorizer, f)

    def tdf(self, vectorizer, id , df):

        tokens = df['body_lemma'].apply(lambda doc: doc.split(" "))

        res, voc = vectorizer.fit_transform(tokens)
        vectorizer.reduce(voc)
        res2, voc2 = vectorizer.fit_transform(tokens)
        vectorizer.vocabulary = voc2
        with open(f'vocab_.{id}', 'wb') as f:
            dill.dump(vectorizer.vocabulary, f)


if __name__ == '__main__':
    unittest.main()

