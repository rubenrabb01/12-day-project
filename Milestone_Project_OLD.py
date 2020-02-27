#!/usr/bin/env python
# coding: utf-8

# In[5]:


#################################################################################################################################
################################################ MILESTONE PROJECT - PART 1 ######################################################

#1. Create Pandas dataframes 
#2. Manipulate data (indexing, selection, variable dtypes)conca

#3. Plot data (Matplotlib, Bokeh)


# In[2]:


#Load all libraries that will be used in this project 

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144


# In[3]:


import pandas as pd
import json 
from io import StringIO
import io
import csv
import sys
import datetime


# In[4]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


# In[5]:


from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral6
from bokeh.resources import CDN
from bokeh.embed import file_html
from ipywidgets import *


# In[6]:


from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')


# In[7]:


#create a dataframe

df1 = pd.DataFrame({
    'id':[1,2,3,4,5,6,7,8,9,10,11],
    'number': ['16.30', '17.20', '17.70','16.30','17.90','15.90','16.00','18.12','16.40','17.00','16.32'],
    'response':[0,1,1,0,0,1,0,1,0,0,0]},
    index=[1,2,3,4,5,6,7,8,9,10,11])


# In[8]:


#Indexing dataframes by 'id'

df1.set_index(['id']).head(11)


# In[9]:


#Let's create a new variable 'date' from current year and range from 2005 to 2015. Then I'll add this new column to each dataframe

year = datetime.datetime.today().year
date = range(2005,year-2)
date

#Also, can create a new variable date which years ranging between 2005 and 2015 as:
#date = pd.date_range('2005', '2016', freq='A')


# In[10]:


#Convert list to an array with float format

date = np.array(date, dtype=np.float32)
date


# In[11]:


#Sort by reverse index
#df1.sort_index(ascending=False).head(11)


# In[12]:


#Define object length using the the variable 'number' as reference

sLength = len(df1['number'])

#Add the new variable 'date' to each dataframe

df1['date'] = date


# In[13]:


#Sort by'number' values 

df1.sort_values('number').head(11)


# In[14]:


#convert the variable 'number' to float64
df1[['number']] = df1[['number']].astype('float')

#convert the variable 'year' to int
df1[['date']] = df1[['date']].astype('int')
#output['date'] = pd.to_datetime(output['date'])
#output['date'] = output['date'].apply(lambda x: x.strftime('%Y'))

#Convert "response" variable to boolean
df1[['response']] = df1[['response']].astype('bool') #Also: #output['response'].astype(str).astype(int)
                                                                 #pd.factorize(output['response'])[0]


# In[15]:


#see dtype objects
df1.dtypes


# In[16]:


df1


# In[17]:


df1.set_index(['date']).head(11)


# In[18]:


from ipywidgets import interact
import numpy as np

from bokeh.io import push_notebook
from bokeh.plotting import figure, show, output_notebook


# In[19]:


x = df1['date']
y = df1['number']
output_notebook()


# In[20]:


#Plot number vs date using matplotlib

from matplotlib import pylab as plt
df1.sort_values(by='date').plot(x='date', y='number', label=id)
plt.ylabel("number")
plt.legend(loc='lower right')


# In[21]:


#Use Bokeh to create an interactive plot of the temporal trend

output_notebook()  
TOOLS = "pan, box_zoom, wheel_zoom, reset, save"

p = figure(tools=TOOLS,title="Temporal trend", plot_height=300, plot_width=600, y_range=(15,20),x_axis_label="date")
r = p.line(x, y, color="#2222aa", line_width=3)
show(p)


# In[22]:


#Create two additional dataframes

df2 = pd.DataFrame({
    'id':[12,13,14,15,16,17,18,19,20,21,22],
    'number': ['18.00', '18.20', '16.90','17.10','16.60','17.50','17.60','17.62','17.30','16.50','17.12'],
    'response':[1,1,0,0,1,0,0,1,1,0,1]},
    index=[11,12,13,14,15,16,17,18,19,20,21])

