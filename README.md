# Currency Converter Telegram Chatbot

This project is a Flask-based backend for a **Telegram currency converter bot** built using **Dialogflow** and the **ExchangeRate API**.

Telegram Bot Username:
**@convertramukaka_bot**

The bot converts currency in real time.

Example:

> Convert 100 INR to USD
> 100 rupees to dollars

---

# Tech Stack

* Python 3
* Flask
* Dialogflow (Google Cloud)
* Telegram Bot API
* ExchangeRate API
* Git

---

# How the System Works

1. User sends a message to **@convertramukaka_bot** on Telegram
2. Telegram forwards the message to Dialogflow
3. Dialogflow extracts:

   * amount
   * source currency
   * target currency
4. Dialogflow calls the Flask webhook
5. Flask fetches live exchange rates
6. Response is returned to Telegram

---

# Step 1 — Create Telegram Bot

1. Open Telegram
2. Search for **@BotFather**
3. Run:

```
/start
/newbot
```

4. Set:

   * Bot Name
   * Username (must end in `bot`)

You will receive a **Bot Token**.

⚠️ Never push this token to GitHub.

---

# Step 2 — Connect Telegram to Dialogflow

In Dialogflow:

1. Go to **Integrations**
2. Enable **Telegram**
3. Paste your Telegram Bot Token
4. Save

Now Telegram is connected to your Dialogflow agent.

---

# Step 3 — Create Dialogflow Agent

1. Go to:
   [https://dialogflow.cloud.google.com/](https://dialogflow.cloud.google.com/)
2. Create a new agent
3. Set default language and timezone

---

# Step 4 — Create Currency Intent

Create a new intent:

```
currency-convert
```

Add training phrases:

```
Convert 100 INR to USD
100 rupees to dollars
Change 500 INR to EUR
```

Add parameters:

* `@sys.unit-currency` → amount + source currency
* `@sys.currency-name` → target currency

Save the intent.

---

# Step 5 — Enable Webhook Fulfillment

1. Go to **Fulfillment**
2. Enable Webhook
3. Add your backend URL:

```
https://your-domain.com/
```

Save.

---

# Step 6 — Backend Setup

## Install dependencies

```
pip install flask requests
```

## Project Structure

```
currency-convert-chatbot-backend/
│
├── app.py
├── README.md
└── .gitignore
```

---

# Example Flask Backend

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    rate = fetch_conversion_factor(source_currency, target_currency)
    converted_amount = amount * rate

    return jsonify({
        "fulfillmentText": f"{amount} {source_currency} is {converted_amount:.2f} {target_currency}"
    })


def fetch_conversion_factor(source, target):
    url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{source}"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates'][target]


if __name__ == "__main__":
    app.run(debug=True)
```

Replace:

```
YOUR_API_KEY
```

with your ExchangeRate API key.

---

# Step 7 — Run Locally

```
python app.py
```

If testing locally, expose using ngrok:

```
ngrok http 5000
```

Copy the HTTPS URL into Dialogflow webhook settings.

---

# Git Setup

```
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

---

# Security Notes

* Do NOT commit API keys
* Do NOT commit Telegram bot token
* Use environment variables in production
* Add error handling for invalid currencies

---
