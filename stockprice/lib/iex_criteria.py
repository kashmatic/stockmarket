import yaml

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
            marketcapMoreThan=None,
            debtRatioMarketcapLessThan=None,
            cashMoreThan=None,
            peCalculateLessThan=None,
            ebitdaMoreThan=None,
            stocksChart1y=None,
            finvizPEttmLessThan=None,
            finvizPEforwardLessThan=None
        )

    def setMsg(self, key, value, msg):
        self.valuation[key]['value'] = value
        self.valuation[key]['msg'] = msg

    def marketcapMoreThan(self, dollars):
        key = 'marketcapMoreThan'
        if 'marketcap' not in self.stocksKeyStats:
            self.valuation[key] = 'N/A'
            return True
        if self.stocksKeyStats['marketcap'] < dollars:
            self.valuation[key] = "(${:,.2f})".format(self.stocksKeyStats['marketcap'])
            return False
        ## True
        self.valuation[key] = "${:,.2f}".format(self.stocksKeyStats['marketcap'])
        return True

    def debtRatioMarketcapLessThan(self, limit):
        key = 'debtRatioMarketcapLessThan'
        if 'debt' not in self.stocksKeyStats:
            self.valuation[key] = 'N/A'
            return True
        if self.stocksKeyStats['debt'] <= 0:
            self.valuation[key] = 'debt (${:,.2f})'.format(self.stocksKeyStats['debt'])
            return True
        if self.stocksKeyStats['marketcap'] <= 0:
            self.valuation[key] = 'marketcap (${:,.2f})'.format(self.stocksKeyStats['marketcap'])
            return False
        ratio = self.stocksKeyStats['debt'] / self.stocksKeyStats['marketcap']
        if ratio > limit:
            self.valuation[key] = '({:,.2f})'.format(ratio)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(ratio)
        return True

    def cashMoreThan(self, dollars):
        key = 'cashMoreThan'
        if not self.stocksFinancials['financials'][0]['currentCash']:
            self.valuation[key] = "N/A"
            return True
        if self.stocksFinancials['financials'][0]['currentCash'] < dollars:
            self.valuation[key] = "(${:,.2f})".format(self.stocksFinancials['financials'][0]['currentCash'])
            return False
        ## True
        self.valuation['cashMoreThan'] = "${:,.2f}".format(self.stocksFinancials['financials'][0]['currentCash'])
        return True

    # def quotePriceRatioEstimatedEPS(self):
    #     if 'earnings' not in self.stocksQuote:
    #         return False, "earnings is N/A"
    #     if not self.stocksQuote['earnings'][0]['actualEPS']:
    #         return False, "actualEPS is null"
    #     if self.stocksQuote['earnings'][0]['actualEPS'] <= 0:
    #         return False, "estimatedEPS is negative or 0\t${:,.2f}".format(self.stocksQuote['earnings'][0]['actualEPS'])
    #     if 'latestPrice' not in self.stocksEarnings:
    #         return False, "latestPrice is NA"
    #     ratio = self.stocksEarnings['latestPrice'] / self.stocksQuote['earnings'][0]['actualEPS']
    #     if ratio > 15:
    #         return False, "latestPrice / actualEPS > 15\t{:,.2f}".format(ratio)
    #     ## True
    #     self.valuation['quotePriceRatioEstimatedEPS'] = ratio
    #     return True, "latestPrice / actualEPS < 15\t{:,.2f}".format(ratio)

    def peCalculateLessThan(self, limit):
        alist = []
        key = 'peCalculateLessThan'
        if 'sharesOutstanding' not in self.stocksKeyStats:
            self.valuation[key] = 'N/A'
            return True
        if self.stocksKeyStats['sharesOutstanding'] == 0:
            self.valuation[key] = "sharesOutstanding (0)"
            return True
        for report in self.stocksFinancials['financials']:
            if not report['netIncome']:
                self.valuation[key] = 'netIncome (N/A)'
                return False
            alist.append(report['netIncome'])
        # x = sum(alist)/len(alist)
        if sum(alist) <= 0:
            self.valuation[key] = "sum of netIncome (${:,.2f})".format(sum(alist))
            return False
        basicEPS = sum(alist) / self.stocksKeyStats['sharesOutstanding']
        trailingPE = self.stocksQuote['delayedPrice'] / basicEPS
        if trailingPE > limit or trailingPE < 0:
            self.valuation[key] = "({:,.2f})".format(trailingPE)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(trailingPE)
        return True

    def ebitdaMoreThan(self, num):
        key = 'ebitdaMoreThan'
        if 'EBITDA' not in self.stocksKeyStats:
            self.valuation[key] = "(N/A)"
            return True
        if self.stocksKeyStats['EBITDA'] < num:
            self.valuation[key] = "({})".format(self.stocksKeyStats['EBITDA'])
            return False
        ## TRUE
        self.valuation[key] = "{}".format(self.stocksKeyStats['EBITDA'])
        return True

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

    def finvizPEttmLessThan(self, num):
        key = 'finvizPEttmLessThan'
        if not self.finviz or not self.finviz['P/E']:
            self.valuation[key] = "(N/A)"
            return True
        if float(self.finviz['P/E']) <= 0:
            self.valuation[key] = "({:,.2f})".format(float(self.finviz['P/E']))
            return False
        if float(self.finviz['P/E']) > num:
            self.valuation[key] = "({:,.2f})".format(float(self.finviz['P/E']))
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(float(self.finviz['P/E']))
        return True

    def finvizPEforwardLessThan(self, num):
        key = 'finvizPEforwardLessThan'
        if not self.finviz or not self.finviz['Forward P/E']:
            self.valuation[key] = "(N/A)"
            return True
        if float(self.finviz['Forward P/E']) <= 0:
            self.valuation[key] = "({:,.2f})".format(float(self.finviz['Forward P/E']))
            return False
        if float(self.finviz['Forward P/E']) > num:
            self.valuation[key] = "({:,.2f})".format(float(self.finviz['Forward P/E']))
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(float(self.finviz['Forward P/E']))
        return True

    def printMsg(self):
        alist = []
        for key in self.valuation:
            if self.valuation[key]:
                alist.append(self.valuation[key])
        return "\t".join(alist)

    def validate(self):
        adic = {
            'marketcapMoreThan': self.marketcapMoreThan,
            'debtRatioMarketcapLessThan': self.debtRatioMarketcapLessThan,
            'cashMoreThan': self.cashMoreThan,
            'peCalculateLessThan': self.peCalculateLessThan,
            'ebitdaMoreThan': self.ebitdaMoreThan,
            'finvizPEttmLessThan': self.finvizPEttmLessThan,
            'finvizPEforwardLessThan': self.finvizPEforwardLessThan
        }

        fh = open('settings.yaml')
        a = yaml.load(fh)
        fh.close()

        for b in a:
            # print(">>", a[b])
            if not a[b]['check']:
                continue
            fn = adic[b]
            val = a[b]['value']
            if not fn(val):
                return False, self.printMsg()

        return True, self.printMsg()

        # fnlist = [
        #     self.marketcapMoreThan(1000000000),
        #     self.debtRatioMarketcap(0.5),
        #     self.cashMoreThan(1000000000),
        #     # self.trailingPECalculate(15),
        #     self.ebitda(1),
        #     # self.volumeChange(100000, 3),
        #     self.finvizPEttm(15),
        #     # self.finvizPEforward(15),
        # ]

        # for fn in fnlist:
        #     abool, msg = fn
        #     if not abool:
        #         return abool, msg
