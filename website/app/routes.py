from app import app
from flask import render_template, make_response, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import mysql.connector as MS
DB = MS.connect(host="localhost", user="root", passwd="", database='stockmarket')
# DB = MS.connect(host="localhost", user="root", passwd="J3sus0MA!!", database='stockmarket')

CURSOR = DB.cursor()

class FilterForm(FlaskForm):
    marketCap = StringField('Market Cap:', validators=[DataRequired()])
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
        print(alist)


    try:
        if alist:
            sql = 'SELECT * FROM stocks WHERE {}'.format(" AND ".join(alist))
        else:
            sql = 'SELECT * FROM stocks'
        print(sql)
        CURSOR.execute(sql)
        alist = CURSOR.fetchall()
    except Exception as e:
        print(e.msg)

    return render_template('hello.html', alist=alist, form=form)
