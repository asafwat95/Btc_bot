import requests
import json

# توكن البوت ومعرف القناة
bot_token = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'
channel_id = '@Cryptoships95'

# توكن الدخول إلى Cryptohopper
access_token = '[0b823d65aef292e7ab38f6232ceeb840205484cb]'

# API الخاص بـ Cryptohopper
base_url = 'https://api.cryptohopper.com/v1/'
endpoint = 'hopper'
uri = base_url + endpoint

# الهيدر فيه التوكن
headers = {
    'access-token': access_token
}

# إرسال طلب لجلب بيانات hoppers
response = requests.get(uri, headers=headers)
data = response.json()

# تحويل البيانات إلى نص منسق (اختياري)
formatted_data = json.dumps(data, indent=2)

# إرسال البيانات لقناة تيليجرام
telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
payload = {
    'chat_id': channel_id,
    'text': f'📊 Hopper Data:\n<pre>{formatted_data}</pre>',
    'parse_mode': 'HTML'
}

telegram_response = requests.post(telegram_url, data=payload)

# طباعة نتيجة الإرسال (اختياري)
print(telegram_response.json())
