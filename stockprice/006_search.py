from pymongo import MongoClient
from time import localtime, strftime

from lib.iex import IEX
from lib.iex_criteria import IexCriteria

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']
astr = strftime("%Y%m%d_%H%M%S", localtime())
GOOD = open(astr+"search.out", "w")
BAD = open(astr+"search.err", "w")


def criteria(symbol):
    aobj = IexCriteria(symbol,
        db[symbol].find_one({},{"stocksEarnings":1, "_id":0})['stocksEarnings'],
        db[symbol].find_one({},{"stocksFinancials":1, "_id":0})['stocksFinancials'],
        db[symbol].find_one({},{"stocksKeyStats":1, "_id":0})['stocksKeyStats'],
        db[symbol].find_one({},{"stocksQuote":1, "_id":0})['stocksQuote'])
    abool, msg = aobj.validate()
    if abool:
        GOOD.write("{}\t{}\n".format(symbol, msg))
    else:
        BAD.write("{}\t{}\n".format(symbol, msg))

def each_symbol():
    for sym in db.collection_names():
        print(sym)
        criteria(sym)

if __name__ == "__main__":
    each_symbol()
    # criteria('A')
    GOOD.close()
    BAD.close()
