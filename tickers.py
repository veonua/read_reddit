lemma_dict = {
    'specs': 'spec'
}

orgs = {'spac', 'wsb', 'aws', 'nyse', "nasdaq", 'irs', 'fbi', 'fed', 'sec', 'etf', 'hotbit', 'webull', 'degiro'}

currency = {'usd', 'cad', 'eur', 'gbp', 'euro', 'dollar'}

it_words = {'api', 'pdf', 'jpeg', 'pgp', 'ssl', 'sql', 'cpu', 'gpu', 'vpn', 'asic', 'asics', 'hw', 'ssd', 'ram', 'ui',
            'rtx',
            'gtx', 'ddos', 'utc'}
slang_abbr = {'atm', 'bnb', 'rolf', 'ligma', 'jpow', 'btfd', 'guh', 'lmao', 'hodler', 'gtfo', 'yolo', 'yoloed', 'win',
              'gang', 'boom', 'fud', 'fml', 'fomo', 'lol', 'wtf',
              'tbh', 'fyi', 'faq', 'imho', 'shit', 'fuck', 'dude', 'dick', 'blyat', 'cyka', 'cykas'}
geo = {'usa', 'uk', 'texas', 'tx', }
finance = {'ceo', 'cto', 'cfo', 'mba', 'ath', 'share', 'proof', 'eoy', 'ytd', 'ipo', 'inc', 'kyc', }


# ??? non_tickers = spacy.lang.en.stop_words.STOP_WORDS
non_tickers = {'covid', 'way', 'gay', 'rope', 'bear', 'fire', 'bears', 'wood', 'corp', 'user', 'porn', 'post', 'cash', 'mess',
               'kind', 'live', 'high', 'hear', 'profit', 'meme', 'dad', 'ride', 'jesus', 'open', 'ebook',
               'tell', 'recipe', 'want', 'hodl', 'wait', 'puts', 'hold', 'good', 'dex', 'sir', 'bank', 'poor', 'plan',
               'like', 'lady', 'have', 'zero', 'eip', 'cold', 'line', 'issue', 'spacs', 'dfv', 'death',
               'tgif', 'tldr', 'plus', 'irl', 'id', 'iv', 'new', 'senate', 'era', 'only', 'moon', 'sell', 'asap',
               'dont', 'long', 'loss', 'town', 'look', 'will', 'lot', 'moonsk', 'stonks', 'stonk',
               'into', 'feb', 'late', 'vlads', 'eps', 'est', 'mean', 'wassup', 'stake', 'stay', 'land', 'jail', 'ps',
               'kiss', 'use', 'let', 'buy', 'week', 'year', 'day', 'today', 'thank', 'ptsd', 'album', 'call', 'kanye',}
non_tickers |= currency | slang_abbr | it_words | geo | finance
non_tickers |= {o.lower() for o in orgs}
# https://www.twitch.tv/wsbzjz
tickers = {'nft', 'aal', 'kss', 'pbw', 'nkd', 'fizz', 'icln', 'ghiv', 'plug', 'prsp', 'vix', 'tak', 'apha', 'amd',
           'penn', 'jcp', 'vxx', 'voo', 'ko', 'blk', 'xlf', 'nly', 'pcg', 'cmg', 'dis', 'f', 'plab', 'shop', 'fdc',
           'mu', 'ag', 'amat', 'dow', 'ddog', 'bio', 'nio', 'pslv', 'hft', 'slm', 'rkt',
           'bch', 'zts', 'kar', 'navi', 'jpm', 'gs', 'anz', 'cba', 'spx', 'spy', 'cmp', 'dyor', 'bruh', 'uni', 'rvn',
           'ttd', 'mgni' 'mdni', 'amc', 'anz', 'snow', 'snpr', 'ark', 'qqq'}