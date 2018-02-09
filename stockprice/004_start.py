import asyncio
import random
import requests
import time

from lib.iex_criteria import IexCriteria

from aiohttp import ClientSession

OUTPUT = open('output.txt', 'w')

def get_symbols():
    URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
    r = requests.get(URL)
    return r.json()

async def mycoroutine(id):
    print(id)
    async with ClientSession() as session:
        # print(dir(session))
        async with session.get("https://api.iextrading.com/1.0/stock/{}/financials".format(id)) as response:
            stocksFinancials = await response.json()
        async with session.get("https://api.iextrading.com/1.0/stock/{}/earnings".format(id)) as response:
            stocksEarnings = await response.json()
        async with session.get("https://api.iextrading.com/1.0/stock/{}/stats".format(id)) as response:
            stocksKeyStats = await response.json()
        async with session.get("https://api.iextrading.com/1.0/stock/{}/quote".format(id)) as response:
            stocksQuote = await response.json()
        aobj = IexCriteria(id, stocksEarnings, stocksFinancials, stocksKeyStats, stocksQuote)
        OUTPUT.write(aobj.validate())
        # ALIST.append(aobj.validate())
        session.close()

async def todo():
    tasks = []
    # for id in ['CTRL', 'CTRN', 'CTRP', 'CTRV', 'CTS', 'CTSH', 'CTSO', 'CTT', 'CTU', 'CTV', 'CTW', 'CTWS', 'CTX', 'CTXR', 'CTXRW', 'CTXS', 'CTY', 'CTZ', 'CUB', 'CUBA']:
    for id in get_symbols():
        atime = random.randint(1,10)
        await asyncio.sleep(atime)
        # tasks.append(asyncio.ensure_future(mycoroutine(id)))
        tasks.append(asyncio.ensure_future(mycoroutine(id['symbol'])))

    await asyncio.gather(*tasks)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(todo())
    loop.close()

if __name__ == "__main__":
    x = time.time()
    main()
    OUTPUT.close()
    y = time.time()
    print("{:,.2f} secs".format(y-x))
