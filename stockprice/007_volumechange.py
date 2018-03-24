from pymongo import MongoClient

from lib.iex_criteria import IexCriteria
from lib.mongo_database import listTickers

import yaml
from datetime import date as datetoday

THRESHOLD = 10000000
RATIO = 3

today = datetoday.today().strftime("%Y%m%d")
good = open("{}_volumechange.good".format(today), "w")
bad = open("{}_volumechange.bad".format(today), "w")

def criteria(symbol):
    aobj = IexCriteria(symbol)
    abool, msg = aobj.volumeChange(THRESHOLD, RATIO)
    if abool:
        good.write("{}\t{}\t{}\n".format(symbol, abool, msg))
    else:
        bad.write("{}\t{}\t{}\n".format(symbol, abool, msg))

def each_symbol():
    for sym in listTickers():
        criteria(sym)

if __name__ == "__main__":
    each_symbol()
    good.close()
    bad.close()
    # criteria('A')
