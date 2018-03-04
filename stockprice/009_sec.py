import requests
from bs4 import BeautifulSoup

url = "https://www.sec.gov/Archives/edgar/daily-index/2018/QTR1"
aurl = "https://www.sec.gov/Archives"

r = requests.get("{}/index.json".format(url))
jobj = r.json()

alist = []

for i in jobj['directory']['item']:
    # print(jobj['directory'][i])
    if i['name'].startswith('form'):
        alist.append(i['name'])
        continue

# print(alist)

r = requests.get("{}/{}".format(url, alist[0]))

blist = []

for i in r.text.splitlines():
    if not i.startswith('10-Q'):
        continue
    print(i.split()[-1])
    blist.append(i.split()[-1])
    # print('*'*100)

print(blist)

for i in blist:
    r = requests.get("{}/{}".format(aurl, i))
    # print(r.text)
    x = BeautifulSoup(r.text, "lxml")
    a = x.html.body.find_all('sec-document')
    b = a[0].find_all('document')
    for c in b:
        print(c.type)
        print('*'*100)
    # print('*'*100)
    break
