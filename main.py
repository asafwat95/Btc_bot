from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# توكن البوت الخاص بك (استبدل 'YOUR_BOT_TOKEN_HERE' بالتوكن الفعلي)
BOT_TOKEN = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'
# معرف القناة - تأكد أن البوت أدمن فيها (استبدل '@your_channel_username' أو الرقم الفعلي)
CHANNEL_ID = '@Cryptoships95'  # مثال: '-1001234567890' للقنوات الخاصة

# دالة عند استلام أي رسالة نصية (ليست أمر)
async def forward_last_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تحقق مما إذا كانت الرسالة موجودة وتحتوي على نص
    if update.message and update.message.text:
        message_text = update.message.text
        # أرسل الرسالة إلى القناة
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message_text)
    elif update.message and update.message.photo:
        # إذا كانت الرسالة صورة، قم بإعادة توجيهها
        # ملاحظة: إعادة توجيه الصور قد تتطلب صلاحيات خاصة أو التعامل مع الملفات.
        # للحصول على أسهل طريقة، يمكن إعادة توجيهها مباشرة.
        await context.bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    elif update.message and update.message.document:
        # إذا كانت الرسالة ملفًا، قم بإعادة توجيهها
        await context.bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    elif update.message and update.message.video:
        # إذا كانت الرسالة فيديو، قم بإعادة توجيهها
        await context.bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    # يمكنك إضافة المزيد من الشروط لأنواع الرسائل الأخرى مثل الملصقات، الأصوات، إلخ.

# دالة للتعامل مع أمر البدء (Start command) إذا أردت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا بوت لإعادة توجيه الرسائل.")

def main():
    # إنشاء كائن التطبيق (Application)
    # ملاحظة: لم نعد نستخدم Updater هنا.
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة المعالجات (Handlers)
    # المعالج لأمر /start
    application.add_handler(CommandHandler("start", start))

    # المعالج لجميع الرسائل النصية التي ليست أوامر
    # filters.TEXT & ~filters.COMMAND يعني "نص وليس أمراً"
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_last_message))
    
    # معالج لإعادة توجيه الصور، الفيديو، والملفات (الوثائق)
    # يمكنك إضافة المزيد من أنواع الفلاتر هنا حسب حاجتك
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.DOCUMENT, 
        forward_last_message
    ))

    # بدء تشغيل البوت (Polling)
    # ملاحظة: لم نعد نستخدم updater.start_polling() و updater.idle()
    print("البوت يعمل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
