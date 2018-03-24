from pymongo import MongoClient

from lib.iex_criteria import IexCriteria
from lib.mongo_database import listTickers

import yaml

THRESHOLD = 10000000
RATIO = 3

def criteria(symbol):
    aobj = IexCriteria(symbol)
    abool, msg = aobj.volumeChange(THRESHOLD, RATIO)
    if abool:
        print(symbol, abool, msg)

def each_symbol():
    for sym in listTickers():
        criteria(sym)

if __name__ == "__main__":
    each_symbol()
    # criteria('A')
