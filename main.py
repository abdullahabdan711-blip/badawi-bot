import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# قراءة المفاتيح من إعدادات الموقع
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بدوي جاهز.. منشن لي وأبشر بـ جلدك!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if "بدوي" in user_text:
        # الطريقة المباشرة لطلب رد من Gemini بدون مكتبات معقدة
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": f"أنت بدوي فكاهي، طقطق على: {user_text}"}]}]}
        
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
            await update.message.reply_text(reply)
        except Exception as e:
            logging.error(f"خطأ اتصال: {e}")
            await update.message.reply_text("بدوي وده يطقطق بس الذكاء الاصطناعي مشغول!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)
    
