import numpy as np
import pandas as pd
import re
import sys
from numpy import log, min
import pymongo
import multiprocessing
import time
import math

# day_date = []
# for x in DouYudb.DanMu.aggregate([
#     {"$project": {"_id": 0, "日期": {"$substr": ['$发送弹幕时间', 0, 10]}}},
#     {"$group": {"_id": "$日期"}},
#     {"$sort": {"_id": 1}}
# ]):
#     day_date.append(x)
# all_string = []
# everyday_danmu_string = {}
# if len(day_date) != Str.find().count():
#     for day in day_date:
#         print(day)
#         s = ''
#         for danmu_info in DanMu.find({'发送弹幕时间': {'$regex': day['_id']}}):
#             s += danmu_info['弹幕内容']
#         everyday_danmu_string['_id'] = day['_id']
#         print(sys.getsizeof(s))
#         if sys.getsizeof(s) <= 2**24:
#             everyday_danmu_string['弹幕字符串'] = s
#             Str.update({'_id': everyday_danmu_string['_id']},
#                        {'$set': {'弹幕字符串': everyday_danmu_string['弹幕字符串']}}, True)
#         else:
#             num = sys.getsizeof(s) / (2**24)
#             for x in range(int(num)):
#                 everyday_danmu_string['弹幕字符串'+str(x)] = s[x*(2**24):(x+1)*(2**14)]
#                 Str.update({'_id': everyday_danmu_string['_id']},
#                            {'$set': {'弹幕字符串': everyday_danmu_string['弹幕字符串' + str(x)]}}, True)
#         all_string.append(everyday_danmu_string)
# else:
#     for x in Str.find():
#         all_string.append(x)
myre = {2: '(..)', 3: '(...)', 4: '(....)', 5: '(.....)', 6: '(......)', 7: '(.......)', 8: '(........)',
        9: '(.........)', 10: '(..........)', 11: '(...........)', 12: '(............)'}

min_support = 30  # 录取词语最低支持度，1代表着随机组合
min_s = 0.2  # 录取词语最低信息熵，越大说明越有可能独立成词
max_sep = 10  # 候选词语的最大字数
t = []

def cal_S(sl):  # 信息熵计算
    return -((sl / sl.sum()).apply(log) * sl / sl.sum()).sum()

