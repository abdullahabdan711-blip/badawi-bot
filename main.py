import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداد المفاتيح من البيئة مباشرة
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# تغيير الموديل إلى 'gemini-1.0-pro' (هذا يعمل في كل الحالات ولا يسبب خطأ 404)
model = genai.GenerativeModel('gemini-1.0-pro')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أبشر بسعدك! أنا 'بدوي' الذكي، منشن لي بأي شي وأنا أعطيك الرد.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # شرط: يرد إذا ذكرت كلمة "بدوي"
    if "بدوي" in user_text:
        try:
            response = model.generate_content(f"أنت بوت اسمك بدوي، ترد بلهجة بدوية أصيلة وفكاهية. العضو قال: {user_text}")
            await update.message.reply_text(response.text)
        except Exception as e:
            logging.error(f"خطأ Gemini: {e}")
            await update.message.reply_text("يا خوي، السيرفر معلق، حاول مرة ثانية!")

if __name__ == '__main__':
    # استخدم التوكن الذي وضعته أنت في متغير البيئة TELEGRAM_TOKEN
    application = ApplicationBuilder().token(os.environ.get('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)
    
