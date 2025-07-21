import requests
import time

# إعدادات API من حساب Cryptohopper
API_KEY = '9gZgRFZrzj5hh4y0tfNzs1gaozVYNl8BSBEhtNyDiyjevUOQv21QmGBrsCcEgvZQ'
API_SECRET = 'm719DnC6BjTYNaOhBEHJURe2RGMFQeigrakQjyOfL6UfPmKh6Sjs87BhWcXVwFbp'
BASE_URL = 'https://api.cryptohopper.com/v1'

# إعدادات بوت تيليجرام
BOT_TOKEN = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'
TARGET_CHAT_ID = '@Cryptoships95'  # مثال: @mychannel أو -100xxxxxx

HEADERS = {
    'Content-Type': 'application/json',
    'X-Auth-Key': API_KEY,
    'X-Auth-Secret': API_SECRET
}

def get_trades():
    url = f'{BASE_URL}/trades'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print("❌ Error fetching trades:", response.text)
        return []

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TARGET_CHAT_ID,
        'text': message
    }
    requests.post(url, json=payload)

def main():
    print("✅ Running Cryptohopper API Logger...")
    seen_ids = set()

    while True:
        trades = get_trades()
        for trade in trades:
            trade_id = trade.get('id')
            if trade_id and trade_id not in seen_ids:
                seen_ids.add(trade_id)
                message = f"{trade['type'].upper()} | {trade['currency']} | Amount: {trade['amount']} @ {trade['rate']}"
                print(message)
                send_to_telegram(message)

        time.sleep(60)  # كل دقيقة

if __name__ == '__main__':
    main()
