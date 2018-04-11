from xbrl import XBRLParser
import requests
import re
import io

MEGADIC = {
    'Fiscal Year End Date': 'dei:CurrentFiscalYearEndDate',
    'Fiscal Period Focus': 'dei:DocumentFiscalPeriodFocus',
    'Fiscal Year Focus': 'dei:DocumentFiscalYearFocus',
    'Type': 'dei:DocumentType',
    'Balance Sheet > Cash and Cash equivalents': 'us-gaap:CashAndCashEquivalentsAtCarryingValue',
    # 'Balance Sheet > Short Term Investments': 'us-gaap:AvailableForSaleSecuritiesCurrent',
    # 'Balance Sheet > Net Receivables': 'us-gaap:AccountsReceivableNetCurrent',
    # 'Balance Sheet > Inventory': 'us-gaap:InventoryFinishedGoodsNetOfReserves',
    # 'Balance Sheet > Other Current Assets': 'us-gaap:OtherAssetsCurrent',
    # 'Balance Sheet > Total Current Assets': 'us-gaap:AssetsCurrent',
}

class MyXBRL():
    def __init__(self, url):
        self.page = self.get_page(url)
        self.context = None

    def get_page(self, url):
        page = requests.get(url)
        xbrl_parser = XBRLParser()
        # print(dir(xbrl_parser))
        b = io.StringIO(page.text)
        obj = xbrl_parser.parse(b)
        # print(obj)
        return obj

    def get_context(self):
        item = self.dothis('dei:CurrentFiscalYearEndDate')
        # print("22: ",item)
        return item['contextref']

    def dothis(self, tag):
        obj = self.page.find_all(name=re.compile(tag, re.IGNORECASE))
        # print("40: ", len(obj))
        # print(obj)
        if len(obj) == 0:
            return None
        elif len(obj) == 1:
            # return obj[0]['contextref']
            return obj[0]
        else:
            context = self.get_context()
            # print("49: ", context[-10:])
            for aobj in obj:
                # print(aobj['contextref'])
                print(aobj)
                # if aobj['contextref'][-10:] == context[-10:]:
                    # return aobj
            return None

    def check_if_none(self, val):
        # print("44: ", val)
        if val:
            return val.string
        else:
            return val

    def get_numbers(self):
        adic = {}
        for key, value in MEGADIC.items():
            output = self.dothis(value)
            adic[key] = self.check_if_none(output)
        return adic

    def inventoryNet(self):
        val = self.dothis('us-gaap:InventoryFinishedGoodsNetOfReserves')
        return self.check_if_none(val)

    def extract(self):
        alist = {
            'Income Statement > Total Revenue': 'us-gaap:SalesRevenueNet',
            # 'Income Statement > Cost of Revenue': 'us-gaap:CostOfGoodsAndServicesSold',

            'Balance Sheet > Long Term Investments': 'us-gaap:AvailableForSaleSecuritiesNoncurrent',
            'Balance Sheet > Property Plant and Equipment': 'us-gaap:PropertyPlantAndEquipmentNet',
            'Balance Sheet > Goodwill': 'us-gaap:Goodwill',
            # 'Balance Sheet > Accumulated Amortization'
            'Balance Sheet > Intangible Assets': 'us-gaap:IntangibleAssetsNetExcludingGoodwill',
            'Balance Sheet > Other Assets': 'us-gaap:OtherAssetsNoncurrent',
            'Balance Sheet > Total Assets': 'us-gaap:Assets',
            # 'Balance Sheet > Accounts Payable'
            # 'Balance Sheet > Short/Current Long Term Debt'
            'Balance Sheet > Other Current Liabilities': 'us-gaap:DeferredRevenueCurrent',
            'Balance Sheet > Total Current Liabilities': 'us-gaap:LiabilitiesCurrent',
            'Balance Sheet > Long Term Debt': 'us-gaap:LongTermDebtNoncurrent',
            'Balance Sheet > Other Liabilities': 'us-gaap:OtherLiabilitiesNoncurrent',
            'Balance Sheet > Deferred Long Term Liability Charges': 'us-gaap:DeferredRevenueNoncurrent',
            # 'Balance Sheet > Minority Interest'
            # 'Balance Sheet > Negative Goodwill'
            'Balance Sheet > Total Liabilities': 'us-gaap:Liabilities',
            # 'Balance Sheet > Misc. Stocks Options Warrants'
            # 'Balance Sheet > Redeemable Preferred Stock'
            # 'Balance Sheet > Preferred Stock'
            'Balance Sheet > Common Stock': 'us-gaap:CommonStocksIncludingAdditionalPaidInCapital',
            'Balance Sheet > Retained Earnings': 'us-gaap:RetainedEarningsAccumulatedDeficit',
            # 'Balance Sheet > Treasury Stock'
            # 'Balance Sheet > Capital Surplus'
            # 'Balance Sheet > Other Stockholder Equity': 'us-gaap:StockholdersEquity', ## ERROR
            'Balance Sheet > Total Stockholder Equity': 'us-gaap:StockholdersEquity',

            # 'Cash Flow > Net income',
            # 'Cash Flow > Depreciation',


            # 'Total current assets': 'us-gaap:assetscurrent',
            # 'Total assets': 'us-gaap:Assets',
            # 'Total current liabilities': 'us-gaap:LiabilitiesCurrent',
            # 'Net Income': 'us-gaap:NetIncomeLoss',
            # 'Cash and cash equivalents': 'us-gaap:CashAndCashEquivalentsAtCarryingValue',
            # 'Cash and cash equivalents': 'us-gaap:CashAndCashEquivalentsAtCarryingValue'
            }
            # 'SalesRevenueNet',
            # 'CostOfGoodsAndServicesSold',
            # 'GrossProfit',
            # 'ResearchAndDevelopmentExpense',
            # 'SellingGeneralAndAdministrativeExpense',
            # 'OperatingExpenses'
            # ]
        adic = {}
        for tag in alist:
            adic[tag] = dothis(xbrl, alist[tag], goodtags)
        return adic

