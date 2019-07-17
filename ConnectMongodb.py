import pymongo

class DouYuDB:
    def __init__(self):
        self.dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.DouYudb = self.dbclient["DouYu"]
        self.Room = self.DouYudb["Room"]
        self.DanMu = self.DouYudb["DanMu"]
        self.Users = self.DouYudb["Users"]
        self.UserRank = self.DouYudb["UserRank"]

    def insertData(self, data, data_catagory):
        if data_catagory == "room":
            self.Room.insert_one(data)
        if data_catagory == "danmu":
            self.DanMu.insert_one(data)
        if data_catagory == "user":
            self.Users.insert_one(data)
        if data_catagory == "black":
            self.UserRank.insert_one(data)

    def findData(self):
        for x in self.Room.find():
            print(x)

    def find_id(self, id):
        if self.Room.find({"_id": str(id)}):
            for x in self.Room.find({"_id": str(id)}):
                if x:
                    return True
                else:
                    return False

    def findSendMostDanMuUser(self):
        userlist = []
        for x in self.DanMu.aggregate([
            {"$group": {"_id": "$用户ID", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]):
            userlist.append(x)
        for x in userlist:
            for z in self.DanMu.find({'用户ID': x['_id']}, {'昵称': 1, '_id': 0}).limit(1):
               x['昵称'] = z['昵称']
        return userlist
