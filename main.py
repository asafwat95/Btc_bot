import requests
import os
import random

# --- Configuration ---
HOPPER_ID = os.environ.get("HOPPER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

API_BASE_URL = "https://api.cryptohopper.com/v1"
LAST_TRADE_ID_FILE = "last_trade_id.txt"

def get_last_trade_id():
    try:
        with open(LAST_TRADE_ID_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_trade_id(trade_id):
    with open(LAST_TRADE_ID_FILE, 'w') as f:
        f.write(str(trade_id))

def fetch_recent_trades():
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
        if "data" in data and "trades" in data["data"]:
            return data["data"]["trades"]
        else:
            return []
    except:
        return None

def format_trade_message(trade):
    trade_type = trade.get('type', 'N/A').capitalize()
    pair = trade.get('pair', 'N/A')
    rate = float(trade.get('rate', 0))
    amount = float(trade.get('amount', 0))
    total = float(trade.get('total', 0))

    if trade_type == 'Buy':
        icon = "🟢"
        message = (
            f"{icon} *New Buy Signal* {icon}\n\n"
            f"*Pair:* `{pair}`\n"
            f"*Price:* `{rate:,.8f}`\n"
            f"*Accuracy:* >= 90%"
        )
    elif trade_type == 'Sell':
        icon = "🔴"
        profit_percent = float(trade.get('result', 0))
        profit_sign = "+" if profit_percent >= 0 else ""
        message = (
            f"{icon} *New Sell Signal* {icon}\n\n"
            f"*Pair:* `{pair}`\n"
            f"*Price:* `{rate:,.8f}`\n"
            f"*Result:* `{profit_sign}{profit_percent:.2f}%`"
        )
    else:
        icon = "⚪️"
        message = (
            f"{icon} *New Trade: {trade_type}*\n\n"
            f"*Pair:* `{pair}`\n"
            f"*Rate:* `{rate:,.8f}`"
        )
    return message

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