df3 = pd.DataFrame({
    'id':[23,24,25,26,27,28,29,30,31,32,33],
    'number': ['16.00', '15.88', '17.30','15.90','16.00','17.10','16.60','15.92','16.30','16.10','17.42'],
    'response':[1,0,0,1,1,0,1,0,1,1,0]},
    index=[22,23,24,25,26,27,28,29,30,31,32])


# In[23]:


#Indexing dataframes by 'id'

df2.set_index(['id']).head(11)


# In[24]:


df3.set_index(['id']).head(11)


# In[25]:


#Define object length using the the variable 'number' as reference

sLength = len(df1['number'])

#Add the new variable 'date' to each dataframe

df2['date'] = date
df3['date'] = date


# In[26]:


#Concatenate the three dataframes

dfs = [df1, df2, df3]
output = pd.concat(dfs)

#Also, can use merge to combine the three dataframes  
#output_join= output.merge(output, on='date', how='left')
#output_join.head(33)


# In[27]:


#convert the variable 'number' to float64
output[['number']] = output[['number']].astype('float')

#convert the variable 'year' to int
output[['date']] = output[['date']].astype('int')

#Convert "response" variable to boolean True/False
output[['response']] = output[['response']].astype('bool') 


# In[28]:


#Indexing by date

output.set_index(['date']).head(33)


# In[29]:


#A short description of the variable "number" in the combined dataframes

print "Numbers between 2005 and 2015"
output['number'].describe()


# In[30]:


#select column 'number' and sum all its values

sum_numb= output['number'].sum()
sum_numb


# In[31]:


#How many unique values are there in the dataframe?

output['number'].unique()[:11]


# In[32]:


#How many cases of each value are there?
output['number'].value_counts().head(33)


# In[35]:


output.plot(x="date", y=["number", "response"],  figsize=(12, 8), kind="bar")


# In[36]:


#Assign axis names to each dataframe
output = pd.concat(dfs, keys=['x', 'y', 'z'])
output


# In[37]:


#################################################################################################################################
################################################ MILESTONE PROJECT - PART 2 ######################################################

#1. Request data from public API using request and simplejson libraries 
#2. Convert jSon data to Pandas dataframe
#3. Create table and plotting data (Bokeh, Holoviews)


# In[38]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144


# In[39]:


import pandas as pd
import json 
from io import StringIO
import io
import csv
import sys
import datetime
import numpy as np
import re


# In[40]:


import simplejson as json
import urllib2
import requests
import ujson as json


# In[41]:


import holoviews as hv
hv.extension('bokeh', 'matplotlib')
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral6
from ipywidgets import *


# In[42]:


#Request search of jobless rate in USA between 1980 and 2016
#API Keys parameters can be found at: http://blog.inqubu.com/inqstats-open-api-published-to-get-demographic-data

r = requests.get('http://inqstatsapi.inqubu.com?api_key=c0081761e5b8e007&data=jobless_rate&countries=us&years=1980:2016')
r


# In[43]:


print(r.content)


# In[44]:


data = r.json()
print(type(data))
print(data)


# In[45]:


print(r.headers)
print(r.headers["content-type"])


# In[46]:


#Define the target url

url="http://inqstatsapi.inqubu.com?api_key=c0081761e5b8e007&data=jobless_rate&countries=us&years=1980:2016"


# In[47]:


data = urllib2.urlopen(url).read()
data


# In[48]:


#Convert from json format to Python dict and limit variable field  

job=json.loads(data)
job=json.loads(data)[0]['jobless_rate']
job


# In[49]:


#Export data into a dataframe and print basic numbers 

data = pd.DataFrame(job)
data
data.describe()


# In[50]:


#Create a new dataframe, index and change name of the first column

dfjob=data[['data', 'year']].head(23)
dfjob.columns
dfjob.columns.values[0] = 'jobless rate' 
dfjob


