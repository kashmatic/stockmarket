class IexCriteria:
    def __init__(self,
            symbol,
            stocksEarnings,
            stocksFinancials,
            stocksKeyStats,
            stocksQuote,
            stocksChart1y,
            finviz):
        self.symbol = symbol
        self.stocksEarnings = stocksEarnings
        self.stocksFinancials = stocksFinancials
        self.stocksKeyStats = stocksKeyStats
        self.stocksQuote = stocksQuote
        self.stocksChart1y = stocksChart1y
        self.finviz = finviz
        self.valuation = dict(
            marketcapMoreThan1B=None,
            debtRatioMarketcap=None,
            cashMoreThan1B=None,
            peCalculate=None,
            ebitda=None,
            stocksChart1y=None,
            finvizPEttm=None,
            finvizPEforward=None,
            score=None
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
        if 'debt' not in self.stocksKeyStats or self.stocksKeyStats['debt'] == 0:
            return True, "debt is N/A or 0"
        if self.stocksKeyStats['debt'] <= 0:
            return False, "debt is N/A or 0\t{}".format(self.stocksKeyStats['debt'])
        if self.stocksKeyStats['marketcap'] <= 0:
            return False, "marketcap <= 0"
        ratio = self.stocksKeyStats['debt'] / self.stocksKeyStats['marketcap']
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
            return False, "peCalculate > 15\t{:,.2f}".format(trailingPE)
        ## True
        self.valuation['peCalculate'] = trailingPE
        return True, "peCalculate < 15\t{:,.2f}".format(trailingPE)

    def ebitda(self, num):
        if 'EBITDA' not in self.stocksKeyStats:
            return False, "EBITDA is N/A"
        if self.stocksKeyStats['EBITDA'] < num:
            return False, "EBITDA < {}\t{}".format(num, self.stocksKeyStats['EBITDA'])
        ## TRUE
        self.valuation['ebitda'] = self.stocksKeyStats['EBITDA']
        return True, "EBITDA > {}\t{}".format(num, self.stocksKeyStats['EBITDA'])

    def volumeChange(self, threshold, num):
        alist = []
        for item in self.stocksChart1y:
            alist.append(item['volume'])
            # print(item['volume'])
        tsum = sum(alist)/52
        if tsum < threshold:
            return False, "Average volume < {}\t{}".format(threshold, tsum)
        last5 = sum(alist[-5:])
        if last5 < 2000000:
            return False, "Last 7 days volume < 2000000\t{}".format(tsum)
        if tsum == 0:
            return False, "Last 7 days is 0\t{}".format(tsum)
        ratio = last5/tsum
        if ratio < num:
            return False, "Last 7 days ratio < {}\t{}".format(num, ratio)
        # print(tsum, last5, last5/tsum)
        # print(self.stocksKeyStats['marketcap'])
        ## True
        self.valuation['stocksChart1y'] = ratio
        return True, "Last 7 days ratio > {}\t{}".format(num, ratio)

    def finvizPEttm(self, num):
        if not self.finviz['P/E']:
            return False, "Finviz P/E(ttm) \tN/A"
        if float(self.finviz['P/E']) <= 0:
            return False, "Finviz P/E(ttm) <= 0\t{}".format(self.finviz['P/E'])
        if float(self.finviz['P/E']) > num:
            return False, "Finviz P/E(ttm) > {}\t{}".format(num, self.finviz['P/E'])
        # print(self.finviz['P/E'])
        # print(self.finviz['Forward P/E'])
        ## True
        self.valuation['finvizPEttm'] = self.finviz['P/E']
        return True, "Finviz P/E(ttm) < {}\t{}".format(num, self.finviz['P/E'])

    def finvizPEforward(self, num):
        if not self.finviz['Forward P/E']:
            return False, "Finviz Fwd P/E \tN/A"
        if float(self.finviz['Forward P/E']) <= 0:
            return False, "Finviz Fwd P/E <= 0\t{}".format(self.finviz['Forward P/E'])
        if float(self.finviz['Forward P/E']) > num:
            return False, "Finviz Fwd P/E > {}\t{}".format(num, self.finviz['Forward P/E'])
        # print(self.finviz['P/E'])
        # print(self.finviz['Forward P/E'])
        ## True
        self.valuation['finvizPEforward'] = self.finviz['Forward P/E']
        return True, "Finviz Fwd P/E < {}\t{}".format(num, self.finviz['Forward P/E'])

    def validate(self):
        fnlist = [
            self.marketcapMoreThan1B(1000000000),
            self.debtRatioMarketcap(0.5),
            self.cashMoreThan1B(1000000000),
            self.trailingPECalculate(15),
            self.ebitda(1),
            # self.volumeChange(100000, 3),
            # self.finvizPEttm(15),
            # self.finvizPEforward(15),
        ]

        for fn in fnlist:
            abool, msg = fn
            if not abool:
                return abool, msg
                # return "{}\t{}\n".format(self.symbol, msg)

        return True, "marketcapMoreThan1B(${:,.2f})\tdebtRatioMarketcap({:,.2f})\tcashMoreThan1B(${:,.2f})\tpeCalculate({:,.2f})\tebitda({})".format(
            self.valuation['marketcapMoreThan1B'],
            self.valuation['debtRatioMarketcap'],
            self.valuation['cashMoreThan1B'],
            self.valuation['peCalculate'],
            self.valuation['ebitda'],
            # self.valuation['stocksChart1y']
            )
        # return True, "marketcapMoreThan1B (${:,.2f})\tratio ({:,.2f})".format(
        #     self.valuation['marketcapMoreThan1B'],
        #     self.valuation['stocksChart1y']
        #     )
        # return True, "Finviz P/E(ttm)\t{:,.2f}\tFinviz Fwd P/E\t{:,.2f}".format(
        #     float(self.valuation['finvizPEttm']),
        #     float(self.valuation['finvizPEforward'])
        #     )
        # return "{}\t{}\n".format(self.symbol, self.valuation)
