import asyncio
import random
import aiohttp
import async_timeout
import requests

from lib.iex_criteria import IexCriteria
from lib.ticker_database import TickerDatabase

URL_stocksFinancials = 'https://api.iextrading.com/1.0/stock/{}/financials'
URL_stocksEarnings = 'https://api.iextrading.com/1.0/stock/{}/earnings'
URL_stocksKeyStats = 'https://api.iextrading.com/1.0/stock/{}/stats'
URL_stocksQuote = 'https://api.iextrading.com/1.0/stock/{}/quote'
URL_stocksChart2y = 'https://api.iextrading.com/1.0/stock/{}/chart/2y'

def printit(symbol, args):
    print("{}\t{}\t{}".format(symbol, args[0], args[1]))

def get_symbols():
    URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
    r = requests.get(URL)
    return r.json()

async def fetch(session, url):
    with async_timeout.timeout(10):
        try:
            async with session.get(url) as response:
                return await response.json()
        except Exception as e:
            print(">>>", url)
            return None

async def financials(symbol):
    async with aiohttp.ClientSession() as session:
        stocksFinancials = await fetch(session, URL_stocksFinancials.format(symbol))
        stocksEarnings = await fetch(session, URL_stocksEarnings.format(symbol))
        stocksKeyStats = await fetch(session, URL_stocksKeyStats.format(symbol))
        stocksQuote = await fetch(session, URL_stocksQuote.format(symbol))
        stocksChart2y = await fetch(session, URL_stocksChart2y.format(symbol))
        print(symbol)
        print(stocksFinancials.keys())
        print(stocksEarnings.keys())
        print(stocksKeyStats.keys())
        print(stocksQuote.keys())
        print(stocksChart2y.keys())

        td = TickerDatabase(symbol)
        td.put_stocksEarnings(stocksEarnings)
        td.put_stocksFinancials(stocksFinancials)
        td.put_stocksKeyStats(stocksKeyStats)
        td.put_stocksQuote(stocksQuote)
        td.put_stocksChart2y(stocksChart2y)

async def todo(symbols_list):
    for item in symbols_list:
        asyncio.sleep(range(0, 5))
        await financials(item['symbol'])

def main():
    symbols_list = get_symbols()
    i = 0
    tasks = []
    loop = asyncio.get_event_loop()
    for item in symbols_list:
        # print(item)
        tasks.append(financials(item['symbol']))
        if i < 50:
            i = i + 1
            # print(i)
        else:
            asyncio.sleep(range(0, 10))
            # print(len(tasks))
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
            if asyncio.get_event_loop().is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            print('*'*100)
            i = 0
            tasks = []
    # if asyncio.get_event_loop().is_closed():
    #     asyncio.set_event_loop(asyncio.new_event_loop())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(todo(symbols_list))
    # loop.close()

if __name__ == "__main__":
    main()
