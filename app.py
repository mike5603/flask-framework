from flask import Flask, render_template, request, redirect, render_template_string
import requests
import json
import pandas
from bokeh.plotting import figure
import datetime
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.models import HoverTool,Range1d
import os
import math

app = Flask(__name__)
app.vars = {}

@app.route('/',methods=['GET','POST'])
def index():
  #return render_template('index.html')
  if request.method=='GET':
    return render_template('input.html')
  app.vars['ticker']=request.form['Stock Ticker']
  app.vars['Starting Date']=request.form['Starting Date']
  app.vars['Ending Date']=request.form['Ending Date']
  r = requests.get('https://www.alphavantage.co/query',params={'function':'TIME_SERIES_DAILY','symbol':app.vars['ticker'],'outputsize':'full','apikey':'MB1WQJ87O5O9N9WM'})
  data = json.loads(r.text)
  df = pandas.DataFrame.from_dict(data['Time Series (Daily)'],dtype=float).transpose()
  df.index=pandas.to_datetime(df.index)
  df = df.sort_index()
  df_range = df.loc[app.vars['Starting Date']:app.vars['Ending Date']]
  df_range['Date'] = df_range.index
  df_range['Date_str'] = df_range.index.strftime('%Y-%m-%d')
  df_range = df_range.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'})
  p=figure(x_axis_type='datetime')
  p.xaxis.axis_label='Date'
  p.yaxis.axis_label='Closing Price'
  p.line(x='Date',y='close', source=df_range)
  try:
    os.remove('template/plot.html')
  except:
    pass
  p.add_tools(HoverTool(tooltips=[('Date','@Date_str'),('Closing Value',"@close")]))
  #htmlo =open('templates/plot.html','w')
  #htmlo.write(file_html(p,CDN,'Stock Output'))
  #htmlo.close()
  return render_template_string(file_html(p,CDN,'Stock Output'))


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=true)
