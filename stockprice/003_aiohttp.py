import asyncio
import random
import aiohttp
import async_timeout
import requests

from lib.iex_criteria import IexCriteria

URL_stocksFinancials = 'https://api.iextrading.com/1.0/stock/{}/financials'
URL_stocksEarnings = 'https://api.iextrading.com/1.0/stock/{}/earnings'
URL_stocksKeyStats = 'https://api.iextrading.com/1.0/stock/{}/stats'
URL_stocksQuote = 'https://api.iextrading.com/1.0/stock/{}/quote'

def printit(symbol, args):
    print("{}\t{}\t{}".format(symbol, args[0], args[1]))

def get_symbols():
    URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
    r = requests.get(URL)
    return r.json()

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.json()

async def financials(symbol):
    async with aiohttp.ClientSession() as session:
        stocksFinancials = await fetch(session, URL_stocksFinancials.format(symbol))
        stocksEarnings = await fetch(session, URL_stocksEarnings.format(symbol))
        stocksKeyStats = await fetch(session, URL_stocksKeyStats.format(symbol))
        stocksQuote = await fetch(session, URL_stocksQuote.format(symbol))
        ic = IexCriteria(stocksEarnings, stocksFinancials, stocksKeyStats, stocksQuote)
        bool_marketcapMoreThan1B, msg_marketcapMoreThan1B = ic.marketcapMoreThan1B()
        print("{}\t{}\t{}".format(symbol, bool_marketcapMoreThan1B, msg_marketcapMoreThan1B))

async def todo(symbols_list):
    for item in symbols_list:
        await financials(item['symbol'])

def main():
    symbols_list = get_symbols()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(todo(symbols_list))
    loop.close()

if __name__ == "__main__":
    main()
