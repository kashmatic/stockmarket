from pymongo import MongoClient
from bson.objectid import ObjectId

from lib.iex import IEX
from lib.finviz import Finviz

import string

client = MongoClient("mongodb://localhost:27017/stocks")
DB = client['stocks']

def iex_database(alist):
    # a = string.ascii_uppercase
    # b = a.replace('ABCDEFGHIJKLMNOPQR', '')
    for sym in alist:
        if not sym.startswith('A'):
        # if sym[0] not in list(b):
        # if sym in ['SZC^#']:
            continue
        print(sym)
        stocksEarnings = iex.stocksEarnings(sym)
        stocksFinancials = iex.stocksFinancials(sym)
        stocksKeyStats = iex.stocksKeyStats(sym)
        stocksQuote = iex.stocksQuote(sym)
        stocksChart1y = iex.stocksChart1y(sym)
        DB[sym].insert({'stocksKeyStats': stocksKeyStats,
            'stocksFinancials': stocksFinancials,
            'stocksEarnings': stocksEarnings,
            'stocksQuote': stocksQuote,
            'stocksChart1y': stocksChart1y})

def iex_database_update(alist):
    for sym in alist:
        print(sym)
        jobj = iex.stocksChart1y(sym)
        id = DB[sym].find_one({}, {"_id": 1})
        DB[sym].update_one({"_id": ObjectId(id['_id'])}, {"$set": {'stocksChart1y': jobj}})

def finviz(alist):
    for sym in alist:
        print(sym)
        f = Finviz()
        jobj = f.get_stat(sym)
        id = DB[sym].find_one({}, {"_id": 1})
        DB[sym].update_one({"_id": ObjectId(id['_id'])}, {"$set": {'finviz': jobj}})

if __name__ == "__main__":
    iex = IEX()
    iex_database(iex.symbols())
    # iex_database_update(iex.symbols())
    # finviz(iex.symbols())
