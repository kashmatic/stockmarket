from lib.iex import IEX
from lib.finviz import Finviz
from lib.ticker_database import TickerDatabase

import string

def iex_database(alist):
    for sym in alist:
        # if not sym.startswith('IDT'):
        # if sym[0] not in list(b):
        # if sym in ['SZC^#']:
            # continue
        print(sym)
        aiex = IEX(sym)
        stocksEarnings = aiex.stocksEarnings()
        stocksFinancials = aiex.stocksFinancials(sym)
        stocksKeyStats = aiex.stocksKeyStats(sym)
        stocksQuote = aiex.stocksQuote(sym)
        stocksChart2y = aiex.stocksChart2y(sym)

        td = TickerDatabase(sym)
        td.put_stocksEarnings(stocksEarnings)
        td.put_stocksFinancials(stocksFinancials)
        td.put_stocksKeyStats(stocksKeyStats)
        td.put_stocksQuote(stocksQuote)
        td.put_stocksChart2y(stocksChart2y)

def iex_database_update(alist):
    for sym in alist:
        print(sym)
        jobj = iex.stocksChart2y(sym)
        id = DB[sym].find_one({}, {"_id": 1})
        DB[sym].update_one(
            {"_id": ObjectId(id['_id'])},
            {"$set": {'stocksChart2y': jobj}},
            upsert=True
            )

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
    iex = IEX()
    list_of_symbols = iex.symbols()
    iex_database(list_of_symbols)
    # iex_database_update(iex.symbols())
    # finviz(list_of_symbols)
