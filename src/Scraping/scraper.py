from selenium import webdriver
import pandas as pd
import praw
from praw.models import MoreComments
import config


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
headlines_df = pd.DataFrame(headlines, columns=['Title', 'URL'])

# Display the DataFrame
# print(headlines_df)




# Getting page content

urls = headlines_df['URL']
comments_df = pd.DataFrame(columns=["URL", "body"])

for url in urls:
    submission = reddit.submission(url=url)
    posts = []
    for top_level_comment in submission.comments[1:]:
        if isinstance(top_level_comment, MoreComments):
            continue
        if (top_level_comment.body == '[removed]') | (top_level_comment.body == '[deleted]'):
            continue
        posts.append(top_level_comment.body)
    posts_df = pd.DataFrame(posts,columns=["body"])
    posts_df["URL"] = url  # Add a new column with the current URL
    comments_df = pd.concat([comments_df, posts_df], ignore_index=True)
    # print(posts)

# print(comments_df)

# AWS

from pyspark.sql import SparkSession

# Assuming you have Pandas DataFrames: pandas_article_df and pandas_comment_df

# Create a Spark session
spark = SparkSession.builder \
    .appName("Pandas to PySpark") \
    .getOrCreate()

# Convert Pandas DataFrames to PySpark DataFrames
spark_headlines_df = spark.createDataFrame(headlines_df)
spark_comments_df = spark.createDataFrame(comments_df)

# Show the PySpark DataFrames
spark_headlines_df.show()
spark_comments_df.show()

# Perform any PySpark operations on the DataFrames if needed

# Stop the Spark session
spark.stop()
