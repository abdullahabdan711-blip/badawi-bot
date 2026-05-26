import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداد الـ Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بدوي جاهز.. منشن لي وأبشر بـ جلدك!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # نجعل البوت لا يرد إلا إذا ذكرت اسمه "بدوي"
    # هذا يمنع البوت من الرد على الرسائل الجانبية أو الترحيب المكرر
    if "بدوي" in user_text:
        try:
            # طلب الرد من الذكاء الاصطناعي
            response = model.generate_content(f"أنت شخصية بدوية فكاهية ووقحة، طقطق على العضو بذكاء وقسوة فكاهية. العضو قال: {user_text}")
            await update.message.reply_text(response.text)
        except Exception as e:
            logging.error(f"خطأ Gemini: {str(e)}")
            # لا نرد برسالة "معلق" لتجنب الإزعاج، نكتفي بالتسجيل في الـ Logs

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('TELEGRAM_TOKEN')).build()
    
    # إضافة الأوامر والرسائل
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling(drop_pending_updates=True)
    
