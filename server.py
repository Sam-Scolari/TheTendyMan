from flask import Flask
from Crawlers import reddit, yahoo

app = Flask(__name__)

@app.route('/')
def root():
    return 'root'

@app.route('/reddit/<subreddit>')
def fetch_reddit(subreddit):
    return reddit.fetch(subreddit)

@app.route('/yahoo/<ticker>')
def fetch_yahoo(ticker):
    return yahoo.fetch(ticker)

