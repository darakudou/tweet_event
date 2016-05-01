#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import datetime, twython, platform
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import time
import configparser



def main():

    comm_names = ['nseg','glnagano']
	#開催前のイベントの情報を抜き出す
    for comm_name in comm_names:
        post_text = get_event(comm_name)
        print (post_text)
		try:
			for i in post_text:
				print(i)
				post_tweet("【自動投稿】" +str(i))
				time.sleep(120.0)
		except:
			print("err!")


def get_event(comm_name):
	#glnaganoのイベント情報を取得,ついでにnsegさんも
	url = urllib2.urlopen("https://"+comm_name+".doorkeeper.jp/events/upcoming")

	soup = BeautifulSoup(url)

	#タイトルの一覧
	#all_title = get_title(soup)
	#urlの一覧
	all_url = get_url(soup,comm_name)
	#urlの一覧からリンク先のtwitterリンクを読み込んでそれを投稿
	tweet_shares = get_tweetlink(all_url)

	#イベント日時の一覧
	#all_date = get_date(soup)
	#イベント場所の一覧
	#all_places = get_place(soup)

	#まとめて送り返す
	return tweet_shares
	#return all_title,all_url,all_date,all_places

#タイトルの一覧を
def get_title(soup):
	all = soup.find_all('h3')

	titles = []
	for title in all:
		span =title.find('span')
		if span is not None:
			titles.append(span.string) #extendにすると１文字ずつになってしまう？？

	return titles

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

#イベント日時を取得
def get_date(soup):
	all_date = soup.find_all("time")
	dates = []
	for date in all_date:
		if date is not None:
			dates.append(date.string)
	return dates

#イベント場所を取得
def get_place(soup):
	all_place = soup.find_all("span",itemprop='name')
	places = []
	for place in all_place:
		if place is not None:
			places.append(place.string)
	return places	

def edit_post(titles,urls,dates,place):
	#編集する
	post_text = []
	for x in range(len(titles)):
		post_text.append("自動投稿テスト:"+str(titles[x])+"\n"+str(urls[x])+"\n"+str(dates[x])+"\n"+str(place[x]))

	return post_text

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


