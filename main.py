import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
# موديلاً قوياً للفكاهة
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا باللي جو.. توني كنت أقول يا ليت يجي أحد نضحك عليه شوي! وش تبي يا راعي المشاكل؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # الشخصية الجديدة: بدوي "مطقطق" وما يرحم
    prompt = (
        f"أنت بوت اسمك 'بدوي'، شخصيتك فكاهية جداً، وقح قليلاً، تحب الطقطقة (السخرية)، وتقصف جبهات الأعضاء بلهجة بدوية أصيلة وقوية. "
        f"لا تكن مؤدباً، بل كن مسلياً واجعل ردك مليئاً بالاستهزاء المرح. "
        f"العضو قال: {user_text}"
    )
    
    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("يا رجال خربت الطقطقة.. السيرفر معلق، خلني أعدل شماغي وأرجع لك!")
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)
    
