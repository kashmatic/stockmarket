from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/stocks")

db = client['stocks']

for sym in db.collection_names():
    print(sym)
    # db[sym].find({}, {"stocksFinancials.financials.totalDebt": 1, "_id": 0})
