# -*- coding: utf-8 -*-
import json
import urllib
import urllib.parse
import urllib.request
import dateutil.parser
import datetime, pytz


def get_evant_connpass_keyword(param, today):
    try:
        # urlエンコードでurlっぽくしてくれる？？
        encodedParams = urllib.parse.urlencode(param)
        with urllib.request.urlopen("http://connpass.com/api/v1/event/?"+encodedParams) as res:
            respons = json.loads(res.read().decode('utf-8'))
        # 日付が過去なら飛ばす
        event_datetime = dateutil.parser.parse(respons['events'][0]['started_at'])
        if  event_datetime < today:
            return None

        tweet = respons['events'][0]['started_at'][5:7]+"月"+\
                respons['events'][0]['started_at'][8:10]+"日 "+\
                respons['events'][0]['title']+"\n"+\
                respons['events'][0]['event_url']+"\n#"+respons['events'][0]['hash_tag']

        return tweet
    except Exception as e:
        print('---- print works ---')
        print(e.args)
        print('----------print end-')


def get_evant_connpass(series_id, today):
    try:
        with urllib.request.urlopen("https://connpass.com/api/v1/event/?series_id="+ str(series_id)) as res:
            respons = json.loads(res.read().decode('utf-8'))

        events = respons['events']

        # イベント情報から開催日が過去の物を除外
        future_events = []
        for event in events:
            if series_id == 991: # LIGさんのイベントの時は場所にGEEKLAB.NAGANOが含まれるもののみ
                description = event['description']
                if 'GEEKLAB. NAGANO' not in description:
                    continue

            event_datetime = dateutil.parser.parse(event['started_at'])
            if event_datetime > today:
                event_date = change_date(event_datetime)

                future_events.append(event['title']+"("+event_date+")""\n"+\
                                event['event_url']+" #"+event['hash_tag'])

        return future_events

    except Exception as e:
        print(e.args)


def change_date(date):

    return str(date)[5:7]+"月"+ str(date)[8:10]+"日"



