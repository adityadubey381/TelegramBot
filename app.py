from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)

    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)

API_KEY = "238f5fb8886846ed154f32a5"
def fetch_conversion_factor(source, target):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{source}"

    response = requests.get(url)
    response = response.json()
    #print(data)


    if response["result"] != "success":
        return None

    return response["conversion_rates"][target]

if __name__ == "__main__":
    app.run(debug=True)
