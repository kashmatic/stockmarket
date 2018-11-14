from app import app
from flask import render_template, make_response, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import mysql.connector as MS
# DB = MS.connect(host="localhost", user="root", passwd="", database='stockmarket')
# DB = MS.connect(host="localhost", user="root", passwd="J3sus0MA!!", database='stockmarket')

import os

DB = MS.connect(
    host=os.environ.get('MARIADB_HOST'),
    user=os.environ.get('MARIADB_USER'),
    passwd=os.environ.get('MARIADB_PASSWORD'),
    database=os.environ.get('MARIADB_DBNAME'),
    port=os.environ.get('MARIADB_PORT')
)

CURSOR = DB.cursor()

class FilterForm(FlaskForm):
    marketCap = StringField('Market Cap:')
    ratioDebtMarketcap = StringField('ratio Debt to Marketcap:')
    cash = StringField('Cash:')
    pe = StringField('PE:')
    ebitda = StringField('EBITDA:')
    pettm = StringField('PE ttm:')
    peforward = StringField('PE forward:')
    submit = SubmitField('Update')

def setfilter(obj):
    alist = []
    for key in obj:
        if 'marketcap' in key:
            alist.append("marketCap > {}".format(obj[key]))
    return " AND ".join(alist)

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    # return 'Hello, World!!'
    # print(request.cookies)
    form = FilterForm(request.form)
    alist = []
    if form.validate():
        val = request.form.get('marketCap')
        if val:
            alist.append("marketCap > {}".format(val))
        val = request.form.get('ratioDebtMarketcap')
        if val:
            alist.append("ratioDebtMarketcap < {}".format(val))
        val = request.form.get('cash')
        if val:
            alist.append("cash > {}".format(val))
        val = request.form.get('pe')
        if val:
            alist.append("ratioPE < {}".format(val))
        val = request.form.get('ebitda')
        if val:
            alist.append("ebitda > {}".format(val))
        val = request.form.get('pettm')
        if val:
            alist.append("ratioPEttm < {}".format(val))
        val = request.form.get('peforward')
        if val:
            alist.append("ratioPEforward < {}".format(val))
        print(alist)


    try:
        if alist:
            # sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks WHERE {} AND date IN (SELECT MAX(date) FROM stocks GROUP BY ticker) ORDER by ticker;'.format(" AND ".join(alist))
            sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks WHERE {} AND date IN (SELECT MAX(date) FROM stocks) ORDER by ticker;'.format(" AND ".join(alist))
        else:
            # sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks'
            # sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks WHERE date IN (SELECT MAX(date) FROM stocks GROUP BY ticker) ORDER by ticker;'
            sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks WHERE date IN (SELECT MAX(date) FROM stocks) ORDER by ticker;'
        print(sql)
        CURSOR.execute(sql)
        result = CURSOR.fetchall()
    except Exception as e:
        print(e.msg)

    return render_template('list.html', result=result, form=form)

@app.route('/<string:symbol>')
def ticker(symbol):
    sql = 'SELECT ticker, marketCap, ratioDebtMarketcap, cash, ratioPE, ebitda, ratioPEttm, ratioPEforward, date FROM stocks WHERE ticker like "{}" ORDER BY date desc'.format(symbol)
    CURSOR.execute(sql)
    result = CURSOR.fetchall()
    return render_template('ticker.html', result=result)
