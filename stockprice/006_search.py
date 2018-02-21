from pymongo import MongoClient
from time import localtime, strftime

from lib.iex import IEX
from lib.iex_criteria import IexCriteria

import yaml

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']
astr = strftime("%Y%m%d_%H%M%S", localtime())
GOOD = open(astr+"_search.out", "w")
BAD = open(astr+"_search.err", "w")

def columnHeader():
    fh = open('settings.yaml')
    a = yaml.load(fh)

    alist = [" "]
    for b in a:
        if not a[b]['check']:
            continue
        alist.append("{}({})".format(b, a[b]['value']))

    return "\t".join(alist)
    fh.close()

def criteria(symbol):
    aobj = IexCriteria(symbol,
        db[symbol].find_one({},{"stocksEarnings":1, "_id":0})['stocksEarnings'],
        db[symbol].find_one({},{"stocksFinancials":1, "_id":0})['stocksFinancials'],
        db[symbol].find_one({},{"stocksKeyStats":1, "_id":0})['stocksKeyStats'],
        db[symbol].find_one({},{"stocksQuote":1, "_id":0})['stocksQuote'],
        db[symbol].find_one({},{"stocksChart1y":1, "_id":0})['stocksChart1y'],
        [])
        # db[symbol].find_one({},{"finviz":1, "_id":0})['finviz'])
    # aobj.newtest()
    abool, msg = aobj.validate()
    print(abool, msg)
    if abool:
        GOOD.write("{}\t{}\n".format(symbol, msg))
    else:
        BAD.write("{}\t{}\n".format(symbol, msg))

def each_symbol():
    for sym in db.collection_names():
        print(sym)
        criteria(sym)
        print('*'*100)

if __name__ == "__main__":
    GOOD.write("{}\n".format(columnHeader()))
    BAD.write("{}\n".format(columnHeader()))
    each_symbol()
    # criteria('A')
    GOOD.close()
    BAD.close()
