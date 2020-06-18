from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.vars = {}

@app.route('/',methods=['GET','POST'])
def index():
  #return render_template('index.html')
  if request.method=='GET':
    return render_template('input.html')
  app.vars['ticker']=request.form['Stock Ticker']
  return render_template('output.html',stock=app.vars['ticker'])


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=true)
