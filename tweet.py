#! /usr/bin/python
# -*- coding: utf-8 -*-
# sys.path.append("site-packages")
import time

from tweet_event.mypackage.connpass import Connpass
from tweet_event.mypackage.doorkeepr import Doorkeepr
from tweet_event.mypackage.util import  Utility


class main:

    def main(self):

        utility = Utility()
        NSEG = 2391
        GLNAGANO = 2591

        # 時間固定ツイート
        if utility.today.hour == 11 or utility.today.hour == 12:
            post_text= Utility.get_lunch()
            utility.post_tweet(post_text)
        
        if utility.today.hour == 21 or utility.today.hour == 22:
            utility.post_tweet("エンジニアの皆様、そろそろ深夜残業ですよ？？帰りませんか？？")

        # doorkeeper
        if utility.today.year == 2016 and utility.today.month <= 8:
            comm_names = ['nseg','glnagano']
            self.get_doorkeepr(comm_names)

        # connpassからづや会の情報を取得する 日本語部分をエンコードしてバイト型に
        param = {"keyword":"づや会".encode(encoding="utf-8")}
        self.get_zuyakai(param)

        # connpassからnsegとglnagano
        comms = [NSEG,GLNAGANO]
        self.get_connpass(comms)

    def get_doorkeepr(self, comm_names):
        utility = Utility()
        doorkeepr = Doorkeepr()
        # コミュニティの数でループ
        for comm_name in comm_names:
            # 投稿するテキストを取得する
            post_texts = doorkeepr.get_event(comm_name)
            try:
                # イベントの数分投稿する、無ければ抜ける
                if post_texts is None:
                    continue
                for post_text in post_texts:
                    self.tweet(post_text)
                    time.sleep(120.0)
            except Exception as e:
                print(e.args)

    def get_zuyakai(self, param):
        connpass = Connpass()

        post_texts = connpass.get_evant_keyword(param)
        try:
            if post_texts is not None:
                self.tweet(post_texts)
        except Exception as e:
            print(e.args)

    def get_connpass(self, comms):
        connpass = Connpass()
        for comm in comms:
            post_texts = connpass.get_event(comm)

            for post_text in post_texts:
                self.tweet(post_text)

    def tweet(self, post_text):
        utility = Utility()
        utility.post_tweet(post_text)

if __name__ == "__main__":
    main = main()
    main.main()


