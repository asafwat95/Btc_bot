from telegram.ext import Updater, MessageHandler, Filters
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
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Bot is listening for Cryptohopper messages...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
