# -*- coding: utf-8 -*-
from mypackage.util import get_now_date, post_tweet, get_lunch
from mypackage.doorkeeper import get_event_doorkeepr
from mypackage.connpass import get_evant_connpass, get_evant_connpass_keyword
import time
today = get_now_date()

def main():


    NSEG = 2391
    GLNAGANO = 2591

    static_post(today.hour)

    # doorkeeper
    if today.year == 2016 and today.month <= 8:
        comm_names = ['nseg','glnagano']
        get_doorkeepr(comm_names)

    # connpassからづや会の情報を取得する 日本語部分をエンコードしてバイト型に
    param = {"keyword":"づや会".encode(encoding="utf-8")}
    get_zuyakai(param)

    # connpassからnsegとglnagano
    comms = [NSEG,GLNAGANO]
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
                print(post_text)
                post_tweet(post_text)
                time.sleep(30.0)
        except Exception as e:
            print(e.args)

def get_zuyakai(param):

    post_texts = get_evant_connpass_keyword(param, today)
    try:
        if post_texts is not None:
            print(post_texts)
            post_tweet(post_texts)
    except Exception as e:
        print(e.args)

def get_connpass(comms):

    for comm in comms:
        post_texts = get_evant_connpass(comm, today)

        for post_text in post_texts:
            print(post_text)
            post_tweet(post_text)
            time.sleep(30.0)

def static_post(hour):
    # 時間固定ツイート
    if hour == 11 or hour == 12:
        post_text= get_lunch()
        print (post_text)
        post_tweet(post_text)

    elif hour == 21 or hour == 22:
        post_tweet("エンジニアの皆様、そろそろ深夜残業ですよ？？帰りませんか？？")

    else:
        post_tweet("ギークラボ長野ではイベント開催したいという方！ふらっと訪れてみたい方をお待ちしてます！")



if __name__ == "__main__":
    main()


