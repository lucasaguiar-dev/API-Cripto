from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis de ambiente a partir do arquivo .env

app = Flask(__name__)

@app.route("/<cripto_name>")
def btc_price(cripto_name):
    api_key = os.getenv("API_KEY")
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={cripto_name}&market=USD&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