# In[51]:


#Convert variable type to assign a sequence argument and plot 'year' vs 'jobless rate'

dfjob=dfjob.astype(float)


# In[60]:


dfjob.plot(x='year', y='jobless rate', figsize=(12, 7), kind='barh') 


# In[54]:


#Export data and create hv table 

table = hv.Table(dfjob, 'year', 'jobless rate')
table


# In[55]:


#Create interactive plot using holoviews

hv.Curve(table) + hv.Bars(table)


# In[129]:


#################################################################################################################################
################################################ MILESTONE PROJECT - PART 3 ######################################################

#1. Request API of stock ticker prices from Quandle WIKI dataset (two approaches with and without selection filters applied) 
#2. Convert jSon data to Pandas dataframe
#3. Create two separate dataframes, one for closing prices per ticker and another one for closing, opening, adjusted closing and adjusted openening prices per ticker  
#4. Analyze prices data since last month 
#5. Create table and plot data (Bokeh, Holoviews)


# In[130]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144
import pandas as pd
import numpy as np


# In[131]:


import simplejson as json
import urllib2
import requests
import ujson as json


# In[132]:


from bokeh.plotting import figure, show, output_notebook
from bokeh.resources import CDN
from bokeh.embed import file_html
from ipywidgets import interact
from bokeh.io import push_notebook
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')


# In[133]:


#################################################################################################################################
#3.1. GENERAL API REQUEST


# In[134]:


#Set url

url="https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=MhSyqwHb1N6rn5JiB7QF"


# In[135]:


#Search request of ticker prices

r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=MhSyqwHb1N6rn5JiB7QF')
r


# In[136]:


#Return json file as python dict

ticker = r.json()
ticker 


# In[137]:


ticker_data=ticker['datatable']
ticker_data.keys()


# In[138]:


#See keys

ticker.keys()


# In[139]:


#FROM HERE ON
#################################################################################################################################
#FOLLOW A) OR B)


# In[140]:


#################################################################################################################################


# In[141]:


#3.1.A) OBTAIN A DATAFRAME OF CLOSING PRICES OF EACH TICKER FROM THE LAST MONTH 

#Select last  month prices

ticker_col=ticker_data['columns']
ticker1=ticker_data['data'][4557:4578]
ticker2=ticker_data['data'][4872:4893]
ticker3=ticker_data['data'][7981:8002]
ticker4=ticker_data['data'][9274:9292]

