# -*- coding: utf-8 -*-
from mypackage.util import get_now_date, post_tweet, get_lunch
from mypackage.doorkeeper import get_event_doorkeepr
from mypackage.connpass import get_evant_connpass, get_evant_connpass_keyword
import time
today = get_now_date()

def main():


    NSEG = 2391
    GLNAGANO = 2591
    LIG = 991

    static_post(today.hour)

    # doorkeeper
    if today.year == 2016 and today.month <= 8:
        comm_names = ['nseg','glnagano']
        get_doorkeepr(comm_names)

    # connpassからづや会の情報を取得する 日本語部分をエンコードしてバイト型に
    # param = {"keyword":"づや会".encode(encoding="utf-8")}
    # get_zuyakai(param)

    # connpassからnsegとglnagano
    comms = [NSEG, GLNAGANO, LIG]
    try:
        get_connpass(comms)
    except Exception as e:
        print(e.args)

def get_doorkeepr(comm_names):

    # コミュニティの数でループ
    for comm_name in comm_names:
        # 投稿するテキストを取得する
        post_texts = get_event_doorkeepr(comm_name)
        try:
            # イベントの数分投稿する、無ければ抜ける
            if post_texts is None:
                continue
            for post_text in post_texts:
                post_tweet(post_text)
                time.sleep(30.0)
        except Exception as e:
            print(e.args)

def get_zuyakai(param):

    post_texts = get_evant_connpass_keyword(param, today)
    try:
        if post_texts is not None:
            post_tweet(post_texts)
    except Exception as e:
        print(e.args)

def get_connpass(comms):

    for comm in comms:
        post_texts = get_evant_connpass(comm, today)

        for post_text in post_texts:
            post_tweet(post_text)
            time.sleep(10.0)

def static_post(hour):
    # 時間固定ツイート
    if hour == 11 or hour == 12:
        post_text= get_lunch()
        post_tweet(post_text)

    elif hour == 21 or hour == 22:
        post_tweet("1日8時間睡眠のためにも寝る準備をしましょう！")

    else:
        post_tweet("みんなのPython勉強会 in 長野(03月18日) #1 https://startpython.connpass.com/event/48846/ #stapy #glnagano")
        post_tweet("【アンケートにご協力お願いいたします】 - GEEKLAB.NAGANOの活動の振り返り、今後のさらなる向上に当たり、アンケートにご協力頂けたら幸いです！ http://geeklab-nagano.com/post/157047930952/%E3%82%A2%E3%83%B3%E3%82%B1%E3%83%BC%E3%83%88%E3%81%AB%E3%81%94%E5%8D%94%E5%8A%9B%E3%81%8A%E9%A1%98%E3%81%84%E3%81%84%E3%81%9F%E3%81%97%E3%81%BE%E3%81%99")
        post_tweet("【3月4日(土)開催：プログラミング「わくわく」探検隊】【長野県長野市会場】【対象：小学3年から6年】 https://sites.google.com/myjuen.jp/codedu-ws/")
if __name__ == "__main__":
    main()


