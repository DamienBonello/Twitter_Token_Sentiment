# TO DO-
# Scrape Relevant data from Mintscan / Any other source
# Create local files to track history of Bond etc.
# With Prices - make use of SMAs, Bollinger etc. - Determine price.

# Gather tweets from Twitter

import tweepy
import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAANHYYgEAAAAAmwzvNgx0Jbig4S0acgZipUvVVgk%3DVLoSaMdUaHXjV0YwZ3MH5S3DvmEHdTeWb"
                       "VVOoQRNHhGtdPagdI")

name = input("What Token do you wish to analyse? ")
query = f"#{name} lang:en -is:retweet"

tweet_info_ls = []

for tweet in tweepy.Paginator(client.search_recent_tweets, query, tweet_fields=["public_metrics"],
                              expansions='author_id', max_results=100).flatten(limit=1000):
    if tweet.public_metrics['like_count'] > 1:
        tweet_info = {
            'Tweet': tweet.text,
            'Likes': tweet.public_metrics['like_count'],
            'RTs': tweet.public_metrics['retweet_count'],
            'Vader Subjectivity': sia.polarity_scores(tweet.text),
            'Subjectivity': round(TextBlob(tweet.text).sentiment.subjectivity, 5),
            'Polarity': round(TextBlob(tweet.text).sentiment.polarity, 5),
        }

        tweet_info_ls.append(tweet_info)

# create dataframe from the extracted records
tweets_df = pd.DataFrame(tweet_info_ls)
pd.set_option("colheader_justify", "center")

# Build simple sentiment analysis
Weighted_Polarity = round(tweets_df['Polarity'].sum() / len(tweet_info_ls), 5)
Weighted_Subjectivity = round(tweets_df['Subjectivity'].sum() / len(tweet_info_ls), 5)
table = tweets_df.to_html(index=True, classes='mystyle')

if Weighted_Polarity == 1 > 0.5:
    Polarity = "Positive"
else:
    Polarity = "Negative"

if Weighted_Subjectivity == 1 > 0.5:
    Subjectivity = "Biased"
else:
    Subjectivity = "Not so Biased"

html_string = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
  <div class='test'>
    <h1>Polarity: {Weighted_Polarity} - {Polarity}</h1>
  </div>
  <div class='test'>
    <h1>Subjectivity: {Weighted_Subjectivity} - {Subjectivity}</h1>
  </div>
    {table}
  </body>
</html>
'''.format(**locals())

# # OUTPUT AN HTML FILE
with open('tweets.html', 'w', encoding="utf-8") as f:
    f.write(html_string)
