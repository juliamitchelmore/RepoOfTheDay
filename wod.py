from wordnik import *
from github import Github
import tweepy, time, os

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

wordnikApiUrl = 'http://api.wordnik.com/v4'
wordnikApiKey = os.environ['WORDNIK_API_KEY']
client = swagger.ApiClient(wordnikApiKey, wordnikApiUrl)

wordsApi = WordsApi.WordsApi(client)

g = Github(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_KEY'])

def find_repo(wordOfDay):
    found_repo = ""
    for repo in g.search_repositories(wordOfDay):
        if wordOfDay.lower() in repo.name.lower():
            found_repo = repo
            break

    if found_repo:
      return "The word of the day is '" + wordOfDay + "'. Github repo: " + found_repo.name + " by " + found_repo.owner.login + " " + found_repo.html_url
    else:
      return "No repo exists for '" + wordOfDay + "'! Maybe you should make one?"


while True:
    wordOfDay = wordsApi.getWordOfTheDay().word
    currentStatus = api.user_timeline(count=1)[0]

    if "'{}'".format(wordOfDay) not in currentStatus.text:
        tweet = find_repo(wordOfDay)
        api.update_status(tweet)
        time.sleep(86400)
    else:
        time.sleep(43200)
