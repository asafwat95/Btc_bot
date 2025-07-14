import requests
import time
import json
import os

# --- بيانات البوت ---
TOKEN = '8051383197:AAHN18riDFBX_b-QW4tBjFYPdxT8YqT5oDk'
CHANNEL_ID = '@CryptoShip95'

# --- إعدادات المراقبة ---
PRICE_CHANGE_THRESHOLD = 0.001  # 1%
LAST_PRICE_FILE = 'last_btc_price.json'

def save_last_price(price):
    with open(LAST_PRICE_FILE, 'w') as f:
        json.dump({'last_price': price}, f)
    print(f"💾 تم حفظ آخر سعر: ${price:,.2f}")

def load_last_price():
    if os.path.exists(LAST_PRICE_FILE):
        try:
            with open(LAST_PRICE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_price')
        except json.JSONDecodeError:
            print("⚠️ خطأ في قراءة ملف آخر سعر.")
            return None
    return None

def get_btc_price_coingecko():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["bitcoin"]["usd"])
    except Exception as e:
        print("❌ خطأ في جلب السعر:", e)
        return None

def send_message(message_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        print("✅ تم إرسال الرسالة:", response.json())
    except Exception as e:
        print("❌ فشل الإرسال:", e)

# --- تنفيذ مرة واحدة فقط (لجدولة المهام) ---
if __name__ == "__main__":
    print(f"\n⏰ بدأ تنفيذ المهمة في {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC")

    last_price = load_last_price()
    current_price = get_btc_price_coingecko()

    if current_price is None:
        print("❌ لم يتم جلب السعر الحالي.")
        exit()

    if last_price is None:
        print(f"📌 لا يوجد سعر سابق. سيتم حفظ السعر الحالي: ${current_price:,.2f}")
        save_last_price(current_price)
        message_text = f"📢 سعر البيتكوين الآن: ${current_price:,.2f} 💰\n\nتم التحديث تلقائيًا عبر CryptoShip 🚢"
        send_message(message_text)
    else:
        price_change = abs((current_price - last_price) / last_price)
        if price_change >= PRICE_CHANGE_THRESHOLD:
            change_type = "📈 ارتفع" if current_price > last_price else "📉 انخفض"
            change_amount = abs(current_price - last_price)
            message_text = (
                f"📢 سعر البيتكوين الآن: ${current_price:,.2f} 💰\n"
                f"{change_type} بنسبة {price_change:.2%} (${change_amount:,.2f})\n\n"
                "تم التحديث تلقائيًا عبر CryptoShip 🚢"
            )
            send_message(message_text)
            save_last_price(current_price)
        else:
            print(f"🔍 لا يوجد تغيير كبير في السعر. السعر الحالي: ${current_price:,.2f}")

    print("✅ انتهى تنفيذ المهمة.")
