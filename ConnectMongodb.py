# -*- coding:utf-8 -*-
import pymongo

class DouYuDB:
    def __init__(self):
        self.dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.DouYudb = self.dbclient["DouYu"]
        self.Room = self.DouYudb["Room"]
        self.DanMu = self.DouYudb["DanMu"]
        self.Users = self.DouYudb["Users"]
        self.UserRank = self.DouYudb["UserRank"]
        self.RoomData = self.DouYudb["RoomData"]
        self.NewBlack = self.DouYudb["NewBlack"]
        self.Word = self.DouYudb["Word"]
        self.DailyString = self.DouYudb["DailyString"]
        self.uncleandata = self.DouYudb["uncleandata"]

    def insertData(self, data, data_catagory):
        if data_catagory == "room":
            self.Room.insert_one(data)
        if data_catagory == "danmu":
            self.DanMu.insert_one(data)
        if data_catagory == "user":
            self.Users.insert_one(data)
        if data_catagory == "userrank":
            self.UserRank.insert_one(data)
        if data_catagory == "roomdata":
            self.RoomData.insert_one(data)
        if data_catagory == "newblack":
            self.NewBlack.insert_one(data)
        if data_catagory == "word":
            self.Word.insert_one(data)
        if data_catagory == "dailystring":
            self.DailyString.insert_one(data)