from lib.iex import IEX
from lib.finviz import Finviz
from lib.ticker_database import TickerDatabase

import string
import argparse

def iex_database(alist, fh):
    for sym in alist:
        # if not sym.startswith('IDT'):
        # if sym[0] not in list(b):
        # if sym not in ['TIBR']:
        if not sym.startswith('ZA'):
            continue
        print(sym)
        fh.write('{}\n'.format(sym))
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

def finviz(alist, fh):
    for sym in alist:
        if not sym.startswith('ZA'):
            continue
        print(sym)
        fh.write('{}\n'.format(sym))
        f = Finviz()
        jobj = f.get_stat(sym)
        td = TickerDatabase(sym)
        td.put_finviz(jobj)
        # id = DB[sym].find_one({}, {"_id": 1})
        # DB[sym].update_one({"_id": ObjectId(id['_id'])}, {"$set": {'finviz': jobj}})

def get_variables():
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('-t', '--type', type=str, help='data source', choices=("iex", "finviz"), required=True)
    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    adic = get_variables()
    iex = IEX()
    list_of_symbols = iex.symbols()
    if adic['type'] == 'iex':
        fh = open('iex.out', 'w')
        iex_database(list_of_symbols, fh)
        fh.close()
    elif adic['type'] == 'finviz':
        fh = open('finviz.out', 'w')
        finviz(list_of_symbols, fh)
        fh.close()
    else:
        print('ERROR: unknown data source')
