from datetime import datetime, timezone, timedelta
import feedparser #pip install feedparser

now = datetime.now(timezone(timedelta(hours=9)))

feedData = feedparser.parse("http://api.tetsudo.com/traffic/atom.xml", response_headers={"content-type": "text/xml; charset=utf-8"})

trainUrl = {
    "jr" : "https://trafficinfo.westjr.co.jp/",
    "近江鉄道" : "https://www.ohmitetudo.co.jp/railway/",
    "信楽高原鉄道" : "https://koka-skr.co.jp",
    "京阪電気鉄道" : "https://www.keihan.co.jp/traffic/traintraffic/"
}

trainData = {
    "東海道新幹線" : False,
    "琵琶湖線" : False,
    "北陸本線" : False,
    "湖西線" : False,
    "草津線" : False,
    "近江鉄道" : False,
    "信楽高原鉄道" : False,
    "京阪電気鉄道" : False,
}
jrLink = False

for data in feedData["entries"]:
    if (datetime.strptime(data["updated"], '%Y-%m-%dT%H:%M:%S%z') > now + timedelta(minutes=-10)):
        if (data["title"][:8] == "【東海道新幹線】" and "（JR西日本）" in data["title"]):
            trainData["東海道新幹線"] = True
            jrLink = True
        if ("琵琶湖線" in data["title"]):
            trainData["琵琶湖線"] = True
            jrLink = True
        if ("北陸本線" in data["title"]):
            trainData["北陸本線"] = True
            jrLink = True
        if ("湖西線" in data["title"]):
            trainData["湖西線"] = True
            jrLink = True
        if ("草津線" in data["title"]):
            trainData["草津線"] = True
            jrLink = True

        if(data["title"][:6] == "【近江鉄道】"):
            trainData["近江鉄道"] = True

        if(data["title"][:8] == "【信楽高原鉄道】"):
            trainData["信楽高原鉄道"] = True

        if(data["title"][:8] == "【京阪電気鉄道】"):
            trainData["京阪電気鉄道"] = True

print(trainData)

if True in trainData.values():
    tweetData = f'{str(now.day)}日{str(now.hour)}時{str(now.minute)}分現在以下の路線で遅延等の情報があります。\n\n'
    for data in trainData:
        if trainData[data]:
            tweetData += f'#{data}\n'
    tweetData += "\nHP\n"
    if jrLink:
        tweetData += f'JR {trainUrl["jr"]}\n'
    if trainData["近江鉄道"]:
        tweetData += f'近江鉄道 {trainUrl["近江鉄道"]}\n'
    if trainData["信楽高原鉄道"]:
        tweetData += f'信楽高原鉄道 {trainUrl["信楽高原鉄道"]}\n'
    if trainData["京阪電気鉄道"]:
        tweetData += f'京阪電気鉄道 {trainUrl["京阪電気鉄道"]}\n'
    tweetData = tweetData[:-1]
    print(tweetData)

    import sys
    import os
    sys.path.append(os.path.abspath("../"))

    from pkg.twitter_python import tweet
    tweet(tweetData)

"""
{
    'title': '【JR東日本（関東地区）】常磐線・湘南新宿ライン・宇都宮線・日光線・中央線快速電車・中央本線',
    'title_detail': {
        'type': 'text/plain',
        'language': None, 'base': 'http://api.tetsudo.com/traffic/atom.xml',
        'value': '【JR東日本（関東地区）】常磐線・湘南新宿ライン・宇都宮線・日光線・中央線快速電車・中央本線'
    },
    'links': [
        {
            'rel': 'alternate',
            'type': 'text/html',
            'href': 'https://traininfo.jreast.co.jp/train_info/kanto.aspx'
        }
    ],
    'link': 'https://traininfo.jreast.co.jp/train_info/kanto.aspx',
    'id': 'https://traininfo.jreast.co.jp/train_info/kanto.aspx?20211103132701',
    'guidislink': False,
    'updated': '2021-12-18T10:33:01+09:00',
    'updated_parsed': time.struct_time(tm_year=2021, tm_mon=12, tm_mday=18, tm_hour=1, tm_min=33, tm_sec=1, tm_wday=5, tm_yday=352, tm_isdst=0),
    'published': '2021-11-03T13:27:01+09:00',
    'published_parsed': time.struct_time(tm_year=2021, tm_mon=11, tm_mday=3, tm_hour=4, tm_min=27, tm_sec=1, tm_wday=2, tm_yday=307, tm_isdst=0),
    'summary': '常磐線・湘南新宿ライン・宇都宮線・日光線・中央線快速電車・中央本線の情報が掲載されています（10:33現在）',
    'summary_detail': {
        'type': 'text/plain',
        'language': None,
        'base': 'http://api.tetsudo.com/traffic/atom.xml',
        'value': '常磐線・湘南新宿ライン・宇都宮線・日光線・中央線快速電車・中央本線の情報が掲載されています（10:33現在）'
    },
    'tags': [
        {
            'term': 'JR東日本',
            'scheme': None,
            'label': None
        }
    ]
}
"""