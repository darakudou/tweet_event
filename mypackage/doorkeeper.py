# -*- coding: utf-8 -*-
import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re


def get_event_doorkeepr(comm_name):
    url = urllib.request.urlopen("https://"+comm_name+".doorkeeper.jp/events/upcoming")
    soup = BeautifulSoup(url)

    # イベントのurlを取得
    all_url = get_url(soup,comm_name)
    if all_url is None:
        return all_url
    # urlの一覧からtwitterリンクを読み込む
    tweet_shares = get_tweetlink(all_url)

    # まとめて送り返す
    return tweet_shares

def get_url(soup,comm_name):
    """urlの一覧を取得"""
    all_events = soup.find_all("h3")
    # 正規表現で取得
    pattern = str("https://"+comm_name+".doorkeeper.jp/events/\d*")
    comp_pattern = re.compile(pattern)
    urls = []
    for event in all_events:
        url = comp_pattern.findall(str(event))
        if url is not None:
            urls.extend(url)

    return urls

def get_tweetlink(all_url):
    # 開催前urlの一覧からtwitter投稿用イベントの一覧を取得する
    tweet_shares = []
    for eventurl in all_url:
        url = urllib.request.urlopen(eventurl)
        soup = BeautifulSoup(url)
        link = soup.find("a",{"href":"http://twitter.com/share"})
        title = link.get("data-text")
        url = link.get("data-url")
        tweet_shares.append(str(title)+"\n"+str(url))

    return tweet_shares