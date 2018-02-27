from app import app
from flask import render_template, make_response, request

import mysql.connector as MS
DB = MS.connect(host="localhost", user="root", passwd="", database='stockmarket')
CURSOR = DB.cursor()

@app.route('/')
@app.route('/index')
def index():
    # return 'Hello, World!!'
    print(request.cookies)
    alist = []
    try:
        CURSOR.execute('SELECT * FROM stocks')
        alist = CURSOR.fetchall()
    except Exception as e:
        print(e.msg)
    resp = make_response(render_template('hello.html', alist=alist))
    resp.set_cookie('cookie_name',value='values')
    return resp
