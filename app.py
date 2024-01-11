from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os
from flasgger import Swagger, swag_from
from models.criptos_model import Cripto
import json

load_dotenv()

app = Flask(__name__)
Swagger(app)  # Inicializa o Swagger

@app.route("/")
def home():
    return jsonify({'message': 'Bem vindo a api de cripto, coloque (/apidocs) ao final da url para acessar o swagger'})

@app.route("/<cripto_name>", methods=["GET"])
@swag_from('swagger_config.yml')
def btc_price(cripto_name):
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        return jsonify({'error': 'API_KEY not found'}), 500
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={cripto_name}&market=USD&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        global_quote = data.get('Global Quote')

        if global_quote:
            cripto = Cripto(
                symbol=global_quote['01. symbol'],
                high=global_quote['03. high'],
                low=global_quote['04. low'],
                latest=global_quote['07. latest trading day']
            )

            # Usando json.dumps para garantir a ordem
            ordered_data = json.dumps({
                'symbol': cripto.symbol,
                'low': cripto.low,
                'high': cripto.high,
                'day reference': cripto.latest
            })

            return ordered_data, 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'error': 'Invalid response format from Alpha Vantage'}), 500

    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': f'HTTP Error: {errh}'}), response.status_code
    
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f'Request Exception: {err}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
