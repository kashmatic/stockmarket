from pymongo import MongoClient
from lib.iex import IEX
from lib.iex_criteria import IexCriteria
from lib.mongo_database import listTickers
from lib.mariadb_database import MariadbDatabase

from datetime import date as datetoday

def load_database():
    iex = IEX()
    maria = MariadbDatabase()
    for sym in listTickers():
        data = IexCriteria(sym)
        adic = insertobj()
        adic['sym'] = sym
        print(data.get_marketcap())
        if data.get_marketcap():
            adic['marketCap'] = data.get_marketcap()
        else:
            continue
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
        # adic['date'] = datetoday.today().isoformat()
        adic['date'] = '2018-11-15'
        print(adic)
        adic = replaceNone(adic)
        sql = '''
        INSERT INTO `stocks`
        (ticker, marketCap, debt, ratioDebtMarketcap, cash, sumNetIncome, sharesOutstanding, ratioPE, ebitda, ratioPEttm, ratioPEforward, date)
        VALUES
        ('{sym}',{marketCap},{debt},{ratioDebtMarketcap},{cash},{sumNetIncome},{sharesOutstanding},{ratioPE},{ebitda},{ratioPEttm},{ratioPEforward},'{date}')
        '''.format(**adic)
        print(sql)
        maria.execute(sql)
        # CURSOR.execute(sql)
        # DB.commit()

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

if __name__ == '__main__':
    load_database()
