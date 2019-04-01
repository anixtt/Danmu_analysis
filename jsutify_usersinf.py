# -*- coding:utf-8 -*-
import pymongo
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest, normaltest

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
douyudb = dbclient["DouYu"]
udc = douyudb['UserDanMuCount']  # 每个用户总共发弹幕数量
danmu = douyudb['DanMu']
danmucountnums = douyudb["dmcn"]  # 每种弹幕数量发送人数
mayberobot = douyudb["suspect"]  # 初级疑似
mayberobothigher = douyudb["suspecthigher"]  # 高级疑似
c = []
# for x in douyudb.DanMu.aggregate([
#     {"$project": {"昵称": 1, "发送弹幕时间": 1, "用户ID": 1, "_id": 0}},
#     {"$group": {"_id": "$用户ID", "count": {"$sum": 1}}},
#     {"$sort": {"count": -1}}
# ], allowDiskUse=True):
    # douyudb.UserDanMuCount.insert_one(x)
    # print(x)
for x in udc.find():
    c.append(x['userdmc'])
countarrary = np.asarray(c)
# print(kstest(countarrary, 'norm'))  # 正态分布假设性测试
# KstestResult(statistic=0.8413447460685429, pvalue=0.0)
# print(normaltest(countarrary))  # 正态分布假设性测试
# NormaltestResult(statistic=6780382.458753075, pvalue=0.0)
# print(np.median(countarrary))  # 中位数
# 3.0
# print(np.average(countarrary))  # 平均数
# 8.503834312407106
# print(np.var(countarrary, ddof=1))  # 方差
# 804.6513860745478
# print(np.std(countarrary, ddof=1))  # 标准差
# 28.366377739756405
x_axis = []
y_axis = []
z = 0

# 想画出来看看是什么样子 看上去是一个反函数...
# for x in udc.aggregate([
#     {"$project": {"_id": 0, "userdmc": 1}},
#     {"$group": {"_id": "$userdmc", "count": {"$sum": 1}}},
#     {"$sort": {"_id": -1}}
# ]):
#     z += int(x['_id']) * int(x['count'])
#     print(z)
#     x_axis.append(x['_id'])
#     y_axis.append(x['count'])
# plt.plot(x_axis, y_axis)
# plt.show()

# 找出通过平均弹幕数量*30天以上的用户，再通过用户信息筛选
for x in udc.aggregate([
    {"$match": {"userdmc": {"$gt": int(np.average(countarrary))*30}}},
    {"$lookup": {
        "from": "DanMu",
        "localField": "_id",
        "foreignField": "用户ID",
        "as": "inf"
    }}
]):
    if int(x['inf'][0]['等级']) < 10 and int(x['inf'][0]['粉丝牌等级']) < 9 and x['inf'][0]['贵族'] == '无':
        x['昵称'] = x['inf'][0]['昵称']
        for m in x['inf']:
            m.pop('昵称')
            m.pop('_id')
            m.pop('贵族')
            m.pop('房间ID')
            m.pop('粉丝牌名字')
            m.pop('用户ID')
            print(m)
        print(x)
        mayberobot.insert_one(x)