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

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("حيّ الله من لفانا! معك 'بدوي'، وش تبي نستشيره فيه؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من أن الرسالة نصية وليست أمراً
    user_text = update.message.text
    
    # رسالة مؤقتة لتوضيح أن البوت يفكر
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = model.generate_content(f"أنت بوت اسمك بدوي، ترد بلهجة بدوية أصيلة ومختصرة. العضو قال: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("يا خوي، واجهت مشكلة تقنية، حاول مرة ثانية!")
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # التعامل مع الأمر /start
    application.add_handler(CommandHandler('start', start))
    
    # التعامل مع أي رسالة نصية عادية (غير الأوامر)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
    
