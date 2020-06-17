from flask import Flask, render_template, request, redirect

app = Flask(__name__)
data = {}

@app.route('/',methods=['get','post'])
def index():
  #return render_template('index.html')
  data['ticker']=request.form['Stock Ticker']
  return data['ticker']
@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
