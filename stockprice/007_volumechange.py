from pymongo import MongoClient

from lib.iex_criteria import IexCriteria

import yaml

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']
THRESHOLD = 10000000
RATIO = 3

def criteria(symbol):
    aobj = IexCriteria(symbol,
        db[symbol].find_one({},{"stocksEarnings":1, "_id":0})['stocksEarnings'],
        db[symbol].find_one({},{"stocksFinancials":1, "_id":0})['stocksFinancials'],
        db[symbol].find_one({},{"stocksKeyStats":1, "_id":0})['stocksKeyStats'],
        db[symbol].find_one({},{"stocksQuote":1, "_id":0})['stocksQuote'],
        db[symbol].find_one({},{"stocksChart2y":1, "_id":0})['stocksChart2y'],
        db[symbol].find_one({},{"finviz":1, "_id":0})['finviz'])
    abool, msg = aobj.volumeChange(THRESHOLD, RATIO)
    print(abool, msg)

def each_symbol():
    for sym in db.collection_names():
        print(sym)
        criteria(sym)
        # print('*'*100)

if __name__ == "__main__":
    each_symbol()
    # criteria('A')
