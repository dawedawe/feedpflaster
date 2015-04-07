import concurrent.futures
from flask import render_template
from app import app
from config import FEEDS, PROXY
from .Feed import Feed


@app.route('/')
def home():
    channels = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(Feed.get_raw, PROXY, url):
                         url for url in FEEDS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result(60)
                feed = Feed(url, data)
                channels.extend(feed.get_channels())
            except Exception as exc:
                print('fetching feed data failed for {} with {}'.format(url,
                                                                        exc))
    return render_template('feeds.html', channels=channels)
