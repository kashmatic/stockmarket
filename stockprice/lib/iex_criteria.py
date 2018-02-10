class IexCriteria:
    def __init__(self, symbol, stocksEarnings, stocksFinancials, stocksKeyStats, stocksQuote):
        self.symbol = symbol
        self.stocksEarnings = stocksEarnings
        self.stocksFinancials = stocksFinancials
        self.stocksKeyStats = stocksKeyStats
        self.stocksQuote = stocksQuote
        self.valuation = dict(
            marketcapMoreThan1B=0,
            debtRatioMarketcap=0,
            cashMoreThan1B=0,
            trailingPECalculate=0,
            score=0
        )

    def marketcapMoreThan1B(self, dollars):
        if 'marketcap' not in self.stocksKeyStats:
            return False, "marketcap is N/A"
        if self.stocksKeyStats['marketcap'] < dollars:
            return False, "marketcap < 1B\t${:,.2f}".format(self.stocksKeyStats['marketcap'])
        ## True
        self.valuation['marketcapMoreThan1B'] = self.stocksKeyStats['marketcap']
        return True, "marketcap > 1B\t${:,.2f}".format(self.stocksKeyStats['marketcap'])

    def debtRatioMarketcap(self, limit):
        if 'totalDebt' not in self.stocksFinancials:
            return False, "debt is N/A or 0"
        if self.stocksFinancials['totalDebt'] <= 0:
            return False, "debt is N/A or 0\t{}".format(self.stocksFinancials['totalDebt'])
        if self.stocksKeyStats['marketcap'] <= 0:
            return False, "marketcap <= 0"
        ratio = self.stocksFinancials['totalDebt'] / self.stocksKeyStats['marketcap']
        if ratio > limit:
            return False, "debt to marketcap ratio > {:,.2f}%\t{:,.2f}%".format(limit * 100, ratio * 100)
        ## True
        self.valuation['debtRatioMarketcap'] = ratio
        return True, "debt to marketcap ratio < {:,.2f}%\t{:,.2f}%".format(limit * 100, ratio * 100)

    def cashMoreThan1B(self, dollars):
        if not self.stocksFinancials['financials'][0]['currentCash']:
            return False, "currentCash is N/A"
        if self.stocksFinancials['financials'][0]['currentCash'] < dollars:
            return False, "currentCash < 1B\t${:,.2f}".format(self.stocksFinancials['financials'][0]['currentCash'])
        ## True
        self.valuation['cashMoreThan1B'] = self.stocksFinancials['financials'][0]['currentCash']
        return True, "currentCash > 1B\t${:,.2f}".format(self.stocksFinancials['financials'][0]['currentCash'])

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
            return False, "latestPrice / actualEPS > 15\t{:,.2f}".format(ratio)
        ## True
        self.valuation['quotePriceRatioEstimatedEPS'] = ratio
        return True, "latestPrice / actualEPS < 15\t{:,.2f}".format(ratio)

    def trailingPECalculate(self, limit):
        alist = []
        if 'sharesOutstanding' not in self.stocksKeyStats:
            return False, "sharesOutstanding is N/A"
        if self.stocksKeyStats['sharesOutstanding'] == 0:
            return False, "sharesOutstanding is 0"
        for report in self.stocksFinancials['financials']:
            if not report['netIncome']:
                return False, "netIncome is N/A"
            alist.append(report['netIncome'])
        # x = sum(alist)/len(alist)
        if sum(alist) <= 0:
            return False, "sum of netIncome <= 0"
        basicEPS = sum(alist) / self.stocksKeyStats['sharesOutstanding']
        trailingPE = self.stocksQuote['delayedPrice'] / basicEPS
        if trailingPE > limit or trailingPE < 0:
            return False, "feCalculate > 15\t{:,.2f}".format(trailingPE)
        ## True
        self.valuation['feCalculate'] = trailingPE
        return True, "feCalculate < 15\t{:,.2f}".format(trailingPE)

    def validate(self):
        fnlist = [
            self.marketcapMoreThan1B(1000000000),
            self.debtRatioMarketcap(0.5),
            self.cashMoreThan1B(1000000000),
            self.trailingPECalculate(15)
        ]

        for fn in fnlist:
            abool, msg = fn
            if not abool:
                return abool, msg
                # return "{}\t{}\n".format(self.symbol, msg)

        return True, self.valuation
        # return "{}\t{}\n".format(self.symbol, self.valuation)
