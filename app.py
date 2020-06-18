from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.data = {}

@app.route('/',methods=['GET','POST'])
def index():
  #return render_template('index.html')
  if request.method=='GET':
    return render_template('input.html')
  app.data['ticker']=request.args['Stock Ticker']
  return app.data['ticker']


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
