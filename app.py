from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/start_bot', method=['POST'])
def start_bot():
  symbol = request.form.get('symbol')

if __name__ == '__main__':
  app.run(debug=True)
