#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  
sys.path.append("site-packages")
 
import datetime, twython, platform
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import time
import configparser

def main():

    comm_names = ['nseg','glnagano']
    #コミュニティの数でループ
    for comm_name in comm_names:
    	#投稿するテキストを取得する
        post_texts = get_event(comm_name)
        try:
            #イベントの数分投稿する、無ければ抜ける
            if post_texts is None:
                continue
            for post_text in post_texts:
                post_tweet(str(post_text))
                time.sleep(120.0)
        except Exception as e:
            print('---- print works ---')
            print(e.message)
            print('----------print end-')


def get_event(comm_name):
	#glnaganoのイベント情報を取得,ついでにnsegさんも
	url = urllib2.urlopen("https://"+comm_name+".doorkeeper.jp/events/upcoming")

	soup = BeautifulSoup(url)

	#イベント投稿用urlの一覧を取得
	all_url = get_url(soup,comm_name)
	if all_url is None:
		return all_url
	#urlの一覧からtwitterリンクを読み込む
	tweet_shares = get_tweetlink(all_url)

	#まとめて送り返す
	return tweet_shares

#urlの一覧を取得
def get_url(soup,comm_name):
	all_events = soup.find_all("h3")
	#正規表現で取得
	pattern = str("https://"+comm_name+".doorkeeper.jp/events/\d*")
	comp_pattern = re.compile(pattern)
	urls = []
	for event in all_events:
		url = comp_pattern.findall(str(event))
		if url is not None:
			urls.extend(url)

	return urls

def get_tweetlink(all_url):
	#開催前urlの一覧からtwitter投稿用イベントの一覧を取得する
	tweet_shares = []
	for eventurl in all_url:
		url = urllib2.urlopen(eventurl)
		soup = BeautifulSoup(url)
		link = soup.find("a",{"href":"http://twitter.com/share"})
		title = link.get("data-text")
		url = link.get("data-url")
		tweet_shares.append(str(title)+"\n"+str(url))

	return tweet_shares

def post_tweet(post_text):
    inifile = configparser.SafeConfigParser()
    inifile.read("./settings.ini")

    #twitter投稿用アクセスキーとか 
    CONSUMER_KEY    = str(inifile.get("twitter","CONSUMER_KEY")).strip()
    CONSUMER_SECRET = str(inifile.get("twitter","CONSUMER_SECRET")).strip()
    ACCESS_KEY      = str(inifile.get("twitter","ACCESS_KEY")).strip()
    ACCESS_SECRET   = str(inifile.get("twitter","ACCESS_SECRET")).strip()
    #twitterで投稿するときに有効化
    api = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

    try:
        api.update_status(status=post_text)
    except twython.TwythonError as e:
        print (e)


if __name__ == "__main__":
    main()


