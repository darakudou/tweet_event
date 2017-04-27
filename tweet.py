# -*- coding: utf-8 -*-
from mypackage.util import get_now_date, post_tweet, get_lunch
from mypackage.doorkeeper import get_event_doorkeepr
from mypackage.connpass import get_evant_connpass, get_evant_connpass_keyword, get_event_connpass_id
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

    post_texts = []
    for comm in comms:
        post_texts.append(get_evant_connpass(comm, today))

    # イベントのIDでツイート
    event_ids = [55693, 55694,]
    post_texts.append(get_event_connpass_id(today, event_ids))

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
        post_tweet("にゃーん(社会性フィルター)")
if __name__ == "__main__":
    main()
