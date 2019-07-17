from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
import sys
sys.path.append("..")
import DouYuDanMu
import threading
import time
import inspect
import ctypes

from asgiref.sync import async_to_sync


class DanmuConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = '1492968'
        # self.room_group_name = 'danmu_%s' % self.room_name
        self.room_group_name = 'danmu'
        # 入组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 退组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    #
    # 从websocket接收数据
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'End':
            await self.close()
        else:
            # 从服务器发数据给客户端
            dmcls = DouYuDanMu.getDanMuSocket()
            dmcls.get_sendthreading(self.room_name, self.channel_layer, self.room_group_name)
            # def _async_raise(tid, exctype):
            #     """raises the exception, performs cleanup if needed"""
            #     tid = ctypes.c_long(tid)
            #     if not inspect.isclass(exctype):
            #         exctype = type(exctype)
            #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            #     if res == 0:
            #         raise ValueError("invalid thread id")
            #     elif res != 1:
            #         # """if it returns a number greater than one, you're in trouble,
            #         # and you should call it again with exc=NULL to revert the effect"""
            #         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            #         raise SystemError("PyThreadState_SetAsyncExc failed")
            #
            # def stop_thread(thread):
            #     _async_raise(thread.ident, SystemExit)
            # def insert_danmu(self1):
            #     z = ''
            #     w = ''
            #     userid = {}
            #     s_x = []
            #     second_time = int(time.time())
            #     aim_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(second_time + 5))
            #     # model = word2vec.Word2Vec.load('/Users/zouminlong/PycharmProjects/DouYu/弹幕.model')
            #     while True:
            #         if not dmcls.dmqu.empty():
            #             x = dmcls.dmqu.get()
            #             if x['_id'] not in s_x:
            #                 s_x.append(x['_id'])
            #                 # if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) != aim_time:
            #                 #     if x['用户ID'] in userid.keys():
            #                 #         userid[x['用户ID']] += 1
            #                 #     else:
            #                 #         userid[x['用户ID']] = 1
            #                 #     x['sign'] = 0
            #                 # if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) == aim_time:
            #                 #     for mmm in userid.values():
            #                 #         if mmm >= 3:
            #                 #             x['sign'] = 1
            #                 #         else:
            #                 #             x['sign'] = 0
            #                 #     userid = {}
            #                 #     second_time = int(time.time())
            #                 #     aim_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(second_time + 5))
            #                 # print(userid)
            #
            #                 #     z += x['弹幕内容']
            #                 #     if 600 > len(z) > 200:
            #                 #         x['分词'] = Segment.Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), z)
            #                 #         for word in x['分词']:
            #                 #             w += word[0] + ' '
            #                 #         print(model.doesnt_match(w.split()))
            #                 #     elif len(z) >= 600:
            #                 #         print(123)
            #                 #         z = z[-600:-399]
            #                 #         print(z)
            #                 #         x['分词'] = Segment.Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), z)
            #                 #         for word in x['分词']:
            #                 #             w += word[0] + ' '
            #                 #         print(model.doesnt_match(w.split()))
            #
            #
            #
            #                 # if message == 'start':
            #                 #     pass
            #                 # elif len(message) > 100:
            #                 #     x['segment'] = \
            #                 #     Segment.Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), message)
            #                 #     print(x['segment'])
            #                 # dmcls.dmqu.task_done()
            #                 # self1.channel_layer.group_send(self1.room_group_name, {'text': x})
            #
            #                 # print(x)
            #
            #
            # # def segment_danmu(self1):
            # #     while True:
            # #         if message == 'start':
            # #             pass
            # #         elif len(message) > 100:
            # #             x = {}
            # #             x['segment'] = \
            # #                 Segment.Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), message)
            # #             async_to_sync(self1.channel_layer.group_send)(self1.room_group_name,
            # #                                                           {'type': 'danmu_message', 'message': x})
            # #             print(x)
            #
            # t1 = threading.Thread(target=dmcls.start, args=((int(self.room_name)),))
            # t2 = threading.Thread(target=insert_danmu, args=(self,))
            # # t3 = threading.Thread(target=segment_danmu, args=(self,))
            # t1.start()
            # t2.start()
            # t3.start()
            # time.sleep(1)
            # stop_thread(t1)
            # stop_thread(t2)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'danmu_message',
        #         'message': message
        #     }
        # )

    # # 接收客户端数据
    async def danmu_message(self, event):
        message = event['message']
        # print(message)
        # print(dm)
        # 通过websocket发数据
        await self.send(text_data=json.dumps({
            'message': message
        }))
