#! /usr/bin/python
# -*- coding: utf-8 -*-
from twitter import *
import configparser

def main():
    # twitter投稿用アクセスキーとか
    inifile = configparser.ConfigParser()
    inifile.read("./settings.ini")
    CONSUMER_KEY    = str(inifile.get("twitter","CONSUMER_KEY")).strip()
    CONSUMER_SECRET = str(inifile.get("twitter","CONSUMER_SECRET")).strip()
    ACCESS_KEY      = str(inifile.get("twitter","ACCESS_KEY")).strip()
    ACCESS_SECRET   = str(inifile.get("twitter","ACCESS_SECRET")).strip()

    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    auth = OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_stream = TwitterStream(auth=auth, domain="glnagano.twitter.com")
    for msg in twitter_stream.user():
        if "in_reply_to_screen_name" in msg and "text" in msg:
            if msg["in_reply_to_screen_name"] == "kasajei":
                print (msg["text"])

if __name__ == "__main__":
    main()