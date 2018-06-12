import yaml

from .ticker_database import TickerDatabase

class IexCriteria:
    def __init__(self, symbol):
        td = TickerDatabase(symbol)
        self.symbol = symbol
        self.stocksEarnings = td.get_stocksEarnings()
        self.stocksFinancials = td.get_stocksFinancials()
        self.stocksKeyStats = td.get_stocksKeyStats()
        self.stocksQuote = td.get_stocksQuote()
        self.stocksChart2y = td.get_stocksChart2y()
        self.finviz = td.get_finviz()
        self.valuation = dict(
            marketcapMoreThan=None,
            debtRatioMarketcapLessThan=None,
            cashMoreThan=None,
            peCalculateLessThan=None,
            ebitdaMoreThan=None,
            stocksChart2y=None,
            finvizPEttmLessThan=None,
            finvizPEforwardLessThan=None
        )

    def setMsg(self, key, value, msg):
        self.valuation[key]['value'] = value
        self.valuation[key]['msg'] = msg

    def get_marketcap(self):
        if not self.stocksKeyStats:
            return None
        if 'marketcap' in self.stocksKeyStats:
            val = int(self.stocksKeyStats['marketcap'])
            if val < 500000:
                return None
            return val
        else:
            return None

    def marketcapMoreThan(self, dollars):
        key = 'marketcapMoreThan'
        # if 'marketcap' not in self.stocksKeyStats:
        value = self.get_marketcap()
        if not value:
            self.valuation[key] = 'N/A'
            return True
        if value < dollars:
            self.valuation[key] = "(${:,.2f})".format(value)
            return False
        ## True
        self.valuation[key] = "${:,.2f}".format(value)
        return True

    def get_debt(self):
        if 'debt' in self.stocksKeyStats:
            return int(self.stocksKeyStats['debt'])
        else:
            return None

    def debtRatioMarketcapLessThan(self, limit):
        key = 'debtRatioMarketcapLessThan'
        debt = self.get_debt()
        marketcap = self.get_marketcap()
        # if 'debt' not in self.stocksKeyStats:
        if not debt:
            self.valuation[key] = 'N/A'
            return True
        if debt <= 0:
            self.valuation[key] = 'debt (${:,.2f})'.format(debt)
            return True
        if not marketcap:
            self.valuation[key] = 'marketcap (N/A)'
            return False
        if marketcap <= 0:
            self.valuation[key] = 'marketcap (${:,.2f})'.format(marketcap)
            return False
        ratio = debt / marketcap
        if ratio > limit:
            self.valuation[key] = '({:,.2f})'.format(ratio)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(ratio)
        return True

    def get_cash(self):
        if 'financials' in self.stocksFinancials:
            if len(self.stocksFinancials['financials']) <= 0:
                return None
            if 'currentCash' not in self.stocksFinancials['financials'][0]:
                return None
            if not self.stocksFinancials['financials'][0]['currentCash']:
                return None
            return int(self.stocksFinancials['financials'][0]['currentCash'])
        else:
            return None

    def cashMoreThan(self, dollars):
        key = 'cashMoreThan'
        cash = self.get_cash()
        # if not self.stocksFinancials['financials'][0]['currentCash']:
        if not cash:
            self.valuation[key] = "N/A"
            return True
        if cash < dollars:
            self.valuation[key] = "(${:,.2f})".format(cash)
            return False
        ## True
        self.valuation['cashMoreThan'] = "${:,.2f}".format(cash)
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

    def get_sharesoutstanding(self):
        if 'sharesOutstanding' in self.stocksKeyStats:
            return int(self.stocksKeyStats['sharesOutstanding'])
        else:
            return None

    def get_netIncome(self):
        alist = []
        if not self.stocksFinancials:
            return None
        for report in self.stocksFinancials['financials']:
            if not report['netIncome']:
                return None
            alist.append(int(report['netIncome']))
        return sum(alist)

    def get_delayedprice(self):
        if 'delayedPrice' in self.stocksQuote and self.stocksQuote['delayedPrice']:
            return int(self.stocksQuote['delayedPrice'])
        else:
            return 0

    def peCalculateLessThan(self, limit):
        key = 'peCalculateLessThan'
        shares = self.get_sharesoutstanding()
        # if 'sharesOutstanding' not in self.stocksKeyStats:
        if not shares:
            self.valuation[key] = 'N/A'
            return True
        if shares == 0:
            self.valuation[key] = "sharesOutstanding (0)"
            return True
        netIncome = self.get_netIncome()
        if not netIncome:
            self.valuation[key] = 'netIncome (N/A)'
            return False

        if netIncome <= 0:
            self.valuation[key] = "sum of netIncome (${:,.2f})".format(netIncome)
            return False
        basicEPS = netIncome / shares
        delayedPrice = self.get_delayedprice()
        trailingPE = delayedPrice / basicEPS
        if trailingPE > limit or trailingPE <= 0:
            self.valuation[key] = "({:,.2f})".format(trailingPE)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(trailingPE)
        return True

    def get_ebitda(self):
        if 'EBITDA' in self.stocksKeyStats:
            return self.stocksKeyStats['EBITDA']
        else:
            return None

    def ebitdaMoreThan(self, num):
        key = 'ebitdaMoreThan'
        ebitda = self.get_ebitda()
        # if 'EBITDA' not in self.stocksKeyStats:
        if not ebitda:
            self.valuation[key] = "(N/A)"
            return True
        if ebitda < num:
            self.valuation[key] = "({})".format(ebitda)
            return False
        ## TRUE
        self.valuation[key] = "{}".format(ebitda)
        return True

    def volumeChange(self, threshold, num):
        alist = []
        if not self.stocksChart2y:
            return False, "No Chart 2y"
        for item in self.stocksChart2y:
            alist.append(item['volume'])
            # print(item['volume'])
        # tsum = sum(alist)/52
        tsum = sum(alist)/104
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
        ## True
        self.valuation['stocksChart2y'] = ratio
        return True, "Last 7 days ratio > {}\t{}".format(num, ratio)

    def get_finvizpettm(self):
        if not self.finviz or 'P/E' not in self.finviz or not self.finviz['P/E']:
            return None
        return float(self.finviz['P/E'])

    def finvizPEttmLessThan(self, num):
        key = 'finvizPEttmLessThan'
        pettm = self.get_finvizpettm()
        # if not self.finviz or not self.finviz['P/E']:
        if not pettm:
            self.valuation[key] = "(N/A)"
            return True
        if pe <= 0:
            self.valuation[key] = "({:,.2f})".format(pettm)
            return False
        if pettm > num:
            self.valuation[key] = "({:,.2f})".format(pettm)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(pettm)
        return True

    def get_finvizpeforward(self):
        if not self.finviz or 'Forward P/E' not in self.finviz or not self.finviz['Forward P/E']:
            return None
        return float(self.finviz['Forward P/E'])

    def finvizPEforwardLessThan(self, num):
        key = 'finvizPEforwardLessThan'
        peforward = self.get_finvizpeforward()
        # if not self.finviz or not self.finviz['Forward P/E']:
        if not peforward:
            self.valuation[key] = "(N/A)"
            return True
        if peforward <= 0 or peforward > num:
            self.valuation[key] = "({:,.2f})".format(peforward)
            return False
        ## True
        self.valuation[key] = "{:,.2f}".format(peforward)
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
