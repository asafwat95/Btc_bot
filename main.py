import requests
import time

# إعدادات API من حساب Cryptohopper - ملاحظة: لا تشارك هذه المفاتيح علنًا!
API_KEY = '9gZgRFZrzj5hh4y0tfNzs1gaozVYNl8BSBEhtNyDiyjevUOQv21QmGBrsCcEgvZQ'
API_SECRET = 'm719DnC6BjTYNaOhBEHJURe2RGMFQeigrakQjyOfL6UfPmKh6Sjs87BhWcXVwFbp'
BASE_URL = 'https://api.cryptohopper.com/v1'

# إعدادات بوت تيليجرام - ملاحظة: لا تشارك هذا الرمز المميز علنًا!
BOT_TOKEN = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'
TARGET_CHAT_ID = '@Cryptoships95'  # مثال: @mychannel أو -100xxxxxx

HEADERS = {
    'Content-Type': 'application/json',
    'X-Auth-Key': API_KEY,
    'X-Auth-Secret': API_SECRET
}

def get_trades():
    """
    يجلب بيانات التداولات من Cryptohopper API.
    """
    url = f'{BASE_URL}/trade' # تصحيح: كان 'trades' والوثائق تشير إلى 'trade' لنقاط النهاية الفردية، لكن إذا كان الغرض هو قائمة التداولات، 'trades' قد يكون صحيحًا.
                               # إذا واجهت مشاكل، جرب 'f'{BASE_URL}/trade/all' أو راجع وثائق API لـ Cryptohopper الخاصة بنقطة نهاية التداولات.
                               # بناءً على سلوك الكود الأصلي الذي يكرر عبر 'trades'، فإن 'trades' هو الأرجح نقطة النهاية الصحيحة لقائمة.
                               # سأفترض 'trades' هو الصحيح كما في الكود الأصلي.
    url = f'{BASE_URL}/trades' # العودة إلى 'trades' على افتراض أنه نقطة النهاية الصحيحة للقائمة.

    try:
        response = requests.get(url, headers=HEADERS, timeout=10) # إضافة مهلة للطلب
        response.raise_for_status() # يثير استثناء لأكواد حالة HTTP 4xx/5xx
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في جلب التداولات: {e}")
        return []

def send_to_telegram(message):
    """
    يرسل رسالة إلى قناة/مجموعة تيليجرام المستهدفة.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TARGET_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown' # يمكن استخدامه لتنسيق أفضل، اختياري
    }
    try:
        response = requests.post(url, json=payload, timeout=5) # إضافة مهلة
        response.raise_for_status() # يثير استثناء لأكواد حالة HTTP 4xx/5xx
        # print(f"✅ تم إرسال رسالة تيليجرام بنجاح: {message}") # يمكن تفعيلها للتصحيح
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في إرسال رسالة تيليجرام: {e}")

def main():
    """
    الدالة الرئيسية لمراقبة تداولات Cryptohopper وإرسال الإشعارات.
    """
    print("✅ جاري تشغيل مسجل API الخاص بـ Cryptohopper...")
    seen_ids = set()
    # لتجنب إرسال "لا يوجد أوامر" كل دقيقة إذا لم تكن هناك أوامر
    last_no_orders_sent_time = 0
    # إرسال رسالة "لا يوجد أوامر" مرة واحدة كل 30 دقيقة إذا لم يكن هناك جديد
    NO_ORDERS_MESSAGE_INTERVAL_SECONDS = 30 * 60

    while True:
        trades = get_trades()
        new_trades_found_in_this_cycle = False

        if not trades:
            # إذا كانت قائمة التداولات فارغة تمامًا من API
            if time.time() - last_no_orders_sent_time > NO_ORDERS_MESSAGE_INTERVAL_SECONDS:
                message_no_orders = "لا يوجد أوامر جديدة الآن."
                print(message_no_orders)
                send_to_telegram(message_no_orders)
                last_no_orders_sent_time = time.time()
        else:
            # تم جلب تداولات، الآن نتحقق من الجديد منها
            for trade in trades:
                trade_id = trade.get('id')
                # استخدام .get() مع قيمة افتراضية لجعل الوصول إلى البيانات أكثر أمانًا
                trade_type = trade.get('type', 'غير معروف').upper()
                currency = trade.get('currency', 'N/A')
                amount = trade.get('amount', 'N/A')
                rate = trade.get('rate', 'N/A')

                if trade_id and trade_id not in seen_ids:
                    seen_ids.add(trade_id)
                    message = (
                        f"**{trade_type}** | `{currency}` | الكمية: `{amount}` | السعر: `{rate}`\n"
                        f"معرف التداول: `{trade_id}`" # إضافة معرف التداول لسهولة التتبع
                    )
                    print(message)
                    send_to_telegram(message)
                    new_trades_found_in_this_cycle = True

            # إذا تم العثور على تداولات جديدة في هذه الدورة، قم بإعادة تعيين مؤقت "لا يوجد أوامر"
            if new_trades_found_in_this_cycle:
                last_no_orders_sent_time = 0 # إعادة تعيين المؤقت للسماح بإرسال الرسالة فورًا إذا توقفت الأوامر لاحقًا
            elif time.time() - last_no_orders_sent_time > NO_ORDERS_MESSAGE_INTERVAL_SECONDS:
                # إذا لم يتم العثور على أي أوامر جديدة (كلها كانت موجودة في seen_ids)
                # وإذا انقضى الوقت الكافي منذ آخر رسالة "لا يوجد أوامر"
                message_no_orders = "لا يوجد أوامر جديدة الآن."
                print(message_no_orders)
                send_to_telegram(message_no_orders)
                last_no_orders_sent_time = time.time()


        time.sleep(60)  # الانتظار لمدة دقيقة واحدة قبل التحقق مرة أخرى

if __name__ == '__main__':
    main()

