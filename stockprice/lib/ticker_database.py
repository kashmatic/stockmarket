from pymongo import MongoClient
from bson.objectid import ObjectId

import os

# client = MongoClient("mongodb://localhost:27017/stocks")
client = MongoClient(os.environ.get('MONGODB_URI'))

# from .mongo_database import client

class TickerDatabase():
    def __init__(self, symbol):
        self.db = client['stocks']
        self.symbol = symbol

    def get_stocksEarnings(self):
        return self.db[self.symbol].find_one({},{"stocksEarnings":1, "_id":0})['stocksEarnings']

    def get_stocksFinancials(self):
        return self.db[self.symbol].find_one({},{"stocksFinancials":1, "_id":0})['stocksFinancials']

    def get_stocksKeyStats(self):
        return self.db[self.symbol].find_one({},{"stocksKeyStats":1, "_id":0})['stocksKeyStats']

    def get_stocksQuote(self):
        return self.db[self.symbol].find_one({},{"stocksQuote":1, "_id":0})['stocksQuote']

    def get_stocksChart2y(self):
        return self.db[self.symbol].find_one({},{"stocksChart2y":1, "_id":0})['stocksChart2y']

    def get_finviz(self):
        return self.db[self.symbol].find_one({},{"finviz":1, "_id":0})['finviz']

    def add(self, key, jobj):
        id = self.db[self.symbol].find_one({}, {"_id": 1})
        if id:
            self.db[self.symbol].find_one_and_update(
                {"_id": ObjectId(id['_id'])},
                {"$set": {key: jobj} },
                upsert=True)
        else:
            self.db[self.symbol].insert({key: jobj})

    def put_stocksEarnings(self, jobj):
        print(os.environ.get('MONGODB_URI'))
        self.add("stocksEarnings", jobj)

    def put_stocksKeyStats(self, jobj):
        self.add("stocksKeyStats", jobj)

    def put_stocksFinancials(self, jobj):
        self.add("stocksFinancials", jobj)

    def put_stocksQuote(self, jobj):
        self.add("stocksQuote", jobj)

    def put_stocksChart2y(self, jobj):
        self.add("stocksChart2y", jobj)

    def put_finviz(self, jobj):
        self.add("finviz", jobj)
