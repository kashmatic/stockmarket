from pymongo import MongoClient

from lib.iex import IEX

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']

iex = IEX()

for sym in iex.symbols():
    # if not sym.startswith('A'):
    #     continue
    print(sym)
    stocksEarnings = iex.stocksEarnings(sym)
    stocksFinancials = iex.stocksFinancials(sym)
    stocksKeyStats = iex.stocksKeyStats(sym)
    stocksQuote = iex.stocksQuote(sym)
    db[sym].insert({'stocksKeyStats': stocksKeyStats,
        'stocksFinancials': stocksFinancials,
        'stocksEarnings': stocksEarnings,
        'stocksQuote': stocksQuote})
