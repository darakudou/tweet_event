# -*- coding: utf-8 -*-
import random
import configparser
import datetime, twython, platform
import pytz


def get_now_date():
   return datetime.datetime.now(pytz.timezone('Asia/Tokyo'))


def get_lunch():
    # 1時間に一回呟くのでランダムで何か言う
    food_list = ['\U0001F354','\U0001F355',
                 '\U0001F35A','\U0001F35B',
                 '\U0001F35C','\U0001F35D',
                 '\U0001F363','\U0001F371',
                 '\U0001F372','\U0001F37C',
                 '\U0001F40B','\U0001F40C',
                 '\U0001F37A','\U0001F419']

    return u"今日のお昼は"+random.choice(food_list)+u"にしよう！"


def post_tweet(post_text):
    inifile = configparser.ConfigParser()
    inifile.read("./settings.ini")

    # twitter投稿用アクセスキーとか
    CONSUMER_KEY    = str(inifile.get("twitter","CONSUMER_KEY")).strip()
    CONSUMER_SECRET = str(inifile.get("twitter","CONSUMER_SECRET")).strip()
    ACCESS_KEY      = str(inifile.get("twitter","ACCESS_KEY")).strip()
    ACCESS_SECRET   = str(inifile.get("twitter","ACCESS_SECRET")).strip()
    # twitterで投稿するときに有効化
    api = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

    try:
        api.update_status(status=post_text)
    except twython.TwythonError as e:
        print (e.args)
