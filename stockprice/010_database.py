from lib.iex import IEX
from lib.finviz import Finviz
from lib.ticker_database import TickerDatabase
from lib.myasync import MyAsync

import string
import asyncio
import time

iex = IEX()

async def se(sym):
    return iex.stocksEarnings(sym)

async def sf(sym):
    return iex.stocksFinancials(sym)

async def sks(sym):
    return iex.stocksKeyStats(sym)

async def sq(sym):
    return iex.stocksQuote(sym)

async def sc2y(sym):
    return iex.stocksChart2y(sym)

async def iex_database(sym):
    # for sym in alist:
        # if not sym.startswith('A'):
        # if sym[0] not in list(b):
        # if sym in ['SZC^#']:
            # continue
    print(">> begin", sym)
    stocksEarnings = await se(sym)
    stocksFinancials = await sf(sym)
    stocksKeyStats = await sks(sym)
    stocksQuote = await sq(sym)
    stocksChart2y = await sc2y(sym)

    print(">> end", sym)

        # td = TickerDatabase(sym)
        # td.put_stocksEarnings(stocksEarnings)
        # td.put_stocksFinancials(stocksFinancials)
        # td.put_stocksKeyStats(stocksKeyStats)
        # td.put_stocksQuote(stocksQuote)
        # td.put_stocksChart2y(stocksChart2y)


def finviz(alist):
    for sym in alist:
        print(sym)
        f = Finviz()
        jobj = f.get_stat(sym)
        td = TickerDatabase(sym)
        td.put_finviz(jobj)
        # id = DB[sym].find_one({}, {"_id": 1})
        # DB[sym].update_one({"_id": ObjectId(id['_id'])}, {"$set": {'finviz': jobj}})

if __name__ == "__main__":
    startTime = time.time()
    # print(iex.get_symbol())
    i = 0
    aMultiTask = MyAsync()

    for sym in iex.symbols():
        print(sym)
        if i < 100:
            aMultiTask.add(iex_database(sym))
            i = i + 1
            print('*'*100)
        else:
            i = 0
            aMultiTask.add(iex_database(sym))
            aMultiTask.run()
            asyncio.sleep(range(0, 5))
            aMultiTask = MyAsync()

    # iex_database(list_of_symbols)
    # iex_database_update(iex.symbols())
    # finviz(list_of_symbols)
