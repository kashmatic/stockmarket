import requests

url = "https://www.sec.gov/Archives/edgar/daily-index/2018/QTR1/"

r = requests.get("{}/index.json".format(url))
jobj = r.json()

for i in jobj['directory']:
    print(i)
