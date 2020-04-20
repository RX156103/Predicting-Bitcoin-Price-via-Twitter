#reference
# https://towardsdatascience.com/extracting-twitter-data-pre-processing-and-sentiment-analysis-using-python-3-0-7192bd8b47cf
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/


import numpy as np # used for handling numbers
import pandas as pd # used for handling the dataset
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import re #regular expression
import string
import emoji
import tweepy
from textblob import TextBlob

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

def extract_emojis(tweet):
    str_emoji = ','.join([c for c in tweet if c in emoji.UNICODE_EMOJI])
    return str_emoji


def extract_hashtag(tweet):
    '''
    https://stackoverflow.com/questions/2527892/parsing-a-tweet-to-extract-hashtags-into-an-array/20614981#20614981
    :param tweet: tweet text
    :return: hashtag list
    '''
    hashtag = re.findall(r'\B#\w*[a-zA-Z]+\w*', tweet)
    str_hash = ','.join([str(elem) for elem in hashtag])
    return str_hash

def clean_tweets_one(tweet):
    clean_text = p.clean(tweet)
    return clean_text


def clean_tweets_two(tweet):
    '''
    Removing stop words with NLTK in Python.
    https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    :param tweet: original tweet
    :return: cleaned tweet
    '''
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
    # after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
    # filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
    # looping through conditions
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(str(w))
    return ' '.join(filtered_tweet)


def get_tweet_sentiment(tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


def main():
    data = pd.read_csv('tweets_original.csv', sep = ';')
    data_tweet = data[data.columns[8]]
    data = data.drop(columns='text')
    list_emoji = []
    list_hash_tag = []
    cleaned_tweet = []
    list_sentiment = []
    for tweet in data_tweet:
        hashtag = extract_hashtag(tweet)
        list_hash_tag.append(hashtag)
        emojis = extract_emojis(tweet)
        list_emoji.append(emojis)
        clean1 = clean_tweets_one(tweet)
        clean2 = clean_tweets_two(clean1)
        cleaned_tweet.append(clean2)
        sentiment = get_tweet_sentiment(clean2)
        list_sentiment.append(sentiment)
    data["text"] = cleaned_tweet
    data["hash tag"] = list_hash_tag
    data["emoji"] = list_emoji
    data["sentiment"] = list_sentiment
    data.to_csv("preprocessing_tweet_with_sentiment.csv", sep=';')
    print("done")
main()