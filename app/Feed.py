import re
import urllib.request
import xml.etree.ElementTree as ET


class Feed():

    def __init__(self, url, rawfeed):
        self.url = url
        self.rawfeed = rawfeed

    @staticmethod
    def parse_encoding(xmlstr):
        xmlstr = xmlstr.lower()
        m1 = re.search('encoding\s*=\s*("|\')', xmlstr)
        if m1 is None:
            return 'utf_8'
        else:
            m2 = re.search('"|\'', xmlstr[m1.end():])
            return xmlstr[m1.end():(m1.end() + m2.start())]

    @staticmethod
    def get_raw(proxyurl, url):
        if proxyurl is not None:
            prox_handler = urllib.request.ProxyHandler({'http': proxyurl,
                                                        'https': proxyurl})
            opener = urllib.request.build_opener(prox_handler)
            urllib.request.install_opener(opener)
        response = urllib.request.urlopen(url)
        return response.read()

    def get_channels(self):
        try:
            enc = Feed.parse_encoding(self.rawfeed.decode(errors='ignore'))
            datastr = self.rawfeed.decode(enc)
            root = ET.fromstring(datastr)
            channels = []
            for channel in root.iter('channel'):
                title = channel.find('title').text
                link = channel.find('link').text
                items = []
                for item in root.iter('item'):
                    items.append(Item(item.find('title').text,
                                      item.find('link').text))
                channels.append(Channel(title, link, items))
            return channels
        except Exception as e:
            print('Feed.get_channels() failed for {}'.format(self.url))
            print(e)
            return []


class Channel():

    def __init__(self, title, link, items):
        self.title = title
        self.link = link
        self.items = items


class Item():

    def __init__(self, title, link):
        self.title = title
        self.link = link
