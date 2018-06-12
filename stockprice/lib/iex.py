import requests
import aiohttp

URL = 'https://api.iextrading.com/1.0/'

class IEX:
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.obj = {}
        if symbol:
            self.obj = self.batch_call()

    def symbols_list(self):
        url = URL + 'ref-data/symbols'
        return self.get_data(url)

    def batch_call(self):
        url = "{}/stock/{}/batch?types=quote,earnings,stats,financials,chart&range=2y".format(URL, self.symbol)
        return self.get_data(url)

    def sync_call(self):
        with async_timeout.timeout(10):
            with session.get(url) as response:
                return response.json()

    def get_data(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def symbols(self):
        alist = []
        for item in self.symbols_list():
            alist.append(item['symbol'])
        return alist

    def symbols_count(self):
        return len(self.symbols_list())

    def stocksEarnings(self):
        # url = '{}/stock/{}/earnings'.format(URL, symbol)
        # return self.get_data(url)
        # print(self.obj.keys())
        if not self.obj:
            return None
        if not 'earnings' in self.obj:
            return None
        if not 'earnings' in self.obj['earnings']:
            return None
        return self.obj['earnings']['earnings']

    def stocksFinancials(self, symbol):
        url = '{}/stock/{}/financials'.format(URL, symbol)
        return self.get_data(url)

    def stocksKeyStats(self, symbol):
        # url = '{}/stock/{}/stats'.format(URL, symbol)
        # return self.get_data(url)
        if not self.obj:
            return None
        if not 'stats' in self.obj:
            return None
        return self.obj['stats']

    def stocksQuote(self, symbol):
        # url = '{}/stock/{}/quote'.format(URL, symbol)
        # return self.get_data(url)
        if not self.obj:
            return None
        if not 'quote' in self.obj:
            return None
        return self.obj['quote']

    def stocksChart1y(self, symbol):
        url = '{}/stock/{}/chart/1y'.format(URL, symbol)
        return self.get_data(url)

    def stocksChart2y(self, symbol):
        # url = '{}/stock/{}/chart/2y'.format(URL, symbol)
        # return self.get_data(url)
        if not self.obj:
            return None
        if not 'chart' in self.obj:
            return None
        return self.obj['chart']


if __name__ == '__main__':
    pass
