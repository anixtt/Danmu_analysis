import numpy as np
import pandas as pd
import re
import sys
from numpy import log, min
import pymongo
import multiprocessing

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
DouYudb = dbclient["DouYu"]
DanMu = DouYudb["DanMu"]
NewBlack = DouYudb["NewBlack"]
Str = DouYudb["DailyString"]
day_date = []
for x in DouYudb.DanMu.aggregate([
    {"$project": {"_id": 0, "日期": {"$substr": ['$发送弹幕时间', 0, 10]}}},
    {"$group": {"_id": "$日期"}},
    {"$sort": {"_id": 1}}
]):
    day_date.append(x)
all_string = []
everyday_danmu_string = {}
if len(day_date) != Str.find().count():
    for day in day_date:
        print(day)
        s = ''
        for danmu_info in DanMu.find({'发送弹幕时间': {'$regex': day['_id']}}):
            s += danmu_info['弹幕内容']
        everyday_danmu_string['_id'] = day['_id']
        print(sys.getsizeof(s))
        if sys.getsizeof(s) <= 2**24:
            everyday_danmu_string['弹幕字符串'] = s
            Str.update({'_id': everyday_danmu_string['_id']},
                       {'$set': {'弹幕字符串': everyday_danmu_string['弹幕字符串']}}, True)
        else:
            num = sys.getsizeof(s) / (2**24)
            for x in range(int(num)):
                everyday_danmu_string['弹幕字符串'+str(x)] = s[x*(2**24):(x+1)*(2**14)]
                Str.update({'_id': everyday_danmu_string['_id']},
                           {'$set': {'弹幕字符串': everyday_danmu_string['弹幕字符串' + str(x)]}}, True)
        all_string.append(everyday_danmu_string)
else:
    for x in Str.find():
        all_string.append(x)
myre = {2: '(..)', 3: '(...)', 4: '(....)', 5: '(.....)', 6: '(......)', 7: '(.......)', 8: '(........)',
        9: '(.........)', 10: '(..........)', 11: '(...........)', 12: '(............)'}

min_count = 20  # 录取词语最小出现次数
min_support = 30  # 录取词语最低支持度，1代表着随机组合
min_s = 3  # 录取词语最低信息熵，越大说明越有可能独立成词
max_sep = 12  # 候选词语的最大字数
t = []

def cal_S(sl):  # 信息熵计算
    return -((sl / sl.sum()).apply(log) * sl / sl.sum()).sum()

def Chinese_Word_Segmentation(day, s):
    t.append(pd.Series(list(s)).value_counts())  # 逐字统计
    tsum = t[0].sum()  # 统计总字数
    rt = []
    print(u'正在处理%s...' % day)
    for m in range(2, max_sep + 1):
        print(u'正在生成%s字词...' % m)
        t.append([])
        print(t)
        for i in range(m):  # 生成所有可能的m字词
            t[m - 1] = t[m - 1] + re.findall(myre[m], s[i:])
            print(t[m - 1])
        t[m - 1] = pd.Series(t[m - 1]).value_counts()  # 逐词统计
        print(t[m - 1])
        t[m - 1] = t[m - 1][t[m - 1] > min_count]  # 最小次数筛选
        print(t[m - 1])
        tt = t[m - 1][:]
        print(tt)
        for k in range(m - 1):
            qq = np.array(list(map(
                lambda ms: tsum * t[m - 1][ms] / t[m - 2 - k][ms[:m - 1 - k]] / t[k][ms[m - 1 - k:]],
                    tt.index))) > min_support  # 最小支持度筛选。
            print(qq)
            tt = tt[qq]
            print(tt)
        rt.append(tt.index)
        print(rt)

    for i in range(2, max_sep + 1):
        print(u'正在进行%s字词的最大熵筛选(%s)...' % (i, len(rt[i - 2])))
        pp = []  # 保存所有的左右邻结果
        for j in range(i + 2):
            pp = pp + re.findall('(.)%s(.)' % myre[i], s[j:])
        pp = pd.DataFrame(pp).set_index(1).sort_index()  # 排序
        index = np.sort(np.intersect1d(rt[i - 2], pp.index))  # 作交集
        # 左邻和右邻信息熵筛选
        index = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[0][s]).value_counts()), index))) > min_s]
        rt[i - 2] = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[2][s]).value_counts()), index))) > min_s]

    # 输出前处理
    for i in range(len(rt)):
        t[i + 1] = t[i + 1][rt[i]]
        t[i + 1].sort_values(ascending=False)

    pd.DataFrame(pd.concat(t[1:])).to_csv('dailystring/allresult%s.txt' % day, header=False)

def multi_process(all_string):
    p = multiprocessing.Pool(processes=4)
    for e in all_string:
        p.apply_async(Chinese_Word_Segmentation, args=(e['_id'], e['弹幕字符串']))
    p.close()
    p.join()
def run():
    for i in range(0, len(all_string), 4):
        multi_process(all_string[i:i+4])