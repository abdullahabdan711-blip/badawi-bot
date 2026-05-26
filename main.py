import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداداتك (تأكد إنها محفوظة في الموقع)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بدوي جاهز.. نادني بأي وقت وأبشر بـ جلدك!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # "بدوي" الآن يسمع إذا ذكرت اسمه أو منشنته
    if "بدوي" in user_text or (context.bot.username and f"@{context.bot.username}" in user_text):
        try:
            # هنا Gemini يحلل الرسالة ويرد بأسلوبه البدوِي
            response = model.generate_content(f"أنت بدوي فكاهي، طقطق على العضو بذكاء. الرسالة: {user_text}")
            await update.message.reply_text(response.text)
        except Exception as e:
            logging.error(f"خطأ: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)
    
