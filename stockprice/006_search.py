from pymongo import MongoClient
from time import localtime, strftime

from lib.iex import IEX
from lib.iex_criteria import IexCriteria
from lib.ticker_database import TickerDatabase
from lib.mongo_database import listTickers

import yaml

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
    aobj = IexCriteria(symbol)
    abool, msg = aobj.validate()
    # print(abool, msg)
    if abool:
        GOOD.write("{}\t{}\n".format(symbol, msg))
    else:
        BAD.write("{}\t{}\n".format(symbol, msg))

def each_symbol():
    for sym in listTickers():
        criteria(sym)

if __name__ == "__main__":
    GOOD.write("{}\n".format(columnHeader()))
    BAD.write("{}\n".format(columnHeader()))
    each_symbol()
    # criteria('A')
    GOOD.close()
    BAD.close()
