import requests
import os
import logging

# إعداد اللوج
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# بيئة التشغيل
HOPPER_ID = os.environ.get("HOPPER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
API_URL = f"https://api.cryptohopper.com/v1/hopper/{HOPPER_ID}/trade"
LAST_ID_FILE = "last_id.txt"


def get_last_id():
    try:
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_id(trade_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(trade_id))

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        logging.info("✅ Sent to Telegram")
    except Exception as e:
        logging.error(f"❌ Telegram error: {e}")

def fetch_trades():
    headers = {
        "access-token": ACCESS_TOKEN,
        "accept": "application/json"
    }
    params = {"limit": 20}
    try:
        res = requests.get(API_URL, headers=headers, params=params)
        res.raise_for_status()
        return res.json().get("data", {}).get("trades", [])
    except Exception as e:
        logging.error(f"❌ Error fetching trades: {e}")
        return []

def format_trade(trade):
    trade_type = trade.get("type", "").capitalize()
    pair = trade.get("pair", "")
    rate = float(trade.get("rate", 0))
    result = float(trade.get("result", 0))

    if trade_type == "Buy":
        icon = "🟢"
        return f"{icon} *Buy Signal*\nPair: `{pair}`\nPrice: `{rate:,.8f}`"
    elif trade_type == "Sell":
        icon = "🔴"
        sign = "+" if result >= 0 else ""
        return f"{icon} *Sell Signal*\nPair: `{pair}`\nPrice: `{rate:,.8f}`\nResult: `{sign}{result:.2f}%`"
    else:
        return f"⚪️ *{trade_type}*\nPair: {pair}"

def run_bot():
    last_id = get_last_id()
    trades = fetch_trades()

    new_trades = []
    for trade in trades:
        if str(trade["id"]) == last_id:
            break
        new_trades.append(trade)

    if not new_trades:
        logging.info("No new trades.")
        return "No new trades."

    new_trades.reverse()
    for trade in new_trades:
        msg = format_trade(trade)
        send_telegram(msg)
        logging.info(f"Trade sent: {msg}")

    save_last_id(str(trades[0]["id"]))
    return f"✅ Processed {len(new_trades)} trade(s)."
