from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import io
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.io import show
app = Flask(__name__)
app.vars={}
feat = ['open','close','adj_open', 'adj_close']



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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)