def Chinese_Word_Segmentation(day, s):
    s = ''.join(s.split())
    s = ''.join(s.split(','))
    s = ''.join(s.split('，'))
    s = s.lower()
    t.append(pd.Series(list(s)).value_counts())  # 逐字统计 每个字出现的个数
    # tsum = t[0].sum()  # 统计总字数
    rt = []
    print(u'正在处理%s...' % day)
    for m in range(2, max_sep + 1):
        print(u'正在生成%s字词...' % m)
        t.append([])
        # print(t)
        # print(123)
        for i in range(len(s)):  # 生成所有可能的m字词
            t[m - 1] = list(t[m - 1]) + list(re.findall(myre[m], s[i:]))
        maybe_word_length = len(t[m - 1])
        t[m - 1] = pd.Series(t[m - 1]).value_counts() / maybe_word_length  # 逐词统计
        t[m - 1] = t[m - 1][(t[m - 1]) > 0.0051]  # 最小次数筛选 0.0051可自己根据结果更改
        tt = t[m - 1][:]  # 筛选之后的所有m字词 Series
        # for k in range(m - 1):
        #     print(list(map(lambda ms: tsum * t[m - 1][ms], tt.index)))
        #     print(list(map(lambda ms: t[m - 2 - k][ms[:m - 1 - k]], tt.index)))
        #     print(list(map(lambda ms: t[k][ms[m - 1 - k:]], tt.index)))
        #     qq = np.array(list(map(
        #         lambda ms: tsum * t[m - 1][ms] / t[m - 2 - k][ms[:m - 1 - k]] / t[k][ms[m - 1 - k:]],
        #             tt.index))) > min_support  # 最小支持度筛选。
        #     tt = tt[qq]
        rt.append(tt.index)

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
    d = {}
    words = []
    two_words = []
    others_words = []
    clear_words = []
    frequencies = []
    nums = 0
    for i in range(len(rt)):
        t[i + 1] = t[i + 1][rt[i]]
        t[i + 1].sort_values(ascending=False)
        for w in list(rt[i]):
            if len(w) == 2:
                two_words.append(w)
            else:
                others_words.append(w)
            words.append(w)
        for f in list(t[i + 1]):
            frequencies.append(f)
    slice_rule = re.compile('(.)\\1+')
    num = 0
    for word in words:
        z = ''.join(re.split(slice_rule, word))
        if len(z) == len(word):
            pass
        else:
            for xm in re.split(slice_rule, word):
                if xm == '':
                    num += 1
            if num > 3:
                clear_words.append(word)
    for other in others_words:
        for two in two_words:
            if len(''.join(other.split(two))) == len(other):
                pass
            else:
                for gh in other.split(two):
                    if gh == '':
                        nums += 1
                if nums > 2 and two in other:
                    if two in clear_words:
                        clear_words.append(two)
                    if other in clear_words:
                        clear_words.append(other)
                    else:
                        clear_words.append(other)
    clear_words = set(clear_words)
    print(clear_words)
    for i in range(len(words)):
        d[words[i]] = frequencies[i]
    for i in clear_words:
        del d[i]
    d = sorted(d.items(), key=lambda h: h[1], reverse=True)
    # slice_rule = re.compile('(..)\\1+')
    # num = 0
    # for mm in d:
    #     z = ''.join(re.split(slice_rule, mm[0]))
    #     if len(z) == len(mm[0]):
    #         pass
    #     else:
    #         del d[num]
    #         print(d)
    #     num += 1
    return d
    # pd.DataFrame(pd.concat(t[1:])).to_csv('allresult%s.txt' % day, header=False)
    # pd.DataFrame(pd.concat(t[1:])).to_csv('allresult%s.txt' % day, header=False)
    # print(pd.DataFrame(pd.concat(t[1:])))
    # for row in pd.DataFrame(pd.concat(t[1:])):
    #     print(row)
    # slice_rule = re.compile('(.*),([\d]{2,6})')
    # words = []
    # frequencies = []
    # try:
    #     with open('allresult%s.txt' % day, 'r') as read_file:
    #         while True:
    #             data = read_file.readline()
    #             if not data:
    #                 break
    #                 pass
    #             print(slice_rule.findall(data))
    #             word = slice_rule.findall(data)[0][0]
    #             frequency = slice_rule.findall(data)[0][1]
    #             if word not in words:
    #                 words.append(word)
    #                 frequencies.append(int(frequency))
    #             else:
    #                 for i in range(len(words)):
    #                     if words[i] == word:
    #                         frequencies[i] += int(frequency)
    #         read_file.close()
    # except FileNotFoundError:
    #     print('No file')
    # dict = {}
    # for i in range(len(words)):
    #     dict[words[i]] = frequencies[i]
    # dict = sorted(dict.items(), key=lambda item: item[1])
    # return dict

# if __name__ == '__main__':
#     s = '旭老八归位早出晚归咋回事呢让1保8？先归位再说哈哈哈，稳定，老八，很稳定啊又第一了归位追不上aabb归位早出晚归人已虚 归位 早出晚归人已虚 归位 早出晚归人已虚 归狗宝旭旭 归位旭老八归位？？a归位前面全是高手啊 旭老八归位你这个起步速度，明显改了付费挨打碰碰车？哈哈哈归位房间一开，油门一加，开局第一，跑完第八0蓝光4M是假的吗，怎么看不见了归位王者归位国服 起步王你刚刚骂了大狗人家不想让你了旭老八你刚刚骂了大狗人家不想让你了aabb旭老八重出江湖旭老八重出江湖旭老八重出江湖旭老八重出江湖旭老八重出又第一了名词一直很稳定啊这把又稳了大狗不在第七第八稳了王者归位旭老八归位撞墙过弯撞墙过弯撞墙过弯撞墙过弯撞墙过弯撞墙过弯撞墙过弯撞墙过弯恭喜宝哥勇夺第一旭老八归位你开的是奔驰，边跑边漏油'
#     Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), s)
#     dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     DouYudb = dbclient["DouYu"]
#     DanMu = DouYudb["DanMu"]
#     NewBlack = DouYudb["NewBlack"]
#     s = ''
#     danmu_string = {}
#     for x in NewBlack.find():
#         s += x['弹幕内容']
#     danmu_string['_id'] = '黑名单'
#     danmu_string['弹幕字符串'] = s
#     Chinese_Word_Segmentation(danmu_string['_id'], danmu_string['弹幕字符串'])
# def multi_process(all_string):
#     p = multiprocessing.Pool(processes=4)
#     for e in all_string:
#         p.apply_async(Chinese_Word_Segmentation, args=(e['_id'], e['弹幕字符串']))
#     p.close()
#     p.join()
# def run():
#     for i in range(0, len(all_string), 4):
#         multi_process(all_string[i:i+4])