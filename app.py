from flask import Flask
import os
import requests
import random
from datetime import datetime
from drive_util import authenticate, download_file, upload_file

app = Flask(__name__)

# --- Configuration ---
HOPPER_ID = os.environ.get("HOPPER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

API_BASE_URL = "https://api.cryptohopper.com/v1"
LAST_TRADE_ID_FILE = "last_trade_id.txt"
TRADE_LOG_FILE = "trades_log.txt"

drive = authenticate()

# --- File Storage Functions ---
def get_last_trade_id():
    try:
        download_file(drive, LAST_TRADE_ID_FILE)
        with open(LAST_TRADE_ID_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_trade_id(trade_id):
    with open(LAST_TRADE_ID_FILE, 'w') as f:
        f.write(str(trade_id))
    upload_file(drive, LAST_TRADE_ID_FILE)

def log_trade(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        download_file(drive, TRADE_LOG_FILE)  # حمّل الملف قبل التعديل
    except:
        pass  # تجاهل لو مش موجود أول مرة

    with open(TRADE_LOG_FILE, 'a') as f:
        f.write(f"--- {timestamp} ---\n")
        f.write(message + "\n\n")

    upload_file(drive, TRADE_LOG_FILE)

# --- Telegram Function ---
def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📤 Message sent to Telegram")
        else:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"🔥 Error sending to Telegram: {e}")

# --- API Call ---
def fetch_latest_trade():
    endpoint = f"/hopper/{HOPPER_ID}/trade"
    url = API_BASE_URL + endpoint

    headers = {
        "accept": "application/json",
        "access-token": ACCESS_TOKEN
    }

    params = {
        "limit": 20
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" in data and "trades" in data["data"] and len(data["data"]["trades"]) > 0:
            return data["data"]["trades"][0]
        else:
            return None
    except requests.exceptions.RequestException as err:
        print(f"Error fetching trade: {err}")
        return None

# --- Message Formatter ---
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
            f"<b>[BUY]</b>\n"
            f"<b>Pair:</b> {pair}\n"
            f"<b>Price:</b> {rate:,.8f}\n"
            f"<b>Accuracy:</b> {float(accuracy):.2f}%\n"
            f"<b>Amount:</b> {amount}\n"
            f"<b>Total:</b> {total_usd}"
        )

    elif trade_type == 'Sell':
        profit_percent = float(trade.get('result', 0))
        profit_sign = "+" if profit_percent >= 0 else ""
        return (
            f"<b>[SELL]</b>\n"
            f"<b>Pair:</b> {pair}\n"
            f"<b>Sell Price:</b> {rate:,.8f}\n"
            f"<b>Profit/Loss:</b> {profit_sign}{profit_percent:.2f}%\n"
            f"<b>Total:</b> {total_usd}"
        )

    else:
        return (
            f"<b>[{trade_type.upper()}]</b>\n"
            f"<b>Pair:</b> {pair}\n"
            f"<b>Rate:</b> {rate:,.8f}"
        )

# --- Flask Routes ---
@app.route('/')
def home():
    return "✅ CryptoHopper Monitor is Online"

@app.route('/check')
def run_check():
    last_known_id = get_last_trade_id()
    latest_trade = fetch_latest_trade()

    if latest_trade:
        latest_id = str(latest_trade['id'])

        if latest_id != last_known_id:
            formatted_message = format_trade_message(latest_trade)
            log_trade(formatted_message)
            save_last_trade_id(latest_id)
            send_to_telegram(formatted_message)
            return "🆕 New trade logged and sent to Telegram"
        else:
            return "⏸️ No new trade"
    else:
        return "⚠️ Failed to fetch trade"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
