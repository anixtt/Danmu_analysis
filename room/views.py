from django.http import HttpResponse
import json
import time
import datetime
import pymongo
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
from django.utils.safestring import mark_safe
from urllib import request as req
from django.views.decorators.csrf import csrf_exempt
import jieba
import jieba.analyse

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('../stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr



# Create your views here.
@csrf_exempt
def liveroominf(request):
    infdict = {}
    roominf = json.loads(req.urlopen('http://open.douyucdn.cn/api/RoomApi/room/9999').read().decode('utf-8'))
    infdict['owner_name'] = roominf['data']['owner_name']
    if roominf['data']['room_status'] == "1":
        infdict['room_status'] = '直播中'
    else:
        infdict['room_status'] = '未直播'
    infdict['start_time'] = roominf['data']['start_time']
    infdict['hot'] = roominf['data']['hn']
    infdict['room_name'] = roominf['data']['room_name']
    infdict['owner_image'] = roominf['data']['avatar']
    return HttpResponse(json.dumps(infdict))

@csrf_exempt
def nowtimeroomdata(request):
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    nowtimedmdb = douYudb[time.strftime("%Y%m%d", time.localtime())]
    live_room_data = {}
    live_room_data['danmu_num'] = str(nowtimedmdb.find().count())
    live_room_data['danmu_date'] = str(time.strftime("%Y-%m-%d", time.localtime()))
    return HttpResponse(json.dumps(live_room_data))


@csrf_exempt
def danmu_num_data(request):
    time_hour = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30',
        '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
        '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    danmu_num_all = []
    fans_danmu_num = []
    normal_danmu_num = []
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    nowtimedmdb = douYudb[time.strftime("%Y%m%d", time.localtime())]
    today = datetime.date.today()
    t = []
    for i in time_hour:
        t.append(str(today)+' '+i)
    for i in range(len(t) - 1):
        numall = nowtimedmdb.find({"$and": [{"发送弹幕时间": {"$gte": t[i]}}, {"发送弹幕时间": {"$lt": t[i+1]}}]}).count()
        normalnumall = nowtimedmdb.find({"$and": [{"发送弹幕时间": {"$gte": t[i]}}, {"发送弹幕时间": {"$lt": t[i+1]}}], "粉丝牌名字": "无", "弹幕颜色": "无"}).count()
        fansnumall = numall - normalnumall
        danmu_num_all.append(numall)
        normal_danmu_num.append(normalnumall)
        fans_danmu_num.append(fansnumall)
    last = nowtimedmdb.find({"发送弹幕时间": {"$gte": t[-1]}}).count()
    lastnormal = nowtimedmdb.find({"发送弹幕时间": {"$gte": t[-1]}, "粉丝牌名字": "无"}).count()
    lastfans = last - lastnormal
    danmu_num_all.append(last)
    normal_danmu_num.append(lastnormal)
    fans_danmu_num.append(lastfans)
    dm_dict = {}
    dm_dict['dmnum'] = danmu_num_all
    dm_dict['ndmnum'] = normal_danmu_num
    dm_dict['fdmnum'] = fans_danmu_num
    print(dm_dict)
    return HttpResponse(json.dumps(dm_dict))

@csrf_exempt
def pasttimeroomdata(request):
    date1 = request.POST.get("searchdate")
    date1 = ''.join(date1.split('"'))
    date = ''.join(date1.split('-'))
    time_hour = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30',
                 '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
                 '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                 '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
                 '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    danmu_num_all = []
    fans_danmu_num = []
    normal_danmu_num = []
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    nowtimedmdb = douYudb[date]
    t = []
    for i in time_hour:
        t.append(str(date1) + ' ' + i)
    print(t)
    for i in range(len(t) - 1):
        numall = nowtimedmdb.find({"$and": [{"发送弹幕时间": {"$gte": t[i]}}, {"发送弹幕时间": {"$lt": t[i + 1]}}]}).count()
        normalnumall = nowtimedmdb.find(
            {"$and": [{"发送弹幕时间": {"$gte": t[i]}}, {"发送弹幕时间": {"$lt": t[i + 1]}}], "粉丝牌名字": "无", "弹幕颜色": "无"}).count()
        fansnumall = numall - normalnumall
        danmu_num_all.append(numall)
        normal_danmu_num.append(normalnumall)
        fans_danmu_num.append(fansnumall)
    last = nowtimedmdb.find({"发送弹幕时间": {"$gte": t[-1]}}).count()
    lastnormal = nowtimedmdb.find({"发送弹幕时间": {"$gte": t[-1]}, "粉丝牌名字": "无"}).count()
    lastfans = last - lastnormal
    danmu_num_all.append(last)
    normal_danmu_num.append(lastnormal)
    fans_danmu_num.append(lastfans)
    dm_dict = {}
    dm_dict['dmnum'] = danmu_num_all
    dm_dict['ndmnum'] = normal_danmu_num
    dm_dict['fdmnum'] = fans_danmu_num
    dm_dict['allnum'] = str(nowtimedmdb.find().count())
    dbclient.close()
    print(dm_dict)
    return HttpResponse(json.dumps(dm_dict))

@csrf_exempt
def makecloudword(request):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = str(today - oneday)
    yd = ''.join(str(yesterday).split('-'))
    worddict = {}
    userdict = {}
    userlist = []
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    s = ''
    for x in douYudb[yd].find():
        s += seg_sentence(x['弹幕内容']) + '\r\n'
    with open('../others/danmustrings/danmustring%s' % yesterday, 'w') as f:
        f.write(s)
    f.close()
    text = open('../others/danmustrings/danmustring%s' % yesterday, 'r').read()

    bg_pic = imread(r'../dota2logo.jpeg')

    wordlist_after_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist_after_jieba)

    font = r'../Alibaba-PuHuiTi-Medium.ttf'
    wc = WordCloud(mask=bg_pic, background_color='white', font_path=font, scale=1.5).generate(wl_space_split)
    image_colors = ImageColorGenerator(bg_pic)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file(r'../others/wordcloud/%s词云.jpg' % yesterday)
    keywords = jieba.analyse.extract_tags(text, topK=20, allowPOS=('ns', 'n'))
    worddict['_id'] = yesterday
    worddict['热词前二十'] = keywords
    douYudb['DayWordTop'].insert_one(worddict)
    for z in douYudb[yd].aggregate([
            {"$group": {"_id": "$用户ID", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]):
        userlist.append(z)
    userdict['_id'] = yesterday
    userdict['弹幕数前十'] = userlist
    douYudb['danmunumtop'].insert_one(userdict)



@csrf_exempt
def userdata(request):
    date1 = request.POST.get("searchdate")
    date1 = ''.join(date1.split('"'))
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    senddict = {}
    for x in douYudb['danmunumtop'].find({'_id': date1}):
        senddict['弹幕数前十'] = x['弹幕数前十']
    for x in douYudb['DayWordTop'].find({'_id': date1}):
        senddict['热词前二十'] = x['热词前二十']
    dbclient.close()
    return HttpResponse(json.dumps(senddict))

@csrf_exempt
def getDetailedInf(request):
    userID = request.POST.get("searchdate")
    userID = ''.join(userID.split('"'))
    userdanmunum = 0
    usermorning = 0
    userafternoon = 0
    usernight = 0
    userdeepnight = 0
    usernosleep = 0
    userbm = 0
    useractivetime = []
    userinf = {}
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    douYudb = dbclient["DouYu"]
    all_day = [{'_id': '2018-12-31'}, {'_id': '2019-01-01'}, {'_id': '2019-01-02'}, {'_id': '2019-01-06'},
               {'_id': '2019-01-07'}, {'_id': '2019-01-08'}, {'_id': '2019-01-09'}, {'_id': '2019-01-10'},
               {'_id': '2019-01-11'}, {'_id': '2019-01-12'}, {'_id': '2019-01-13'}, {'_id': '2019-01-14'},
               {'_id': '2019-01-15'}, {'_id': '2019-01-16'}, {'_id': '2019-01-17'}, {'_id': '2019-01-18'},
               {'_id': '2019-01-20'}, {'_id': '2019-01-21'}, {'_id': '2019-01-22'}, {'_id': '2019-01-23'},
               {'_id': '2019-01-24'}, {'_id': '2019-01-25'}, {'_id': '2019-01-26'}, {'_id': '2019-01-27'},
               {'_id': '2019-01-28'}, {'_id': '2019-01-29'}, {'_id': '2019-01-30'}, {'_id': '2019-01-31'},
               {'_id': '2019-02-01'}, {'_id': '2019-02-02'}, {'_id': '2019-02-03'}, {'_id': '2019-02-04'},
               {'_id': '2019-02-05'}, {'_id': '2019-02-06'}, {'_id': '2019-02-07'}, {'_id': '2019-02-08'},
               {'_id': '2019-02-09'}, {'_id': '2019-02-10'}, {'_id': '2019-02-11'}, {'_id': '2019-02-12'},
               {'_id': '2019-02-13'}, {'_id': '2019-02-14'}, {'_id': '2019-02-15'}, {'_id': '2019-02-16'},
               {'_id': '2019-02-17'}, {'_id': '2019-02-18'}, {'_id': '2019-02-19'}, {'_id': '2019-02-20'},
               {'_id': '2019-02-21'}, {'_id': '2019-02-22'}, {'_id': '2019-02-23'}, {'_id': '2019-02-24'},
               {'_id': '2019-02-25'}, {'_id': '2019-02-26'}, {'_id': '2019-02-27'}, {'_id': '2019-03-27'},
               {'_id': '2019-03-28'}, {'_id': '2019-04-05'}, {'_id': '2019-04-06'}, {'_id': '2019-04-11'},
               {'_id': '2019-04-15'}, {'_id': '2019-04-16'}, {'_id': '2019-04-17'}, {'_id': '2019-04-21'},
               {'_id': '2019-04-22'}, {'_id': '2019-04-23'}, {'_id': '2019-04-24'}, {'_id': '2019-04-25'},
               {'_id': '2019-04-26'}, {'_id': '2019-04-27'}, {'_id': '2019-04-28'}, {'_id': '2019-04-29'},
               {'_id': '2019-04-30'}, {'_id': '2019-05-04'}, {'_id': '2019-05-05'}, {'_id': '2019-05-06'},
               {'_id': '2019-05-07'}, {'_id': '2019-05-08'}]
    s = ''
    for x in all_day:
        for z in douYudb[''.join(x['_id'].split('-'))].find({"用户ID": userID}):
            userinf['昵称'] = z['昵称']
            userinf['等级'] = z['等级']
            userinf['粉丝牌'] = z['粉丝牌名字'] + ' ' + z['粉丝牌等级']
            userdanmunum += 1
            useractivetime.append(z['发送弹幕时间'][-8:-1])
            s += seg_sentence(z['弹幕内容']) + '\r\n'
    for x in useractivetime:
        if '06' > x >= '00':
            usernosleep += 1
        if '08' > x >= '06':
            userbm += 1
        if '12' >= x >= '08':
            usermorning += 1
        if '18' > x >= '13':
            userafternoon += 1
        if '22' > x >= '18':
            usernight += 1
        if '24' > x >= '22':
            userdeepnight += 1
    userat = {'凌晨': usernosleep, '清晨': userbm, '早晨': usermorning, '下午': userafternoon, '晚上': usernight,
              '深夜': userdeepnight}
    userat = sorted(userat.items(), key=lambda x: x[1], reverse=True)
    userinf['弹幕数'] = userdanmunum
    userinf['发弹幕时间'] = [userat[0][0], userat[1][0]]
    keywords = jieba.analyse.extract_tags(s, topK=5, allowPOS=('ns', 'n'))
    userinf['常说词'] = keywords
    dbclient.close()
    return HttpResponse(json.dumps(userinf))
