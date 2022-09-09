import ctypes
import os

import praw
from dotenv import load_dotenv
from termcolor import colored


def removePrevLn(n=1):
    for i in range(n):
        print('\033[1A' + '\033[K', end='')


def loopThroughSubmissions():
    for submission in submissions:

        if submission.over_18:
            print('\n', colored(text='NSFW', color='red',
                                attrs=['bold']), sep='', end='\n\n')

        print(colored(text='Title:', color='yellow'), colored(
            text=submission.title, attrs=['bold']), end='\n\n')
        print(colored(text='Desc:', color='yellow'),
              submission.selftext, end='\n\n')

        print('Upvotes:', colored(text=submission.score, color='green'))
        print('ID', submission.id, end='\n\n\n')

        while True:

            choice = input(colored(text='waiting for input... ',
                                   color='cyan', attrs=['bold']))

            # Remove the input line with the below ANSI codes
            removePrevLn(2)

            match choice.lower():
                case 'q':
                    choice = input(
                        f'The data will be saved, confirm quit? {colored(text="[y/n]", color="yellow", attrs=["bold"])} ')
                    if choice.lower() == 'y':
                        print('Saving, please wait...')
                        # Execute saving logic here
                        removePrevLn(2)
                        print(colored(text='Saved',
                              color='green', attrs=['bold']))
                        return
                case 'a':
                    # Execute addition logic here
                    print('Added')
                    print()
                    break
                case 'e':
                    # Add editing logic here
                    print('Edited')
                    print()
                    break
                case _:
                    print(
                        colored(text="Invalid input, please enter one of the following (a, e, q)", color="red"))


# Use ctypes to enable ANSI codes in a terminal
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

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

# Lazy-load all submissions in the subreddit
submissions = reddit.subreddit('DadJokes').top(limit=float('inf'))

loopThroughSubmissions()
