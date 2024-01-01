from selenium import webdriver
import pandas as pd
import praw
from praw.models import MoreComments
import config.py


# Scraping with PRAW

reddit = praw.Reddit (
client_id=config.REDDIT_CLIENT_ID,
client_secret=config.REDDIT_CLIENT_SECRET,
user_agent=config.REDDIT_USER_AGENT
)

headlines = set()
for submission in reddit.subreddit('SkincareAddiction').hot(limit=5):
    headlines.add((submission.title, "https://www.reddit.com" + submission.permalink))

# Convert set of tuples to Pandas DataFrame
df = pd.DataFrame(headlines, columns=['Title', 'URL'])

# Display the DataFrame
print(df)




# Getting page content

urls = df['URL']
print(urls[2])
url = urls[2]

for url in urls:
    submission = reddit.submission(url=url)
    posts = []
    for top_level_comment in submission.comments[1:]:
        if isinstance(top_level_comment, MoreComments):
            continue
        if (top_level_comment.body == '[removed]') | (top_level_comment.body == '[deleted]'):
            continue
        posts.append(top_level_comment.body)
    posts = pd.DataFrame(posts,columns=["body"])
    print(posts)
