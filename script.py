import requests
import os
from datetime import datetime

# --- Configuration ---
HOPPER_ID = os.environ.get("HOPPER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

API_BASE_URL = "https://api.cryptohopper.com/v1"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

LAST_TRADE_ID_FILE = "last_trade_id.txt"
TRADE_LOG_FILE = "trades_log.txt"
SAVED_IDS_FILE = "saved_trade_ids.txt"

def get_last_trade():
    url = f"{API_BASE_URL}/hopper/{HOPPER_ID}/trade-history"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        trades = response.json().get("data", {}).get("trades", [])
        return trades[0] if trades else None
    else:
        print("Error fetching trades:", response.text)
        return None

def read_file(filename):
    if not os.path.exists(filename):
        return ""
    with open(filename, "r") as f:
        return f.read().strip()

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def append_to_file(filename, content):
    with open(filename, "a") as f:
        f.write(content + "\n")

def load_saved_ids():
    if not os.path.exists(SAVED_IDS_FILE):
        return set()
    with open(SAVED_IDS_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_new_id(trade_id):
    with open(SAVED_IDS_FILE, "a") as f:
        f.write(trade_id + "\n")

def main():
    trade = get_last_trade()
    if not trade:
        return

    trade_id = str(trade["id"])
    saved_ids = load_saved_ids()

    if trade_id in saved_ids:
        print("No new trade.")
        return

    # سجل البيانات الجديدة
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trade_data = f"[{timestamp}] ID: {trade_id}, Type: {trade['type']}, Amount: {trade['amount']}, Rate: {trade['rate']}, Total: {trade['total']}, Pair: {trade['currency_pair']}"
    print("New Trade:", trade_data)

    append_to_file(TRADE_LOG_FILE, trade_data)
    write_file(LAST_TRADE_ID_FILE, trade_id)
    save_new_id(trade_id)

if __name__ == "__main__":
    main()
