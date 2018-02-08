from flask import Flask, render_template, request, redirect
from os.path import abspath, dirname, join
from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import webbrowser
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplejson as json
import urllib2
import requests
import ujson as json
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')

app = Flask(__name__)

_cwd = dirname(abspath(__file__))

app.vars={}

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)


quandl.ApiConfig.api_key = 'MhSyqwHb1N6rn5JiB7QF'
dfs=quandl.get_table('WIKI/PRICES', paginate=True, qopts={'columns': ['date','ticker','open','close','adj_open','adj_close']},date='2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31')
dfs.columns = ['Date','Ticker','Open Price','Close Price','Adj Open Price','Adj Close Price']
dfs_open=dfs.copy(deep=True)
dfs_close=dfs.copy(deep=True)
dfs_adj_open=dfs.copy(deep=True)
dfs_adj_close=dfs.copy(deep=True)
dfs_open=dfs_open.drop(dfs_open.columns[[3, 4, 5]], axis=1)
dfs_close=dfs_close.drop(dfs_close.columns[[2, 4, 5]], axis=1)
dfs_adj_open=dfs_adj_open.drop(dfs_adj_open.columns[[2, 3, 5]], axis=1)
dfs_adj_close=dfs_adj_close.drop(dfs_adj_close.columns[[2, 3, 4]], axis=1)  
names = [('Open Price', 'Open Price')]
ds_open = hv.Dataset(dfs_open, ['Date', 'Ticker'], names)
names = [('Close Price', 'Close Price')]
ds_close = hv.Dataset(dfs_close, ['Date', 'Ticker'], names)
names = [('Adj Open Price', 'Adj Open Price')]
ds_adj_open = hv.Dataset(dfs_adj_open, ['Date', 'Ticker'], names)
names = [('Adj Close Price', 'Adj Close Price')]
ds_adj_close = hv.Dataset(dfs_adj_close, ['Date', 'Ticker'], names)


@app.route('/index',methods=['GET','POST']) 
def index():
    if request.method == 'GET':
      return render_template('config.html')
    else:
      app.vars['name'] = request.form['ticker']
      app.vars['features'] = request.form['close']
   
      f=open('%s_%s.txt'%(app.vars['ticker'],app.vars['close']),'w')
      f.write('Ticker: %s\n'%(app.vars['ticker']))
      f.write('Closing price: %s\n'%(app.vars['close']))
      f.close()

      return 'Ticker input is not correct'


if __name__ == '__main__':
  app.run(host='0.0.0.0')

