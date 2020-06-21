from flask import Flask, render_template, request, redirect, render_template_string
import requests
import json
import pandas
from bokeh.plotting import figure
import datetime
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.models import HoverTool,Range1d,LinearAxis
import os
from datetime import date

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
  app.vars['Plot2']=request.form.get('Dow')
  if app.vars['Plot2']=="1":
    app.vars['ticker 2']=request.form['Stock Ticker 2']
  try:
    test = date.fromisoformat(app.vars['Starting Date'])
    test = date.fromisoformat(app.vars['Ending Date'])
  except:
    return 'Please enter date in form "yyyy-mm-dd"'
  r = requests.get('https://www.alphavantage.co/query',params={'function':'TIME_SERIES_DAILY','symbol':app.vars['ticker'],'outputsize':'full','apikey':'MB1WQJ87O5O9N9WM'})
  data = json.loads(r.text)
  if not data:
    return 'No data found for {}'.format(app.vars['ticker'])
  if 'Error Message' in data.keys():
    return 'Stock Ticker Not Found'
  df = pandas.DataFrame.from_dict(data['Time Series (Daily)'],dtype=float).transpose()
  df.index=pandas.to_datetime(df.index)
  df = df.sort_index()
  df_range = df.loc[app.vars['Starting Date']:app.vars['Ending Date']]
  df_range['Date'] = df_range.index
  df_range['Date_str'] = df_range.index.strftime('%Y-%m-%d')
  df_range = df_range.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'})
  if df_range.empty:
    return 'No data found for {} from {} to {}'.format(app.vars['ticker'],app.vars['Starting Date'],app.vars['Ending Date'])
  p=figure(x_axis_type='datetime',title='Stock Closing Price for {} from {} to {}'.format(app.vars['ticker'],app.vars['Starting Date'],app.vars['Ending Date']))
  p.xaxis.axis_label='Date'
  p.yaxis.axis_label='{} Closing Price'.format(app.vars['ticker'])
  p.line(x='Date',y='close', source=df_range,line_width=3,legend_label=app.vars['ticker'])
  p.add_tools(HoverTool(tooltips=[('Date','@Date_str'),('Closing Value',"@close")]))
  if app.vars['Plot2']=="1":
    r2 = requests.get('https://www.alphavantage.co/query',params={'function':'TIME_SERIES_DAILY','symbol':app.vars['ticker 2'],'outputsize':'full','apikey':'MB1WQJ87O5O9N9WM'})
    data2 = json.loads(r2.text)
    if not data2:
      return 'No data found for {}'.format(app.vars['ticker 2'])
    if 'Error Message' in data.keys():
      if app.vars['ticker 2']=='':
        return 'Input Symbol for Second Stock'
      else:
        return 'No data found for {}'.format(app.vars['ticker 2'])
    df2 = pandas.DataFrame.from_dict(data2['Time Series (Daily)'],dtype=float).transpose()
    df2.index=pandas.to_datetime(df2.index)
    df2 = df2.sort_index()
    df2_range = df2.loc[app.vars['Starting Date']:app.vars['Ending Date']]
    df2_range['Date'] = df2_range.index
    df2_range['Date_str'] = df2_range.index.strftime('%Y-%m-%d')
    df2_range = df2_range.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'})
    if df2_range.empty:
      return 'No data found for {} from {} to {}'.format(app.vars['ticker 2'],app.vars['Starting Date'],app.vars['Ending Date'])                  
    ymax = df_range['close'].max()
    ymin = df_range['close'].min()
    p.y_range=Range1d(start=ymin,end=ymax)
    ymax2 = df2_range['close'].max()
    ymin2 = df2_range['close'].min()
    p.extra_y_ranges = {"y2": Range1d(start=ymin2, end=ymax2)}
    p.add_layout(LinearAxis(y_range_name="y2", axis_label='{} Closing Price'.format(app.vars['ticker 2'])), 'right')
    p.line(x='Date',y='close',source=df2_range,y_range_name='y2',line_width=3, line_color='red',legend_label=app.vars['ticker 2'])
    p.legend.location = "top_left"
    p.yaxis[0].axis_label_text_color = 'blue'
    p.yaxis[1].axis_label_text_color = 'red'
    p.title.text='Stock Closing Price for {} and {} from {} to {}'.format(app.vars['ticker'],app.vars['ticker 2'],app.vars['Starting Date'],app.vars['Ending Date'])
  else:
    p.legend.visible=False
  #htmlo =open('templates/plot.html','w')
  #htmlo.write(file_html(p,CDN,'Stock Output'))
  #htmlo.close()
  return render_template_string(file_html(p,CDN,'Stock Output'))


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
