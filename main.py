import requests
import os
import random

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
        return data.get("data", {}).get("trades", [])
    except Exception as e:
        print(f"Error fetching trades: {e}")
        return None

def format_trade_message(trade):
    trade_type = trade.get('type', 'N/A').capitalize()
    pair = trade.get('pair', 'N/A')
    rate = float(trade.get('rate', 0))

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
        sign = "+" if profit_percent >= 0 else ""
        message = (
            f"{icon} *New Sell Signal* {icon}\n\n"
            f"*Pair:* `{pair}`\n"
            f"*Price:* `{rate:,.8f}`\n"
            f"*Result:* `{sign}{profit_percent:.2f}%`"
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
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def run_bot():
    output_logs = []

    last_known_id = get_last_trade_id()
    output_logs.append(f"Last known ID: {last_known_id}")
    
    recent_trades = fetch_recent_trades()
    if recent_trades is None:
        output_logs.append("Failed to fetch trades.")
        return "\n".join(output_logs)

    new_trades = []
    for trade in recent_trades:
        if str(trade['id']) == last_known_id:
            break
        new_trades.append(trade)

    if not new_trades:
        output_logs.append("No new trades.")
        return "\n".join(output_logs)

    new_trades.reverse()
    for trade in new_trades:
        msg = format_trade_message(trade)
        success = send_telegram_message(msg)
        output_logs.append(f"Sent trade ID {trade.get('id')} - Success: {success}")

    save_last_trade_id(recent_trades[0]['id'])
    output_logs.append(f"Saved latest ID: {recent_trades[0]['id']}")

    return "\n".join(output_logs)