import pandas
df1=pandas.DataFrame.from_dict(ticker1, orient='columns')
df1.drop(df1.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df1.columns = ['Ticker', 'Date', 'Price']
df2=pandas.DataFrame.from_dict(ticker2, orient='columns')
df2.drop(df2.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df2.columns = ['Ticker', 'Date', 'Price']
df3=pandas.DataFrame.from_dict(ticker3, orient='columns')
df3.drop(df3.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df3.columns = ['Ticker', 'Date', 'Price']
df4=pandas.DataFrame.from_dict(ticker4, orient='columns')
df4.drop(df4.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df4.columns = ['Ticker', 'Date', 'Price']
dfs = [df1, df2, df3, df4]
dfs = pd.concat(dfs)


# In[142]:


out=dfs.pivot(index= 'Date', columns='Ticker', values='Price')
out


# In[16]:


out.plot.box(figsize=(8, 5))


# In[17]:


#Bar plots of Date per Ticker prices

out.plot.bar(colormap='Greens',stacked=True, figsize=(11, 7),legend='top_right')


# In[ ]:


#Plot closing prices for each ticker 


# In[18]:


names = [('Price', 'Stock Input')]
ds = hv.Dataset(dfs, ['Date', 'Ticker'], names)


# In[19]:


get_ipython().run_cell_magic('opts', 'Curve [width=800 height=550] {+framewise}', "ds.to(hv.Curve, 'Date','Price')")


# In[20]:


get_ipython().run_cell_magic('opts', "Bars [width=900 height=400 tools=['hover'] group_index=1 legend_position='top_right']", "Tickers = ['A', 'AA', 'AAL', 'AAMC']\nds.select(Ticker=Tickers).to(hv.Bars, ['Date','Ticker'], 'Price').sort()")


# In[21]:


get_ipython().run_cell_magic('opts', "Curve [width=200] (color='indianred')", "Tickers = ['A', 'AA', 'AAL', 'AAMC']\ngrouped = ds.select(Ticker=Tickers).to(hv.Curve, 'Date', 'Price')\ngrouped.grid('Ticker')")


# In[22]:


get_ipython().run_cell_magic('opts', "Curve [width=600] (color=Cycle(values=['indianred', 'slateblue', 'lightseagreen', 'coral']))", "grouped.overlay('Ticker')")


# In[ ]:


#JUMP TO LINE 34 FOR ADDITIONAL SUMMARY STATISTICS AND GRAPH VISUALIZATION


# In[24]:


#################################################################################################################################


# In[114]:


#3.1.B) OBTAIN A DATAFRAME OF CLOSING, OPENING, ADJUSTED CLOSING AND ADJUSTED OPENING PRICRES FROM THE LAST MONTH FOR EACH TICKER 

#Select last  month prices

ticker_col=ticker_data['columns']
ticker1=ticker_data['data'][4557:4578]
ticker2=ticker_data['data'][4872:4893]
ticker3=ticker_data['data'][7981:8002]
ticker4=ticker_data['data'][9274:9292]

import pandas
df1=pandas.DataFrame.from_dict(ticker1, orient='columns')
df1.drop(df1.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df1.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df2=pandas.DataFrame.from_dict(ticker2, orient='columns')
df2.drop(df2.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df2.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df3=pandas.DataFrame.from_dict(ticker3, orient='columns')
df3.drop(df3.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df3.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df4=pandas.DataFrame.from_dict(ticker4, orient='columns')
df4.drop(df4.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df4.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
dfs = [df1, df2, df3, df4]
dfs = pd.concat(dfs)
dfs


# In[115]:


#Create a new dataframe 'Date' from previous dataframe that will be used as an index

dfsd=dfs.loc[:, 'Date']
dfsd1=dfsd.drop_duplicates()
dfsd1


# In[116]:


#Re-order the columns in the dataframe:

#1.  Assign multi-index columns from tuples

multicols = pd.MultiIndex.from_tuples([('A','Open Price'),('A','Close Price'),('A','Adj Open Price'),('A','Adj Close Price'),
                                       ('AA','Open Price'),('AA','Close Price'),('AA','Adj Open Price'),('AA','Adj Close Price'),
                                       ('AAL','Open Price'),('AAL','Close Price'),('AAL','Adj Open Price'),('AAL','Adj Close Price'),
                                       ('AAMC','Open Price'),('AAMC','Close Price'),('AAMC','Adj Open Price'),('AAMC','Adj Close Price')],
                                       names=['Ticker', 'Price'])

#2. Create an empty dataframe using the former newly created 'Date' index and the multi-index columns from step 1

index = dfsd1
out = pd.DataFrame(index=index,columns=multicols).sort_index().sort_index(axis=1)
out


# In[111]:


dfs['Open Price'] = dfs['Open Price'].fillna(dfs['Open Price'].mean())  
dfs['Close Price'] = dfs['Close Price'].fillna(dfs['Close Price'].mean())      
dfs['Adj Open Price'] = dfs['Adj Open Price'].fillna(dfs['Adj Open Price'].mean())  
dfs['Adj Close Price'] = dfs['Adj Close Price'].fillna(dfs['Adj Close Price'].mean())     

dfs=dfs[['Open Price', 'Close Price', 'Adj Open Price', 'Adj Close Price']]


# In[121]:


#3. Create another dataframe based on the combined dataframes (1,2,3,4, dfs) containing the actual values of ticker prices

#Group columns  by 'Ticker' name, pivot column index rows to column and imputate missing cases

dfill = (dfs.groupby('Ticker').apply(lambda g:g.set_index('Date') [['Open Price', 'Close Price', 'Adj Open Price', 'Adj Close Price']]).unstack(level=0).fillna(dfs['Close Price'].mean()))

#Delete column and adjust the multi-index column 

dfill.columns=dfill.columns.droplevel()  
print dfill


# In[122]:


#Reset the indices of the two dataframes

out = out.reset_index(drop=True)
dfill = dfill.reset_index(drop=True)

#Rebuild the empty dataframe

out = pd.DataFrame(out)

#Assign length of columns and copy price values within each price category and ticker from one to another dataframe

sLength = len(out['A'])
out['A']= dfill['A'].values
out['AA']= dfill['AA'].values
out['AAL']= dfill['AAL'].values
out['AAMC']= dfill['AAMC'].values


# In[123]:


#Add the column 'Date' indexed in the dataframe

out['Date'] = dfsd1
out


# In[124]:


out.describe()


# In[32]:


out.columns


# In[33]:


#FROM HERE ON THE RESULTS CHANGE DEPENDING ON WHETHER YOU CHOSE 3.1.A, 3.1.B!!!!!
################################################################################################################################
#RESULTS SUMMARY STATISTICS AND DATA PLOT


# In[34]:


#Show summary statistics 

print out.describe()

#Calculate/plot mean-error values of each Ticker   

mean = out.mean()
error = out.std()
mean
error


# In[35]:


#Mean+Error bar plot

fig, ax = plt.subplots()
mean.plot.bar(yerr=error, ax=ax)


# In[36]:


out.plot.area(stacked=False,figsize=(11, 8))


# In[37]:


out.plot(subplots=True, figsize=(10, 10))


# In[38]:


plt.figure()
out.plot(colormap=cm.cubehelix,figsize=(12, 7))


# In[38]:


output_notebook()


# In[40]:


################################################################################################################################
#3.2.SPECIFIC API REQUEST (Filter by columns 'date', 'ticker' and ticker prices)


# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplejson as json
import urllib2
import requests
import ujson as json


# In[3]:


from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')


# In[4]:


#Either use:

#3.2.1.A) 

import quandl
quandl.ApiConfig.api_key = 'MhSyqwHb1N6rn5JiB7QF'
dfs=quandl.get_table('WIKI/PRICES',qopts={'columns': ['date','ticker','open','close','adj_open','adj_close']},date='2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31')

#For closing prices only alternatively you can use:
#dfs=quandl.get_table('WIKI/PRICES',qopts={'columns': ['date','ticker','close']},date='2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31')

#or

#3.2.1.B)

#r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?qopts.columns=ticker,date,open,close,adj_open,adj_close&date=2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31&api_key=MhSyqwHb1N6rn5JiB7QF')
#qt = r.json() 


# In[5]:


#From here on follow 3.2.1 or 3.2.2 approaches 
#################################################################################################################################


# In[6]:


###########3.2.1. This method will result in four plots for each of the price values contained in the requested data


# In[7]:


#Rename columns

dfs.columns = ['Date','Ticker','Open Price','Close Price','Adj Open Price','Adj Close Price']

#For search selection filtered only by closing prices use:

#dfs.columns = ['Date','Ticker','Price']
#out=dfs.pivot(index= 'Date', columns='Ticker', values='Price')


# In[8]:


#Make four copies of the dataframe and drop columns by price values

dfs_open=dfs.copy(deep=True)
dfs_close=dfs.copy(deep=True)
dfs_adj_open=dfs.copy(deep=True)
dfs_adj_close=dfs.copy(deep=True)
dfs_open=dfs_open.drop(dfs_open.columns[[3, 4, 5]], axis=1)
dfs_close=dfs_close.drop(dfs_close.columns[[2, 4, 5]], axis=1)
dfs_adj_open=dfs_adj_open.drop(dfs_adj_open.columns[[2, 3, 5]], axis=1)
dfs_adj_close=dfs_adj_close.drop(dfs_adj_close.columns[[2, 3, 4]], axis=1)  


# In[9]:


#Assign Y names

names = [('Open Price', 'Open Price')]
ds_open = hv.Dataset(dfs_open, ['Date', 'Ticker'], names)
names = [('Close Price', 'Close Price')]
ds_close = hv.Dataset(dfs_close, ['Date', 'Ticker'], names)
names = [('Adj Open Price', 'Adj Open Price')]
ds_adj_open = hv.Dataset(dfs_adj_open, ['Date', 'Ticker'], names)
names = [('Adj Close Price', 'Adj Close Price')]
ds_adj_close = hv.Dataset(dfs_adj_close, ['Date', 'Ticker'], names)


# In[10]:


#Plot open prices for each ticker   


# In[11]:


get_ipython().run_cell_magic('opts', 'Curve [width=800 height=550] {+framewise}', "%%opts Curve (color='red' line_width=1.5)\nds_open.to(hv.Curve, 'Date','Open Price',label='Last month opening ticker prices')")


# In[12]:


#Plot closing prices for each ticker  


# In[13]:


get_ipython().run_cell_magic('opts', 'Curve [width=800 height=550] {+framewise}', "%%opts Curve (color='blue' line_width=1.5)\nds_close.to(hv.Curve, 'Date','Close Price',label='Last month closing ticker prices')")


# In[14]:


#Plot adjusted open prices for each ticker   


# In[15]:


get_ipython().run_cell_magic('opts', 'Curve [width=800 height=550] {+framewise}', "%%opts Curve (color='green' line_width=1.5)\nds_adj_open.to(hv.Curve, 'Date','Adj Open Price',label='Last month adjusted opening ticker prices')")


# In[16]:


#Plot adjusted closing prices for each ticker   


# In[17]:


get_ipython().run_cell_magic('opts', 'Curve [width=800 height=550] {+framewise}', "%%opts Curve (color='yellow' line_width=1.5)\nds_adj_close.to(hv.Curve, 'Date','Adj Close Price',label='Last month adjusted closing ticker prices')")


# In[18]:


import param,paramnb
class Result(param.Parameterized):
    score=param.Integer(default=1,bounds=(0,10))
    verified=param.Boolean(default=False)
    grade=param.ObjectSelector(objects=["A","B","C"])
paramnb.Widgets(Result,next_n=1)


# In[ ]:


###########3.2.2. This method aims to categorize a dataframe containing all the prices and tickers for subsequent graph contruction


# In[44]:


#Create a new dataframe 'date' from previous dataframe that will be used as an index

dfsd=dfs.loc[:, 'date']
dfsd1=dfsd.drop_duplicates()
dfsd1


# In[45]:


#Create a new dataframe using grouping variables 'ticker' and 'prices' and indexed by date. Imputate missing cases with closing prices mean

outg = (dfs.groupby('ticker').apply(lambda g:g.set_index('date')[['open','close','adj_open','adj_close']]).unstack(level=0).fillna(dfs['close'].mean()))

#Delete column and adjust the multi-index column 

print outg


# In[46]:


#Remove index 
outg = outg.reset_index(drop=True)

#Add the previously generated dataframe index to the final dataframe

outg['date'] = dfsd1

#View the final table 

outg


# In[47]:


#See elements ordered

sorted(outg)


# In[48]:


#Show summary statistics

print outg.describe()


# In[50]:


outg.plot(x='date', y='close', figsize=(12, 7), kind='bar') 


# In[136]:


outg.set_index('date').query("Close Price").sort_values('Close Price', ascending=False).plot.bar(rot=0, width=1)


# In[ ]:




