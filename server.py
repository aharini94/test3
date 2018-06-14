# import csv
import os
import time
import random
from math import ceil

from flask import Flask, render_template, request
# from numpy import var
# from sqlalchemy import DATETIME
# from werkzeug.utils import redirect

app = Flask(__name__)
import sqlite3 as sql
import pandas as pd
dbc = sql.connect('database.db')
dataframe1 = pd.read_csv('equake.csv')
# Referenced from https://stackoverflow.com/questions/43730422/how-to-split-one-column-into-multiple-columns-in-pandas-using-regular-expression
dataframe1[['date', 'time']] = dataframe1['time'].str.split('T', expand=True)
dataframe1[['time']] = dataframe1['time'].str.split('.').str[0]
table_create_start_time = time.time()
dataframe1.to_sql('assign3table', dbc, if_exists='replace')
table_create_end_time = time.time()

@app.route('/')
def home():
    time_diff = table_create_end_time - table_create_start_time
    return render_template("homescreen.html", time_diff=time_diff)

@app.route('/go')
def go():
    return render_template("home.html")

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("Select distinct locationSource from assign3table;")
    rows4 = cur.fetchall()
    return render_template("home.html", rows4=rows4)

@app.route('/rand', methods=['POST'])
def rand():
    num=request.form['num']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    query1_start_time = time.time()
    #for i in range(1,int(num)+1):
    i=1
    while i < int(num) + 1:
        rand1 = ['0', '1', '2', '3', '4', '5', '6', '7']
        rand2 = random.choice(rand1)
        mag = int(rand2)
        cur.execute('SELECT * from assign3table where mag>?', (mag,))
        i = i + 1
    rows = cur.fetchall()
    count = 0
    for row in rows:
        count = count + 1
    query1_end_time = time.time()
    query1_time_diff = query1_end_time - query1_start_time
    return render_template("home.html", query1_time_diff=query1_time_diff, count=count)

@app.route('/randloc', methods=['POST'])
def randloc():
    num=request.form['num']
    loc=request.form['loc']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    query2_start_time = time.time()
    for i in range(1,int(num)+1):
        rand = ['hv' , 'ci' , 'ak' , 'nn' , 'nc' , 'us' , 'pr' , 'nm' , 'uw' , 'se' , 'mb' , 'uu' , 'ld' , 'tul' , 'ismp' , 'ott']
        loc=random.choice(rand)
        cur.execute('SELECT * from assign3table where locationSource=?',(loc,))
    row1=cur.fetchall()
    count1 = 0
    for row in row1:
        count1 = count1 + 1
    query2_end_time = time.time()
    query2_time_diff = query2_end_time - query2_start_time
    return render_template("home.html",query2_time_diff=query2_time_diff, count1=count1)

PORT = int(os.getenv('PORT','5000'))
if __name__ == '__server__':
    app.run(debug=True)
