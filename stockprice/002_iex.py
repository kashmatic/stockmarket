import requests
from lib.iex import IEX

# r = requests.get('https://api.github.com/user')
x = IEX()
# y = x.symbols()

print(x.symbols_count())

# for z in x.symbols():
#     print(z)

print(x.stocksKeyStats('aapl'))

print(x.stocksFinancials('aapl'))
