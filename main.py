from flask import Flask
import requests
import json
import os

# إعدادات البوت
TOKEN = "8051383197:AAHN18riDFBX_b-QW4tBjFYPdxT8YqT5oDk"
CHANNEL_ID = "@CryptoShip95"
LAST_PRICE_FILE = "last_btc_price.json"
PRICE_CHANGE_THRESHOLD = 0.005  # 1%

app = Flask(__name__)

def save_last_price(price):
    with open(LAST_PRICE_FILE, 'w') as f:
        json.dump({'last_price': price}, f)

def load_last_price():
    if os.path.exists(LAST_PRICE_FILE):
        with open(LAST_PRICE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_price')
    return None

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data["bitcoin"]["usd"])

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text})

@app.route('/')
def run_bot():
    current_price = get_btc_price()
    last_price = load_last_price()

    if last_price is None:
        message = f"📢 سعر البيتكوين الأولي: ${current_price:,.2f} 💰\nتم التحديث تلقائيًا عبر CryptoShip 🚢"
        send_message(message)
        save_last_price(current_price)
        return "✅ Sent Initial Price"

    change = abs((current_price - last_price) / last_price)
    if change >= PRICE_CHANGE_THRESHOLD:
        change_type = "📈 ارتفع" if current_price > last_price else "📉 انخفض"
        message = (
            f"📢 سعر البيتكوين الآن: ${current_price:,.2f} 💰\n"
            f"{change_type} بنسبة {change:.2%}\nتم التحديث عبر CryptoShip 🚢"
        )
        send_message(message)
        save_last_price(current_price)
        return "✅ Sent Updated Price"
    else:
        return "⏳ لا تغيير ملحوظ في السعر."

if __name__ == '__main__':
    app.run()
