from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price_data', methods=['POST'])
def get_price_data():
    data = request.get_json()
    coin_id = data.get('coin_id')
    interval = data.get('interval', '1')


    market_chart_url = f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': interval,
        'interval': 'hourly' if interval == '1' else 'daily'
    }
    response = requests.get(market_chart_url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    market_data = response.json()
    prices = market_data.get('prices', [])
    return jsonify({'prices': prices})

if __name__ == '__main__':
    app.run(debug=True)
