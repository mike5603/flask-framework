from flask import Flask, render_template, request, redirect
import requests
import json
import pandas

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
  df = pandas.DataFrame.from_dict(data['Time Series (Daily)'])
  df.head
  return 'test'


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=true)
