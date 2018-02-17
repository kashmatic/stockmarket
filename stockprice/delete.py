from pymongo import MongoClient

import string

client = MongoClient("mongodb://localhost:27017/stocks")

db = client['stocks']

for sym in db.collection_names():
    print(sym)
    # db[sym].find({}, {"stocksFinancials.financials.totalDebt": 1, "_id": 0})
    if not sym.startswith('S'):
        db[sym].drop()
