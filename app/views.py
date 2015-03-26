from flask import render_template
from app import app
from config import FEEDS, PROXY
from .Feed import Feed


@app.route('/')
def home():
    channels = []
    for l in FEEDS:
        feed = Feed(l, PROXY)
        channels.extend(feed.get_channels())
    return render_template('feeds.html', channels=channels)
