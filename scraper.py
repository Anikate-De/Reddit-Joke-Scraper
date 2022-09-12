import ctypes
import json
import os

import praw
from dotenv import load_dotenv
from termcolor import colored


def loadDataFromJSON():

    global jsonData

    path = 'data/data.json'

    # create a directory and a data file if it does not exist
    if (not os.path.exists(path)):
        try:
            os.mkdir('data')
        except:
            pass
        file = open(path, 'w')
        file.close()
        loadDataFromJSON()
        return
    else:
        file = open(path, 'r+')
        if not len(file.read()) > 0:
            file.write('[]')
            file.close()
            loadDataFromJSON()
            return

    file.seek(0)
    jsonData = json.load(file)
    file.close()
    print(colored('Loaded Data Modules', color='green'))


def loadDataFromSkipped():

    global skippedData

    path = 'data/skipped.txt'

    # create a directory and a data file if it does not exist
    if (not os.path.exists(path)):
        try:
            os.mkdir('data')
        except:
            pass
        file = open(path, 'w')
        file.close()
        loadDataFromSkipped()
        return
    else:
        file = open(path, 'r+')

    file.seek(0)
    skippedData = file.read().splitlines()
    file.close()
    print(colored('Loaded Skipped Data Modules', color='green'))


def displayIntroductoryMSG():
    print(colored('\nREDDIT JOKE SCRAPER\n', color='red', attrs=['bold']))

    print('Current Joke Save type -',
          colored('Two-line (Setup & Punchline)', color="cyan"))
    print('Current Data Save Type <Saved Jokes, Skipped Jokes>',
          colored('<JSON, TXT>', color="cyan"))
    print()

    print(colored('\nHow to Use - \n', color='yellow', attrs=['bold']))

    print('Use the following keys to operate this tool -')
    print(colored('a', color='green', attrs=[
          'bold']), 'Add after editing tags')
    print(colored('A', color='green', attrs=[
          'bold']), 'Forced Add (no editing)')
    print(colored('e or E', color='green', attrs=[
          'bold']), 'Add after editing content (tags + title + desc)')
    print(colored('s or S', color='green', attrs=['bold']), 'Skip')
    print(colored('q or Q', color='green', attrs=['bold']), 'Save Data & Quit')

    print()
    print(colored('\nPLEASE DON\'T HIT CTRL+C TO EXIT OUT OF THIS PROGRAM. IT WON\'T SAVE THE SESSION\'S DATA. USE THE Q KEY\n',
          color='red', attrs=['bold']))
    print('It is recommended to not extend any session beyond 100 jokes without saving the data. Do a quit and restart\n')

    input(colored('Press ENTER | RETURN to continue ', color="cyan"))
    print()
    print(colored('--------------------', color="yellow"))
    print()


def removePrevLn(n=1):
    for i in range(n):
        print('\033[1A' + '\033[K', end='')


def editTags():
    return {
        "flags": {
            "religious": input('Religious: (False) ') != "",
            "sexist": input('Sexist: (False) ') != "",
            "racist": input('Racist: (False) ') != "",
            "explicit": input('Explicit: (False) ') != "",
            "political": input('Political: (False) ') != "",
            "nsfw": input('NSFW: (False) ') != ""
        },
        "safe": input('SAFE: (true) ') == ""
    }


def loopThroughSubmissions(dataList, skippedList):
    for submission in submissions:

        if submission.id in skippedList:
            continue

        for obj in dataList:
            if obj['rID'] == submission.id:
                break
        else:
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

                match choice:
                    case 'q' | 'Q':
                        choice = input(
                            f'The data will be saved, confirm quit? {colored(text="[y/n]", color="yellow", attrs=["bold"])} ')
                        if choice.lower() == 'y':
                            print('Saving, please wait...')

                            id = 1
                            for obj in dataList:
                                obj['id'] = id
                                id += 1

                            # Execute saving logic here
                            with open('data/data.json', 'w') as file:
                                json.dump(dataList, file,
                                          indent=4, sort_keys=True)

                            with open('data/skipped.txt', 'w') as skipped:
                                skipped.write('\n'.join(skippedList) + '\n')

                            removePrevLn(2)
                            print(colored(text='Saved',
                                          color='green', attrs=['bold']))
                            return

                    # Lets the user add the joke to the save-list
                    case 'A':

                        # Execute addition logic here
                        dataList += [{
                            "rID": submission.id,
                            "setup": submission.title,
                            "punchline": submission.selftext,
                            "flags": {
                                "religious": False,
                                "sexist": False,
                                "racist": False,
                                "explicit": False,
                                "political": False,
                                "nsfw": False
                            },
                            "safe": True
                        }]

                        print(colored(text='Added',
                                      color='green', attrs=['bold']))
                        print()
                        break

                    # Lets the user add a joke after editing tags [only]
                    case 'a':
                        print(
                            'Edit the tags below, their default values are present in parenthesis - ')
                        dataList += [
                            {
                                "rID": submission.id,
                                "setup": submission.title,
                                "punchline": submission.selftext,
                            } | editTags()
                        ]
                        print()
                        print(colored(text='Added with custom tags',
                                      color='green', attrs=['bold']))
                        print()
                        break
                    case 'e' | 'E':
                        print(
                            'Edit the joke below, their default values, if available, are present in parenthesis - ')
                        setup = input('Setup: (Default Title) ')
                        punchline = input('Punchline: (Default Desc) ')
                        dataList += [
                            {
                                "rID": submission.id,
                                "setup": submission.title if setup == '' else setup,
                                "punchline": submission.selftext if punchline == '' else punchline,
                            } | editTags()
                        ]
                        print()
                        print(colored(text='Edited',
                                      color='yellow', attrs=['bold']))
                        print()
                        break
                    case 's' | 'S':
                        skippedList += [submission.id]
                        print('Skipped')
                        print()
                        break
                    case _:
                        print(
                            colored(text="Invalid input, please enter one of (A, a, e, s, q)", color="red"))


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


jsonData = []
skippedData = []

loadDataFromJSON()
loadDataFromSkipped()

displayIntroductoryMSG()

loopThroughSubmissions(jsonData, skippedData)
