import asyncio

async def iex_database(alist):
    for sym in alist:
        # if not sym.startswith('IDT'):
        # if sym[0] not in list(b):
        # if sym in ['SZC^#']:
            # continue
        print(sym)
        return await IEX(sym)
        # stocksEarnings = aiex.stocksEarnings()
        # stocksFinancials = aiex.stocksFinancials(sym)
        # stocksKeyStats = aiex.stocksKeyStats(sym)
        # stocksQuote = aiex.stocksQuote(sym)
        # stocksChart2y = aiex.stocksChart2y(sym)

        # td = TickerDatabase(sym)
        # td.put_stocksEarnings(stocksEarnings)
        # td.put_stocksFinancials(stocksFinancials)
        # td.put_stocksKeyStats(stocksKeyStats)
        # td.put_stocksQuote(stocksQuote)
        # td.put_stocksChart2y(stocksChart2y)

async def main():
    alist = ['AAPL']
    loop = asyncio.get_event_loop()
