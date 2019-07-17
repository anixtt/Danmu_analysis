# from django.http import HttpResponse
from django.shortcuts import render
import sys
import json
sys.path.append("..")
import time
import re
import Segment
import pymongo


def show(request):
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    DouYudb = dbclient["DouYu"]
    DanMu = DouYudb["DanMu"]
    NewBlack = DouYudb["NewBlack"]
    Str = DouYudb["DailyString"]
    danmu_string = {}
    dict = {}
    danmulist = []
    slice_rule = re.compile('(.*),([\d]{2,6})')
    s = ''
    for x in DanMu.find({'发送弹幕时间': {'$regex': time.strftime("%Y-%m-%d", time.localtime())}}):
        s += x['弹幕内容']
    danmu_string['_id'] = time.strftime("%Y-%m-%d", time.localtime())
    danmu_string['弹幕字符串'] = s
    Segment.Chinese_Word_Segmentation(danmu_string['_id'], danmu_string['弹幕字符串'])
    with open('allresult%s.txt' % danmu_string['_id'], 'r') as read_file:
        while True:
            data = read_file.readline()
            if not data:
                break
                pass
            for l in slice_rule.findall(data):
                dict[l[0]] = l[1]

    # 弹幕数量排行（每日）
    for x in DanMu.aggregate([
        {"$project": {"_id": 0, "日期": {"$substr": ['$发送弹幕时间', 0, 10]}}},
        {"$group": {"_id": "$日期", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]):
        danmulist.append(x)



    # for x in douyudb.DanMu.aggregate([
    #     {"$project": {"_id": 0, "日期": {"$substr": ['$发送弹幕时间', 0, 10]}}},
    #     {"$group": {"_id": "$日期"}},
    #     {"$sort": {"_id": 1}}
    # ]):
    #     all_day.append(x)

    # 发弹幕最多排行（总）
    # for x in douyudb.DanMu.aggregate([
    #     {"$group": {"_id": "$用户ID", "count": {"$sum": 1}}},
    #     {"$sort": {"count": -1}},
    #     {"$limit": 10}
    # ]):
    #     user_list.append(x)
    # for x in user_list:
    #     for z in douyudb.DanMu.find({'用户ID': x['_id']}, {'昵称': 1, '_id': 0}).limit(1):
    #         x['昵称'] = z['昵称']
    # for x in user_list:
    #     for z in all_day:
    #         for j in douyudb.DanMu.aggregate([
    #             {"$match": {"用户ID": x["_id"]}},
    #             {"$match": {"发送弹幕时间": {"$regex": z["_id"]}}},
    #             {"$group": {"_id": "$用户ID", "count": {"$sum": 1}}}
    #         ]):
    #             x[z["_id"]] = j["count"]
    # for x in UserRank.find():
    #     d.append(x)
    return render(request, 'show.html', {'dict': json.dumps(dict),
                                         'danmu_list': json.dumps(danmulist)})
                                         # 'all_day': json.dumps(all_day)})
                                         # 'd': json.dumps(d)})