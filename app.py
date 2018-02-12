from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import quandl
import io
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.io import show


app = Flask(__name__)
app.vars={}
feat = ['open','close','adj_open', 'adj_close']


#@app.route('/plot',methods=['GET','POST'])
#def plot():
#    quandl.ApiConfig.api_key = 'MhSyqwHb1N6rn5JiB7QF'
#    dfs=quandl.get_table('WIKI/PRICES', paginate=True, qopts={'columns':['date','ticker','open','close','adj_open','adj_close']},date='2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31')
#dfs.columns = ['Date','Ticker','Open Price','Close Price','Adj Open Price','Adj Close Price']
#dfs_open=dfs.copy(deep=True)
#dfs_close=dfs.copy(deep=True)
#dfs_adj_open=dfs.copy(deep=True)
#dfs_adj_close=dfs.copy(deep=True)
#dfs_open=dfs_open.drop(dfs_open.columns[[3, 4, 5]], axis=1)
#dfs_close=dfs_close.drop(dfs_close.columns[[2, 4, 5]], axis=1)
#dfs_adj_open=dfs_adj_open.drop(dfs_adj_open.columns[[2, 3, 5]], axis=1)
#dfs_adj_close=dfs_adj_close.drop(dfs_adj_close.columns[[2, 3, 4]], axis=1)  
#names = [('Open Price', 'Open Price')]
#ds_open = hv.Dataset(dfs_open, ['Date', 'Ticker'], names)
#names = [('Close Price', 'Close Price')]
#ds_close = hv.Dataset(dfs_close, ['Date', 'Ticker'], names)
#names = [('Adj Open Price', 'Adj Open Price')]
#ds_adj_open = hv.Dataset(dfs_adj_open, ['Date', 'Ticker'], names)
#names = [('Adj Close Price', 'Adj Close Price')]
#ds_adj_close = hv.Dataset(dfs_adj_close, ['Date', 'Ticker'], names)

#@app.route('/index',methods=['GET','POST']) 
#def index():
#    if request.method == 'GET':
#      return render_template('config.html')
#    else:
#      app.vars['name'] = request.form['ticker']
#      app.vars['features'] = request.form['close']
   
#      f=open('%s_%s.txt'%(app.vars['ticker'],app.vars['close']),'w')
#      f.write('Ticker: %s\n'%(app.vars['ticker']))
#      f.write('Closing price: %s\n'%(app.vars['close']))
#      f.close()

#      return 'Ticker input is not correct'    
   
#renderer = hv.renderer('bokeh')
#print(renderer)
#renderer = renderer.instance(mode='server')
#hvplot = renderer.get_plot(layout)
#print(hvplot)

#%%opts Curve [width=800 height=550] {+framewise}
#%%opts Curve (color='red' line_width=1.5)
#p1=ds_open.to(hv.Curve, 'Date','Open Price',label='Last month opening ticker prices')
#app = renderer.app(p1)
#print(app)



@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('config.html')
    else:
        app.vars['ticker'] = request.form['ticker'].upper()
        app.vars['select'] = [feat[q] for q in range(4) if feat[q] in request.form.values()]
        return redirect('/plot')

@app.route('/plot',methods=['GET','POST'])
def plot():
    urlData = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?start_date=2018-01-08&end_date=2018-02-08'
                          %app.vars['ticker']).content
    dfs = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    dfs.set_index('Date', inplace=True)
    dfs.set_index(pd.to_datetime(dfs.index), inplace=True)
    dfs.sort_index(inplace=True)
    source = ColumnDataSource(dfs)
                           
    p = figure(title='%s Quandl WIKI EOD Stock Prices - Last month' %app.vars['ticker'], x_axis_type="datetime",plot_width=1000, plot_height=500)

    if 'open' in app.vars['select']:
        p.line('Date', 'Open', line_width=2,line_color='#404EC0',legend='Opening price',source = ColumnDataSource(dfs))
    if 'close' in app.vars['select']:
        p.line('Date', 'Close', line_width=2, line_color="#FB8072",legend='Closing price',source = ColumnDataSource(dfs))
    if 'adj_open' in app.vars['select']:
        p.line('Date', 'High', line_width=2,line_color='#58C44B',legend='Adjusted opening price',source = ColumnDataSource(dfs))
    if 'adj_close' in app.vars['select']:
        p.line('Date','Low', line_width=2, line_color="#FAE116",legend='Adjusted closing price',source = ColumnDataSource(dfs))
    script, div = components(p)
    return render_template('plot.html', script=script, div=div)



if __name__ == '__main__':
  app.run(host='0.0.0.0')