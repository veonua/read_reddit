import itertools
import time
from datetime import date, datetime
from typing import AsyncGenerator, Dict, Tuple

import asyncpraw
from aiostream import stream, pipe, async_
from asyncpraw.models import MoreComments
from asyncpraw.reddit import Submission
from tqdm import tqdm

from psaw.psaw import PushshiftAPI

client_id = "JM9TDBDgHCiKcg"
client_secret = "XEEhfiRmer3EXpUDoPfwSscbhFQmVQ"


def to_row(some, submission_id=None):
    try:
        author = str(some.author)
        author_id = some.author_fullname
    except AttributeError:
        return None

    result = {
        "_id": some.id,
        "_kind": type(some).__name__.lower(),
        "subreddit": str(some.subreddit),
        "subreddit_id": some.subreddit_id,
        "created": some.created_utc,
        "author": author,
        "author_id": author_id,
        "score_": some.score,
        "submission_id": submission_id
    }

    if hasattr(some, "title"):  # if isinstance(some, psaw.PushshiftAPI.submission):
        result.update({
            "pinned": some.pinned,
            # "promoted": some.promoted,
            "title": some.title,
            "body": some.selftext,
            "parent_id": some.subreddit_id,
            "num_comments_": int(some.num_comments),
        })

    if hasattr(some, "link_flair_text"):
        result["flair"] = some.link_flair_text

    if hasattr(some, "upvote_ratio"):
        result["upvote_ratio_"] = some.upvote_ratio

    if hasattr(some, "total_awards_received"):
        result["total_awards_received_"] = some.total_awards_received

    if hasattr(some, "ups"):
        result.update({
            "ups_": some.ups,
            "downs_": some.downs,
            "gilded_": some.gilded,
            "edited_": some.edited if some.edited else None
        })

    if hasattr(some, "body"):
        result.update({
            "body": some.body,
            "parent_id": some.parent_id,
            "depth": int(some.depth),
            "distinguished": some.distinguished
        })

    if author in {'AutoModerator', 'WSBVoteBot', 'AnimalFactsBot', 'sukabot', 'crypto_bot', 'the_timezone_bot',
                  'timee_bot', 'rBitcoinMod', 'Ask-Bitcoin',
                  'image_linker_bot', 'demonitize_bot', 'QualityVote',
                  'etherium_bot', 'responseAIbot', 'twitterInfo_bot', 'ThesaurizeThisBot', 'SPACsBot',
                  'NoGoogleAMPBot', 'Satoshi_Symbol', 'BigLebowskiBot', 'TrendingBot',
                  'topredditbot', 'VisualMod', 'haikusbot', 'coinfeeds-bot', 'AmputatorBot', 'Generic_Reddit_Bot'}:
        result['is_bot'] = author

    return result


async def to_rows(submission: Submission):
    cmmts = await submission.comments()
    for comment in await cmmts.list():
        if not isinstance(comment, MoreComments):
            yield to_row(comment, submission.id)

    yield to_row(submission, submission.id)


def not_removed(submission):
    if submission is None:
        return False

    if hasattr(submission, "removed_by_category") and submission.removed_by_category:
        return False

    if hasattr(submission, "is_robot_indexable"):
        return submission.is_robot_indexable

    return True


async def _submission(reddit_session, sub):
    try:
        return await reddit_session.submission(id=sub.id)
    except Exception as e:
        print(f"{sub} exception: {e}")
        return


async def subreddit(names, sort_type="created_utc", sort="asc", after=None, before=None, author=None,
                    progress: tqdm = None) \
        -> AsyncGenerator[Dict, None]:
    async def split_pushapi(val):
        batch, meta = val
        if progress:
            if not progress.total:
                progress.total = meta['total_results']
            progress.set_description( datetime.utcfromtimestamp(meta['after']).strftime('%Y-%m-%d %H:%M:%S') )

        for item in batch:
            yield item

    if isinstance(before, date):
        before = int(time.mktime(before.timetuple()))

    if isinstance(after, date):
        after = int(time.mktime(after.timetuple()))

    # fields = ["id", "is_robot_indexable", "url",
    #           "selftext", "title",
    #           'tickers', "link_flair_text", "created_utc", "author", "author_fullname", "pinned",
    #           "score", "upvote_ratio", "total_awards_received", "gilded", "edited_utc", "num_comments",
    #           "subreddit", "subreddit_id", "no_follow", "removed_by_category", "quarantine"
    #           ]

    NUM_SESSIONS = 5
    reddit_sesstions = itertools.cycle([asyncpraw.Reddit(
        user_agent=f"Comment Extraction (by r/subreddit)",
        client_id=client_id,
        client_secret=client_secret
    )])
    r_sessions_cycle = stream.iterate(reddit_sesstions)

    search_submissions = stream.map(PushshiftAPI().search_submissions(
        # html_decode='true',
        fields=['id', 'created_utc'],
        return_batch=True,
        subreddit=names,
        user_removed='false', mod_removed='false',
        sort=sort, sort_type=sort_type,
        after=after, before=before, author=author, ), split_pushapi) \
                         | pipe.flatten() \
                         | pipe.zip(progress) | pipe.map(lambda x: x[0]) \
                         | pipe.filter(not_removed)

    # search_submissions = stream.merge(*pushshifts)

    subm_stream = stream.map(r_sessions_cycle, _submission, search_submissions, ordered=False, task_limit=NUM_SESSIONS) \
                  | pipe.filter(not_removed)

    return subm_stream \
           | pipe.map(to_rows, ordered=False) \
           | pipe.flatten() \
           | pipe.filter(lambda x: x is not None)


def merge_subreddits(*iters, before=None, after=None, sort_type="sort_type", sort="asc", limit=15000):
    iters = list(subreddit(i, before=before, after=after, sort_type=sort_type, sort=sort) for i in iters)
    while iters:
        for i in iters:
            try:
                yield next(i)
            except StopIteration as e:
                iters.remove(i)

# {'subreddit': 'SPACs', 'num_comments': '>10', 'fields': ['created_utc', 'author', 'url', 'title', 'score'], 'after': 1612137600, 'limit': None, 'memsafe': True, 'size': 100, 'sort': 'desc', 'metadata': 'true', 'before': 1614102415}
# if __name__ == "stream":
#     for submission in reddit.subreddit("wallstreetbets").stream.submissions():
#         print(to_row(submission))
