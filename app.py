from flask import Flask, render_template, request, redirect
import requests
import json
import pandas
from bokeh.plotting import figure
import datetime
from bokeh.embed import file_html
from bokeh.resources import CDN

app = Flask(__name__)
app.vars = {}

@app.route('/',methods=['GET','POST'])
def index():
  #return render_template('index.html')
  if request.method=='GET':
    return render_template('input.html')
  app.vars['ticker']=request.form['Stock Ticker']
  r = requests.get('https://www.alphavantage.co/query',params={'function':'TIME_SERIES_DAILY','symbol':app.vars['ticker'],'apikey':'MB1WQJ87O5O9N9WM'})
  data = json.loads(r.text)
  df = pandas.DataFrame.from_dict(data['Time Series (Daily)']).transpose()
  df.index=pandas.to_datetime(df.index)
  df = df.sort_index()
  df_range = df.loc['2020-05-01':'2020-06-01']
  p=figure()
  p.line(x=df_range.index.values,y=df_range['4. close'])
  html =open('templates/plot.html','w')
  html.write(file_html(p,CDN,'Stock Output')
  html.close()
  return render_template('plot.html',script=script,div=div)


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=true)
