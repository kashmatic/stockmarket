from pymongo import MongoClient

from lib.iex import IEX

client = MongoClient("mongodb://localhost:27017/stocks")
db = client['stocks']

iex = IEX()

for sym in iex.symbols():
    print(sym)
    stocksEarnings = iex.stocksEarnings(sym)
    db[sym].insert({'stocksEarnings': stocksEarnings})
    stocksFinancials = iex.stocksFinancials(sym)
    db[sym].insert({'stocksFinancials': stocksFinancials})
    stocksKeyStats = iex.stocksKeyStats(sym)
    db[sym].insert({'stocksKeyStats': stocksKeyStats})
    stocksQuote = iex.stocksQuote(sym)
    db[sym].insert({'stocksQuote': stocksQuote})
