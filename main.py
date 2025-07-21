from telegram.ext import Application, MessageHandler, filters # تم تغيير الاستيرادات

import json

# ===== إعدادات البوت =====
BOT_TOKEN = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'  # استبدل هذا بالتوكن من BotFather
TARGET_CHAT_ID = '@Cryptoships95'  # مثال: @my_channel أو -123456789 للمجموعة

# ===== ملف حفظ العمليات =====
LOG_FILE = 'trades.json'

# تحميل السجل الحالي إن وُجد
try:
    with open(LOG_FILE, 'r') as f:
        trades = json.load(f)
except FileNotFoundError:
    trades = []

# التحقق إذا كانت الرسالة عملية تداول
def is_trade_message(text):
    text = text.lower()
    return (
        'buy order has been placed' in text or
        'sell order has been placed' in text or
        'hop completed on market' in text
    )

# التعامل مع الرسائل
# لاحظ أن update و context لم يتغيرا في البارامترات
def handle_message(update, context):
    message = update.message.text
    if message and is_trade_message(message):
        trades.append(message)
        with open(LOG_FILE, 'w') as f:
            json.dump(trades, f, indent=2)

        # إعادة إرسال الرسالة
        context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message)

# تشغيل البوت
def main():
    # هذا السطر تغير بشكل كبير: استخدام Application.builder()
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة الـ handler: لاحظ استخدام filters.TEXT و filters.COMMAND (حرف صغير)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is listening for Cryptohopper messages...")
    # بدء تشغيل البوت: run_polling بدلاً من start_polling و idle
    application.run_polling() 
    # يمكنك استخدام application.run_forever() إذا كنت تفضل ذلك، لكن run_polling() كافية هنا

if __name__ == '__main__':
    main()
