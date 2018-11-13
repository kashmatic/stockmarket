import mysql.connector as MS

import os

# DB = MS.connect(host="localhost", user="root", passwd="", database='stockmarket')
# DB = MS.connect(host="localhost", user="root", passwd="J3sus0MA!!", database='stockmarket')

DB = MS.connect(
    host=os.environ.get('MARIADB_HOST'),
    user=os.environ.get('MARIADB_USER'),
    passwd=os.environ.get('MARIADB_PASSWORD'),
    database=os.environ.get('MARIADB_DBNAME'),
    port=os.environ.get('MARIADB_PORT')
)

CURSOR = DB.cursor()

class MariadbDatabase():
    def __init__(self):
        self.create_ticker_database('stocks')

    def execute(self, sql):
        try:
            CURSOR.execute(sql)
            DB.commit()
        except Exception as e:
            print(e.msg)

    def execute_command(self, sql):
        try:
            CURSOR.execute(sql)
        except Exception as e:
            print(e.msg)

    def create_ticker_database(self, tname):
        sql = '''
        CREATE TABLE IF NOT EXISTS `{}` (
        `id` int(15) NOT NULL AUTO_INCREMENT,
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
        PRIMARY KEY (`id`)
        )
        '''.format(tname)
        self.execute_command(sql)

    def create_database(self, dbname):
        sql = 'CREATE DATABASE IF NOT EXISTS {}'.format(dbname)
        execute_command(sql)

if __name__ == "__main__":
    md = MariadbDatabase()
    md.create_ticker_database('stocks')
