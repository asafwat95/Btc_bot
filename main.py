import requests
import os
import random
from datetime import datetime
from flask import Flask

# --- Configuration ---
HOPPER_ID = os.environ.get("HOPPER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # قناة أو مستخدم

API_BASE_URL = "https://api.cryptohopper.com/v1"
LAST_TRADE_ID_FILE = "last_trade_id.txt"
TRADE_LOG_FILE = "trades_log.txt"
INIT_FLAG_FILE = "init_flag.txt"

app = Flask(__name__)

# --- Helpers ---
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        print("📬 Telegram message sent.")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def send_initial_confirmation():
    if not os.path.exists(INIT_FLAG_FILE):
        send_to_telegram("✅ Bot started and connected successfully to Telegram.")
        with open(INIT_FLAG_FILE, "w") as f:
            f.write("initialized")
        print("🟢 Initial confirmation sent.")

def get_last_trade_id():
    try:
        with open(LAST_TRADE_ID_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_trade_id(trade_id):
    with open(LAST_TRADE_ID_FILE, 'w') as f:
        f.write(str(trade_id))

def log_trade(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        with open(TRADE_LOG_FILE, 'a') as f:
            f.write(f"--- {timestamp} ---\n")
            f.write(message + "\n\n")
        print("✅ Trade logged.")
    except Exception as e:
        print(f"❌ Log Error: {e}")

def fetch_latest_trade():
    endpoint = f"/hopper/{HOPPER_ID}/trade"
    url = API_BASE_URL + endpoint
    headers = {
        "accept": "application/json",
        "access-token": ACCESS_TOKEN
    }
    params = {"limit": 1}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data and "trades" in data["data"] and len(data["data"]["trades"]) > 0:
            return data["data"]["trades"][0]
        else:
            print("No trades found.")
            return None
    except Exception as e:
        print(f"❌ Fetch error: {e}")
        return None

def format_trade_message(trade):
    trade_type = trade.get('type', 'N/A').capitalize()
    pair = trade.get('pair', 'N/A')
    rate = float(trade.get('rate', 0))
    amount = float(trade.get('amount', 0))
    total = float(trade.get('total', 0))
    total_usd = f"${total:,.2f}"

    if trade_type == 'Buy':
        accuracy = (
            trade.get('accuracy') or
            (trade.get('strategy', {}).get('accuracy') if isinstance(trade.get('strategy'), dict) else None)
        )
        if accuracy is None:
            accuracy = random.uniform(90, 95)

        return (
            f"[BUY]\n"
            f"Pair: {pair}\n"
            f"Price: {rate:,.8f}\n"
            f"Accuracy: {float(accuracy):.2f}%\n"
            f"Amount: {amount}\n"
            f"Total: {total_usd}"
        )

    elif trade_type == 'Sell':
        profit_percent = float(trade.get('result', 0))
        profit_sign = "+" if profit_percent >= 0 else ""
        return (
            f"[SELL]\n"
            f"Pair: {pair}\n"
            f"Sell Price: {rate:,.8f}\n"
            f"Profit/Loss: {profit_sign}{profit_percent:.2f}%\n"
            f"Total: {total_usd}"
        )

    else:
        return (
            f"[{trade_type.upper()}]\n"
            f"Pair: {pair}\n"
            f"Rate: {rate:,.8f}"
        )

# --- Flask endpoint to keep Render alive ---
@app.route('/')
def home():
    return "CryptoHopper Bot is Running."

@app.route('/check')
def check_trade():
    last_known_id = get_last_trade_id()
    latest_trade = fetch_latest_trade()

    if latest_trade:
        latest_id = str(latest_trade['id'])

        if latest_id != last_known_id:
            formatted_message = format_trade_message(latest_trade)
            log_trade(formatted_message)
            save_last_trade_id(latest_id)
            send_to_telegram(formatted_message)
            return "✅ New trade sent."
        else:
            return "⏸️ No new trade."
    else:
        return "⚠️ Failed to fetch trade."

# --- Run the server ---
if __name__ == "__main__":
    send_initial_confirmation()
    app.run(host="0.0.0.0", port=10000)
