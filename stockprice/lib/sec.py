import requests
from bs4 import BeautifulSoup
from .myxbrl import MyXBRL
import pprint

class Sec():
    def __init__(self):
        pass

    def get_page(self, url):
        page = requests.get(url)
        obj = BeautifulSoup(page.text, "lxml")
        return obj

    def get_cik(self, ticker):
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&action=getcompany&owner=exclude'.format(ticker)
        obj = self.get_page(url)

        spans = obj.find_all('span', {'class': 'companyName'})

        if len(spans) == 1:
            astr = spans[0].find_all('a')[0].text
            astr = astr.replace(" (see all company filings)", '')
            return astr
        else:
            return False

    def get_fillings(self, cik):
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-&dateb=&owner=exclude&output=xml&count=100'.format(cik)
        obj = self.get_page(url)
        # print(obj)

        fillings = {}

        table = obj.find_all('filing')
        # print(table)
        for tab in table:
            # print(tab.find_all('datefiled')[0].string)
            # print(tab.find_all('filinghref')[0].string)
            # print(tab.find_all('type')[0].string)
            fillings[tab.find_all('datefiled')[0].string] = dict(
                link=tab.find_all('filinghref')[0].string,
                type=tab.find_all('type')[0].string
            )
        return fillings

    def get_xbrl(self, url):
        obj = self.get_page(url)

        table = obj.find_all('table', {'summary': 'Data Files'})
        # print(table)
        for tr in table[0].find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            # if tds[1].string == 'XBRL INSTANCE DOCUMENT':
            if tds[3].string == 'EX-101.INS':
                return tds[2].find_all('a')[0]['href']
            # print(tds[1])
            # print('*'*100)

    def get_numbers(self, url):
        xbrl = MyXBRL(url)
        return xbrl.get_numbers()
