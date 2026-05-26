import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import google.generativeai as genai

# تحميل الإعدادات
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد Gemini - نستخدم موديل أحدث وأكثر استقراراً
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("حيّ الله من لفانا! معك 'بدوي'، وش تبي نستشيره فيه؟")

async def chat_with_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من أن الرسالة تحتوي على نص
    if update.message and update.message.text:
        user_text = update.message.text
        try:
            response = model.generate_content(f"أنت بوت اسمك بدوي، ترد بلهجة بدوية أصيلة ومختصرة. العضو قال: {user_text}")
            await update.message.reply_text(response.text)
        except Exception as e:
            await update.message.reply_text("يا خوي، واجهت مشكلة تقنية، حاول مرة ثانية!")
            logging.error(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    # فلتر لضمان معالجة الرسائل النصية فقط وتجنب الأخطاء
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_with_gemini))
    
    application.run_polling()
    
