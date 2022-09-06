import os
from dotenv import load_dotenv
import praw

load_dotenv()

# Get env var by using -
# os.getenv('ENV NAME')

reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),      # your client id
                     client_secret=os.getenv(
                         'CLIENT_SECRET'),  # your client secret
                     user_agent=os.getenv('USERAGENT'),  # user agent name
                     username=os.getenv('USERNAME'),
                     redirect_uri="http://localhost:8080",    # your reddit username
                     password=os.getenv('PASSWORD'))

print(reddit.auth.url(scopes=["identity"], state="...", duration="permanent"))

reddit.read_only = True

submission = reddit.subreddit('DadJokes').random()

print(submission.title)
print(submission.selftext)
