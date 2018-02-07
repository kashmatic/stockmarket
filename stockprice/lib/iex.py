import requests
URL = 'https://api.iextrading.com/1.0/'

class IEX:
    def __init__(self):
        pass

    def symbols_list(self):
        url = URL + 'ref-data/symbols'
        return self.get_data(url)

    def get_data(self, url):
        r = requests.get(url)
        return r.json()

    def symbols(self):
        alist = self.symbols_list()
        for item in alist:
            yield item['symbol']

    def symbols_count(self):
        return len(self.symbols_list())

    def stocksKeyStats(self, symbol):
        url = '{}/stock/{}/stats'.format(URL, symbol)
        return self.get_data(url)

    def stocksFinancials(self, symbol):
        url = '{}/stock/{}/financials'.format(URL, symbol)
        return self.get_data(url)

if __name__ == '__main__':
    pass
