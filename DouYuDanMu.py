# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import multiprocessing
import ConnectMongodb
import socket
import time
import threading
import re


class getDanMuSocket():
    # 配置socket的ip和端口
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname("openbarrage.douyutv.com")
        self.port = 8601
        self.client.connect((self.host, self.port))

    # 获取用户昵称及弹幕信息的正则表达式
    # bnn@=粉丝牌 bl@=粉丝牌等级
    # rg@=4房管
    # ct@=客户端类型
    # 房间id 客户端类型 用户id 用户昵称 弹幕内容 弹幕id 等级 贵族 弹幕颜色 粉丝牌名字 粉丝牌等级 粉丝牌所属房间
        self.danmu = re.compile\
            ('type@=chatmsg.*?/rid@=(.*?)/(?:ct@=(.*?)/)?uid@=(.*?)/nn@=(.*?)/'
             'txt@=(.*?)/cid@=(.*?)/.*?level@=(.*?)/sahf@=0/(?:nl@=(.*?)/)?(?:col@=(.*?)/)?.*?bnn@=(.*?)/bl@=(.*?)/brid@=(.*?)/')

    def sendmsg(self, msgstr):
        # 协议头 参照斗鱼协议
        msg = msgstr.encode('utf-8')
        data_length = len(msg) + 8
        code = 689
        msgHead = int.to_bytes(data_length, 4, 'little') \
                  + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
        self.client.send(msgHead)
        sent = 0
        while sent < len(msg):
            tn = self.client.send(msg[sent:])
            sent = sent + tn

    def keeplive(self):
        # 向服务器发心跳包，维持长连接
        def sendhf():
            while True:
                msg = 'type@=mrkl/\0'
                self.sendmsg(msg)
                time.sleep(30)
        t = threading.Thread(target=sendhf)
        t.start()


    def start(self, roomid):
        msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
        # 登录
        self.sendmsg(msg)
        print(msg)
        msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
        # 入组
        self.sendmsg(msg_more)
        print(msg_more)
        douyudb = ConnectMongodb.DouYuDB()
        # gfid 2122盛典星耀超火 2123盛典火箭 2125盛典飞机 1951盛典办卡 1859小飞碟 2097幸运戒指 2095幸运水晶
        #      2048冲鸭 2096幸运钥匙 1949典赞 1948特供鱼丸 713辣眼睛 193弱鸡 824荧光棒 192赞 520稳
        #      712棒棒哒 714怂 519 1855 1857 1858办卡
        self.keeplive()
        while True:
            data = self.client.recv(1024)
            dataDict = {"房间接收信息": data.decode(encoding='utf-8', errors='ignore')}
            douyudb.insertData(dataDict, "roomdata")
            print(dataDict)
            # gift_inf = re.compile('(type@=dgb/.*/)').findall(data.decode(encoding='utf-8', errors='ignore'))
            # for i in gift_inf:
            #     print(i)
            # print(data.decode(encoding='utf-8', errors='ignore'))
            danmu_more = self.danmu.findall(data.decode(encoding='utf-8', errors='ignore'))
            if not data:
                break
            else:
                try:
                    for i in danmu_more:
                        i = list(i)
                        dmDict = {}
                        if len(i[7]) == 0:
                            i[7] = '无'
                        if len(i[8]) == 0:
                            i[8] = '无'
                        if len(i[9]) == 0:
                            i[9] = '无'
        # nl@=7游侠 nl@=3伯爵 nl@=1骑士 nl@=2子爵 nl@=4公爵 nl@=5国王 nl@=6皇帝
        # col@=2蓝色(粉丝牌六级及以上) col@=3绿色(九级及以上) col@=6粉色(十二级及以上) col@=4橙色(十五级及以上)
        # col@=5紫色(十八级及以上) col@=1红色(二十一级及以上)
                        nobility = {'1': '骑士', '2': '子爵', '3': '伯爵', '4': '公爵',
                                    '5': '国王', '6': '皇帝', '7': '游侠', '无': '无'}
                        danmu_color = {'1': '红色', '2': '蓝色', '3': '绿色', '4': '橙色',
                                       '5': '紫色', '6': '粉色', '无': '无'}
                        i[7] = nobility[i[7]]
                        i[8] = danmu_color[i[8]]
                        if i[9] == '无':
                            i[11] = '无'
            # 房间id 客户端类型 用户id 用户昵称 弹幕内容 弹幕id(_id) 等级 贵族 弹幕颜色 粉丝牌名字 粉丝牌等级
            # 粉丝牌房间号
                        dmDict['_id'] = i[5]
                        dmDict['房间ID'] = i[0]
                        dmDict['用户ID'] = i[2]
                        dmDict['昵称'] = i[3]
                        dmDict['弹幕内容'] = i[4]
                        dmDict['等级'] = i[6]
                        dmDict['贵族'] = i[7]
                        dmDict['弹幕颜色'] = i[8]
                        dmDict['粉丝牌名字'] = i[9]
                        dmDict['粉丝牌等级'] = i[10]
                        dmDict['粉丝牌房间ID'] = i[11]
                        dmDict['发送弹幕时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        douyudb.insertData(dmDict, "danmu")
                        print(dmDict)
                except:
                    continue


# 启动程序
if __name__ == '__main__':
    room = [9999, 99999]    # 房间号, 可以自己添加
    for i in range(len(room)):
        sx = getDanMuSocket()
        p = multiprocessing.Process(target=sx.start, args=(room[i], ))
        p.start()
