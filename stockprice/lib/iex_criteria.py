class IexCriteria:
    def __init__(self, symbol, stocksEarnings, stocksFinancials, stocksKeyStats, stocksQuote):
        self.symbol = symbol
        self.stocksEarnings = stocksEarnings
        self.stocksFinancials = stocksFinancials
        self.stocksKeyStats = stocksKeyStats
        self.stocksQuote = stocksQuote

    def marketcapMoreThan1B(self):
        if 'marketcap' not in self.stocksKeyStats:
            return False, "marketcap is N/A"
        if self.stocksKeyStats['marketcap'] < 1000000000:
            return False, "marketcap < 1B\t${:,.2f}".format(self.stocksKeyStats['marketcap'])
        ## True
        return True, "marketcap > 1B\t${:,.2f}".format(self.stocksKeyStats['marketcap'])

    def debtRatioMarketcap(self):
        if 'debt' not in self.stocksKeyStats:
            return False, "debt is N/A or 0"
        if self.stocksKeyStats['debt'] <= 0:
            return False, "debt is N/A or 0\t{}".format(self.stocksKeyStats['debt'])
        ratio = self.stocksKeyStats['debt'] / self.stocksKeyStats['marketcap']
        if ratio > 0.5:
            return False, "debt to marketcap ratio > 50%\t{:,.2f}%".format(ratio*100)
        ## True
        return True, "debt to marketcap ratio < 50%\t{:,.2f}%".format(ratio * 100)

    def cashMoreThan1B(self):
        if 'cash' not in self.stocksKeyStats:
            return False, "cash is N/A"
        if self.stocksKeyStats['cash'] < 1000000000:
            return False, "cash < 1B\t${:,.2f}".format(self.stocksKeyStats['cash'])
        ## True
        return True, "cash > 1B\t${:,.2f}".format(self.stocksKeyStats['cash'])

    def quotePriceRatioEstimatedEPS(self):
        if 'earnings' not in self.stocksQuote:
            return False, "earnings is N/A"
        if not self.stocksQuote['earnings'][0]['actualEPS']:
            return False, "actualEPS is null"
        if self.stocksQuote['earnings'][0]['actualEPS'] <= 0:
            return False, "estimatedEPS is negative or 0\t${:,.2f}".format(self.stocksQuote['earnings'][0]['actualEPS'])
        if 'latestPrice' not in self.stocksEarnings:
            return False, "latestPrice is NA"
        ratio = self.stocksEarnings['latestPrice'] / self.stocksQuote['earnings'][0]['actualEPS']
        if ratio > 15:
            return False, "latestPrice / actualEPS > 15\t{:,.2f}%".format(ratio)
        ## True
        return True, "latestPrice / actualEPS < 15\t{:,.2f}%".format(ratio)

    def validate(self):
        abool, msg = self.marketcapMoreThan1B()
        if not abool:
            return "{}\t{}\n".format(self.symbol, msg)
        abool, msg = self.debtRatioMarketcap()
        if not abool:
            return "{}\t{}\n".format(self.symbol, msg)
        abool, msg = self.cashMoreThan1B()
        if not abool:
            return "{}\t{}\n".format(self.symbol, msg)
        abool, msg = self.quotePriceRatioEstimatedEPS()
        if not abool:
            return "{}\t{}\n".format(self.symbol, msg)
        return "{}\n".format('*'*50)
