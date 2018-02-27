import mysql.connector as MS

from pymongo import MongoClient
from lib.iex import IEX
from lib.iex_criteria import IexCriteria

from datetime import date as datetoday

# DB = MS.connect(host="localhost", user="root", passwd="", database='stockmarket')
DB = MS.connect(host="localhost", user="root", passwd="J3sus0MA!!", database='stockmarket')
CURSOR = DB.cursor()

client = MongoClient("mongodb://localhost:27017/stocks")
mongodb = client['stocks']

def execute_command(sql):
    try:
        CURSOR.execute(sql)
    except Exception as e:
        print(e.msg)

def create_database(dbname):
    sql = 'CREATE DATABASE IF NOT EXISTS {}'.format(dbname)
    execute_command(sql)

def insertobj():
    adic = dict(
        ticker=None,
        marketCap=None,
        debt=None,
        ratioDebtMarketcap=None,
        cash=None,
        sumNetIncome=None,
        sharesOutstanding=None,
        ratioPE=None,
        ebitda=None,
        ratioPEttm=None,
        ratioPEforward=None,
        date=None
    )
    return adic

def replaceNone(adic):
    for key in adic:
        if not adic[key]:
            adic[key] = 'NULL'
    return adic

def create_ticker_database(tname):
    sql = '''
    CREATE TABLE `{}` (
    `ticker` varchar(11) NOT NULL,
    `marketCap` BIGINT unsigned,
    `debt` BIGINT unsigned,
    `ratioDebtMarketcap` double,
    `cash` BIGINT unsigned,
    `sumNetIncome` BIGINT signed,
    `sharesOutstanding` BIGINT unsigned,
    `ratioPE` double,
    `ebitda` BIGINT unsigned,
    `ratioPEttm` double,
    `ratioPEforward` double,
    `date` date NOT NULL,
    PRIMARY KEY (`ticker`)
    )
    '''.format(tname)
    execute_command(sql)

def load_database():
    iex = IEX()
    for sym in iex.symbols():
        print(sym)
        stocksEarnings = iex.stocksEarnings(sym)
        stocksFinancials = iex.stocksFinancials(sym)
        stocksKeyStats = iex.stocksKeyStats(sym)
        stocksQuote = iex.stocksQuote(sym)
        stocksChart1y = iex.stocksChart1y(sym)
        data = IexCriteria(
            sym,
            stocksEarnings,
            stocksFinancials,
            stocksKeyStats,
            stocksQuote,
            stocksChart1y,
            {}
        )
        adic = insertobj()
        adic['sym'] = sym
        if data.get_marketcap():
            adic['marketCap'] = data.get_marketcap()
        if data.get_debt():
            adic['debt'] = data.get_debt()
        if adic['debt'] and adic['marketCap']:
            adic['ratioDebtMarketcap'] = adic['debt'] / adic['marketCap']
        if data.get_cash():
            adic['cash'] = data.get_cash()
        if data.get_netIncome():
            adic['sumNetIncome'] = data.get_netIncome()
        if data.get_sharesoutstanding():
            adic['sharesOutstanding'] = data.get_sharesoutstanding()
        delayedPrice = int(data.get_delayedprice())
        if delayedPrice and adic['sumNetIncome'] and adic['sharesOutstanding']:
            adic['ratioPE'] = delayedPrice / (adic['sumNetIncome'] / adic['sharesOutstanding'])
        if data.get_ebitda():
            adic['ebitda'] = data.get_ebitda()
        if data.get_finvizpettm():
            adic['ratioPEttm'] = data.get_finvizpettm()
        if data.get_finvizpeforward():
            adic['ratioPEforward'] = data.get_finvizpeforward()
        adic['date'] = datetoday.today().isoformat()
        adic = replaceNone(adic)
        sql = '''
        INSERT INTO `stocks`
        (ticker, marketCap, debt, ratioDebtMarketcap, cash, sumNetIncome, sharesOutstanding, ratioPE, ebitda, ratioPEttm, ratioPEforward, date)
        VALUES
        ('{sym}',{marketCap},{debt},{ratioDebtMarketcap},{cash},{sumNetIncome},{sharesOutstanding},{ratioPE},{ebitda},{ratioPEttm},{ratioPEforward},'{date}')
        '''.format(**adic)
        print(sql)
        CURSOR.execute(sql)
        DB.commit()

if __name__ == '__main__':
    create_ticker_database('stocks')
    load_database()
