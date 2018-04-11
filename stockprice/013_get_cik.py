from lib.mongo_database import listTickers
from lib.sec import Sec

import yaml

secdata = Sec()

### Get ticker cik mapping
ticker_list = ['aapl', 'idt', 'azo']
#, aapl, idt, azo]

def get_cik():
    # for sym in listTickers():
    alist = []
    for sym in ticker_list:
        a = secdata.get_cik(sym)
        if a:
            alist.append(a)
    return alist

### Get fillings search results
def get_link(cik_list):
    adic = {}
    for cik in cik_list:
        adic[cik] = []
        fillings = secdata.get_fillings(cik)
        for date in fillings:
            # print("{}\t{}\t{}".format(date, fillings[date]['type'], fillings[date]['link']))
            if len(adic[cik]) > 5:
                continue
            adic[cik].append({
                'date': date,
                'type': fillings[date]['type'],
                'link': fillings[date]['link']
            })
    return adic

def xbrl_data(infolinks):
    for link in infolinks:
        for item in infolinks[link]:
            print(item['date'])
            print(item['type'])
            # print(item['link'])
            ### Get the xml link
    # url = 'http://www.sec.gov/Archives/edgar/data/866787/000119312518085999/0001193125-18-085999-index.htm'
            xbrlurl = secdata.get_xbrl(item['link'])
            # print(xbrlurl)

            ## Get the XBRL file
            url = 'https://www.sec.gov/{}'.format(xbrlurl)
            print(secdata.get_numbers(url))
            print('-'*100)
        print('*'*100)

cik_list = get_cik()
# print(cik_list)
infolinks = get_link(cik_list)
# print(infolinks)
xbrl_data(infolinks)

# with open('data.yml', 'w') as outfile:
# yaml.dump(infolinks)
