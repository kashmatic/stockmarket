import requests
from lib.iex import IEX

# r = requests.get('https://api.github.com/user')
x = IEX()
# y = x.symbols()

# print(x.symbols_count())

for z in x.symbols():
    jobj = x.stocksKeyStats(z)
    print(z, end="\t")
    ## Criteria 1: More than 1 billion
    if marketcap not in jobj:
        print("marketcap is NA")
        continue
    if jobj['marketcap'] < 1000000000:
        print("marketcap is less than 1 billion, (${:,.2f})".format(jobj['marketcap']))
        continue
    ## Criteria 2: debt should not be N/A or 0
    if jobj['debt'] == 0:
        print("debt is N/A in the data. ({})".format(jobj['debt']))
        continue
    ## Criteria 3: debt to marketcap ratio must be less than 0.5
    ddm = jobj['debt'] / jobj['marketcap']
    if ddm > 0.5:
        print("debt to marketcap ratio is less than 50% ({})".format(ddm))
        continue
    ## Criterian 4: Cash is more than 1 billion
    if jobj['cash'] < 1000000000:
        print("Cash is less then 1B, (${:,.2f})".format(jobj['cash']))
        continue
    ## Criteria 5: quote price / estimatedEPS
    sq = x.stocksQuote(z)
    se = x.stocksEarnings(z)
    if not se['earnings'][0]['estimatedEPS']:
        print("estimatedEPS is null, ({})".format(se['earnings'][0]['estimatedEPS']))
        continue
    if se['earnings'][0]['estimatedEPS'] < 0:
        print("estimatedEPS is negative, ({})".format(se['earnings'][0]['estimatedEPS']))
        continue
    sqdse = sq['latestPrice'] / se['earnings'][0]['estimatedEPS']
    ## lets check for sure [0] object is actually the latest earnings report
    if sqdse > 15:
        print("latestPrice / estimatedEPS is more then 15 ({}).".format(sqdse))
        continue
    ## ALL good print this
    print(jobj['companyName'], jobj['marketcap'], ddm, sqdse)
    print('*'*100)
    # select: few keys
    # condition: if something > anotherthing
    # calculate: multiply x with y

# goes to database

y = x.stocksQuote('aapl'.lower())
print(y['latestPrice'])

y = x.stocksEarnings('aapl'.lower())
print(y['earnings'][0]['estimatedEPS'])

# print(x.stocksFinancials('aapl'))
