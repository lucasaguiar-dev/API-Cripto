from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
Swagger(app)  # Inicializa o Swagger

@app.route("/<cripto_name>", methods=["GET"])
def btc_price(cripto_name):
    api_key = os.getenv("API_KEY")
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={cripto_name}&market=USD&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