# def gettags(xbrl):
#     obj = xbrl.find_all(name=re.compile("xbrli:context", re.IGNORECASE))
#     # print(len(obj))
#     alist = []
#     for a in obj:
#         # print(a['id'])
#         # aobj = a.find_all(name=re.compile('xbrldi:explicitMember', re.IGNORECASE))
#         aobj = a.find_all(name=re.compile('xbrli:segment', re.IGNORECASE))
#         if len(aobj) > 0:
#             pass
#         else:
#             # print(a['id'])
#             alist.append(a['id'])
#         # print(len(aobj))
#         # if aobj:
#         #     return
#         # aobj = a.find_all(name=re.compile('xbrli:startDate', re.IGNORECASE))
#         # print(a)
#         # print('-'*100)
#     # print('*'*100)
#     # print(alist)
#     return alist
#
# def allfiles():
#     files = ['idt-20180131.xml']
#     # 'aapl-20171230.xml', 'idt-20180131.xml', 'azo-20180210.xml']
#     for filename in files:
#         fh = open(filename, "r")
#
#         xbrl_parser = XBRLParser()
#         xbrl = xbrl_parser.parse(fh)
#         goodtags = gettags(xbrl)
#         pprint.pprint(extract(xbrl, goodtags))
#         print('*'*100)
#         fh.close()

# extract()
# allfiles()

####
# <dei:DocumentFiscalPeriodFocus contextRef="eol_PE5925----1810-Q0003_STD_168_20180210_0" id="id_11913696_94A06FF4-BC10-4470-8CCC-B16999B10CF7_1_4">Q2</dei:DocumentFiscalPeriodFocus>
# <dei:DocumentFiscalYearFocus contextRef="eol_PE5925----1810-Q0003_STD_168_20180210_0" id="id_11913696_94A06FF4-BC10-4470-8CCC-B16999B10CF7_1_3">2018</dei:DocumentFiscalYearFocus>
# <dei:DocumentType contextRef="eol_PE5925----1810-Q0003_STD_168_20180210_0" id="id_11913696_94A06FF4-BC10-4470-8CCC-B16999B10CF7_1_0">10-Q</dei:DocumentType>

if __name__ == '__main__':
    pass
