import requests

def handle_symbol_input(symbol):
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        symbols = [s['symbol'] for s in data['symbols']]

        if symbol in symbols:
            print("its in there!")
        else:
            print("it aint in there cuz")
    else:
        print(f"Error fetching symbols from binance api: {response.status_code}")