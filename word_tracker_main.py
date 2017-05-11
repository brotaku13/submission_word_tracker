import config
import praw
from collections import Counter



def login():
    """
    creates a reddit instance. id, client secret etc are private information and therefore not uploaded to github.
    Param: none
    return: reddit instance as r
    """
    print('logging in...')
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent=config.user_agent,
                    username=config.username,
                    password=config.password)
    print('logged in!')
    return r



def search_bill_gates(r):
    """
    used when wanting to search a specific subreddit for a specific subject and user
    param: reddit instance
    returns a list of comment ID's
    """


    ama_post_list = []

    # for post in a given subreddit (IAmA) search the subreddit for posts with the word 'Bill Gates'.
    # if the post author is 'thisisbillgates', append the post ID to a list and return it
    for post in r.subreddit('IAmA').search('bill gates', sort='relevance', syntax='cloudsearch', time_filter='all'):
        if post.author.name == 'thisisbillgates':
            ama_post_list.append(post.id)

    return ama_post_list

def user_words(r, username):
    """
    parses though words in the profile of a users post history and creates and edits a txt file of all words in last 1000 posts
    param: reddit instance, given username
    returns void
    """

    # collects words from all comments (last 1000?) and puts them in a text file
    with open("{} comments.txt".format(username), 'w', encoding='utf-8') as f:
        comment_count=0
        for comment in r.redditor(username).comments.new(limit=None):
            try:
                comment_count += 1
                if comment.body == '[removed]' or comment.body == '[deleted]':
                    continue
                else:
                    f.write(comment.body)
            except UnicodeDecodeError:
                pass
    print('number of comments parsed: ', comment_count)
    f.close()



def word_count(username):
    """
    opens a txt file and processes the each post into a list of words.
    counts words and prints out most used words (in this case, top 50)
    param: reddit instance, given username
    returns void
    """

    f = open("{} comments.txt".format(username), 'r')
    filetext = f.read()
    # replaces
    word_list = filetext.split()

    for i in range(len(word_list)):
        if word_list[i].startswith('[') and word_list[i].endswith(')'):
            continue
        elif word_list[i][0] in '!?.,"[@#$%^&*()\':;':
            word_list[i] = word_list[i].replace(word_list[i], word_list[i][1:len(word_list[i]) - 1])
        elif word_list[i][-1] in '!?.,"]@#$%^&*()\':;':
            word_list[i] = word_list[i].replace(word_list[i], word_list[i][0:len(word_list[i])-2])

    long_word_list = [word for word in word_list if len(word) > 7]

    word_count = Counter(long_word_list)
    print("Most common")
    for key, value in word_count.most_common(50):
        print('{} : {}'.format(key, value))






def main():
    r = login()
    user = 'brotaku13'
    #bg_post_list = search_bill_gates(r)
    user_words(r, user)
    word_count(user)




main()