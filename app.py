from flask import Flask, render_template, request, redirect, url_for
import bot_modules as bm
import error_handling as eh

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start_bot', methods=["POST"])
def start_bot():
    symbol = request.form.get("symbol").upper()
    interval = request.form.get("interval")
    indicators = request.form.getlist("indicators")

    eh.handle_symbol_input(symbol)

    bm.crypto_data(symbol, interval)
    bm.indicator_combiner(indicators)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)