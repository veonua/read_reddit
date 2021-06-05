import asyncio
import datetime
import itertools

import pandas as pd
from aiostream import pipe, stream
from tqdm.asyncio import tqdm

from reddit_utils import subreddit, bot_list
from spacy_magic import make_nlp
from text_utils import norm_doc, norm

columns = ["_id",
           "body", "body_lemma", "body_lemma_wcount",
           "title", "title_lemma", "title_lemma_wcount",
           'tickers', "flair", "created", "author", "author_id", "is_bot", "pinned",
           "score_", "ups_", "downs_", "upvote_ratio_", "total_awards_received_", "gilded_", "edited_", "num_comments_",
           "_kind", "subreddit", "subreddit_id", "submission_id", "parent_id", "depth",
           ]


async def process_batch(batch_list, nlp):
    batch_size = len(batch_list)
    piece = pd.DataFrame(batch_list, columns=columns)
    piece['title'].fillna('', inplace=True)
    piece['body'].fillna('', inplace=True)
    title_outs = stream.iterate(nlp.pipe(piece['title'].apply(norm), batch_size=batch_size)) \
                 | pipe.map(norm_doc, ordered=False) | pipe.list()
    body_outs = stream.iterate(nlp.pipe(piece['body'].apply(norm), batch_size=batch_size)) \
                | pipe.map(norm_doc, ordered=False) | pipe.list()

    # I don't know how to unzip better
    title_outs = list(zip(*await title_outs))
    body_outs = list(zip(*await body_outs))

    piece['body_lemma'] = body_outs[0]
    piece['body_lemma_wcount'] = body_outs[1]

    piece['title_lemma'] = title_outs[0]
    piece['title_lemma_wcount'] = title_outs[1]

    piece['tickers'] = list(map(lambda x, y: ','.join(x | y), title_outs[2], body_outs[2]))
    piece["created"] = pd.to_datetime(piece["created"], unit="s")
    piece["created_date"] = piece["created"].dt.date
    piece["created_time"] = piece["created"].dt.time
    piece['is_bot'] = piece[piece['author'].isin(bot_list)]['author']

    piece["pinned"] = piece["pinned"].fillna(False)
    piece["edited_"] = pd.to_datetime(piece["edited_"], unit="s")
    return piece.set_index('_id', verify_integrity=True)


async def save(batches):
    batch = pd.concat(batches, verify_integrity=True)
    dt = batch.iloc[-1]['created']
    time_str = dt.strftime("%Y_%b_%d-%H")

    filename = f"../data/{file_prefix}.{time_str}.parquet"
    batch.to_parquet(filename)


async def main(subreddits):
    batch_size = 1000
    batches_in_file = 100

    NLP_PROCESSORS = 1
    nlps = stream.iterate(itertools.cycle([make_nlp() for _ in range(NLP_PROCESSORS)]))

    global file_prefix
    file_prefix = "_".join(subreddits)

    progress = tqdm(iterable=itertools.count(), smoothing=0.3, unit_scale=True, unit='topics')
    reddit_stream = await subreddit(subreddits, after=datetime.date(2021, 5, 1), progress=progress)

    await (reddit_stream.stream()
           | pipe.chunks(batch_size) \
           | pipe.map(process_batch, nlps, ordered=False, task_limit=NLP_PROCESSORS) \
           | pipe.chunks(batches_in_file) \
           | pipe.action(save))


if __name__ == "__main__":
    import argparse

    # ["SPACs", "investing", "bitcoin", "stocks", "ethereum", "wallstreetbets"]
    parser = argparse.ArgumentParser(description='Help string')
    parser.add_argument('subreddits', metavar='N', type=str, nargs='+',
                        help='subreddits')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(subreddits=args.subreddits))
    loop.close()
