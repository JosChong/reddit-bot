import os
import praw
import re
import time
from praw.models import Comment

def analyze(text):
    text = re.sub(r'[^a-zA-Z0-9-_\s\']', '', text)
    words = text.lower().split()
    unique_words = set(words)
    word_counts = dict()

    for word in unique_words:
        word_count = words.count(word)
        word_counts[word] = word_count

    # list of words ordered by frequency
    reply = 'Here are the words ordered by their frequency of use:\n\nWord|Count\n:--|:--'
    for key, value in sorted(word_counts.items(), key = lambda x: x[1], reverse = True):
        reply += '\n' + key + '|' + str(value)

    # word cloud generated using the following tools:
    # amueller's Python word cloud generator @ https://github.com/amueller/word_cloud
    # iambibhas's Python Imgur image uploader @ https://gist.github.com/iambibhas/6855102
    f = open('words.txt', 'w+')
    f.write(text)
    f.close()

    os.system('wordcloud_cli.py --text words.txt --imagefile wordcloud.png')
    os.system('python3 imgur.py wordcloud.png')

    f = open('link.txt', 'r')
    link = f.read()
    f.close()

    os.remove('words.txt')
    os.remove('wordcloud.png')
    os.remove('link.txt')

    reply+= '\n\n[A word cloud generated using the words above.](' + link + ')'

    return reply

def authenticate():
    print('Authenticating...')
    reddit = praw.Reddit('WordCounter_Bot', user_agent = 'WordCounter_Bot v1.0')
    print('Authenticated as {}'.format(reddit.user.me()))

    return reddit

def run_bot(reddit, comments_replied_to):
    check = '!countwords'
    check_limit = 25

    print('Checking {} comment(s)...'.format(check_limit))
    for comment in reddit.subreddit('test').comments(limit = check_limit):
        if check == comment.body and comment.id not in comments_replied_to:# and comment.author != reddit.user.me():
            print('\'{0}\' found in {1}'.format(check, comment.id))

            parent = comment.parent()
            if isinstance(parent, Comment):
                comment_reply = analyze(parent.body)
            else:
                comment_reply = analyze(parent.selftext)
            comment.reply(comment_reply)
            print('Replied to comment {}'.format(comment.id))

            comments_replied_to.append(comment.id)
            with open('comments_replied_to.txt', 'a') as f:
                f.write(comment.id + '\n')
    print('Sleeping for 10 seconds...')
    time.sleep(10)

def load_comments_replied_to():
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
    else:
        with open('comments_replied_to.txt', 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split('\n')
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to

def main():
    reddit = authenticate()
    comments_replied_to = load_comments_replied_to()

    while True:
        run_bot(reddit, comments_replied_to)

if __name__ == '__main__':
    main()
