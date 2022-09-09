import os

import praw
from dotenv import load_dotenv

load_dotenv()

# Get env var by using - os.getenv('ENV NAME')

reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv(
                         'CLIENT_SECRET'),
                     user_agent=os.getenv('USERAGENT'),
                     username=os.getenv('USERNAME'),
                     redirect_uri=os.getenv('REDIRECT_URL'),
                     password=os.getenv('PASSWORD'))

print(reddit.auth.url(scopes=["identity"], state="...", duration="permanent"))

reddit.read_only = True

while True:

    submissions = reddit.subreddit('DadJokes').top(limit = float('inf'))

    for submission in submissions:
        print(submission.title)
        print(submission.selftext)
        print()

        print('NSFW', submission.over_18)
        print('Upvotes', submission.score)
        print('ID', submission.id)
        print()

        input('Enter to get to next joke _')
