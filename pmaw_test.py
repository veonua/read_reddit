from psaw.psaw import PushshiftAPI

api = PushshiftAPI()
post_ids = ['lpukyd']
posts = api.search_submissions(subreddit='SPACs', num_comments=">10",
                               fields=['created_utc', 'author', 'url', 'title', 'score'], after=1612137600, limit=None,
                               memsafe=True)
# posts = list(posts)

for i in range(1, 100):
    po = next(posts)
    print(f"{i}: {po.title}")
import pandas as pd

# df = pd.DataFrame.from_dict(posts)

# df.sort_values('score', ascending=False, inplace=True)
print(api.metadata)
