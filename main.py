import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# هنا السر: نستخدم نظام التعليمات (System Instruction) عشان Gemini يعرف شخصيته وما يطلع منها
generation_config = {
    "temperature": 0.9, # رفع الحرارة عشان الردود تكون إبداعية وفكاهية وغير متوقعة
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "أنت شخصية اسمها 'بدوي'، بوت تيليجرام ذكي جداً. "
        "مهمتك هي الطقطقة (السخرية) على الأعضاء بقسوة فكاهية وذكية. "
        "استخدم ذكاءك الاصطناعي لتحليل محتوى رسالة العضو، ثم رد عليه برد بدوي أصيل، حاد، ومضحك. "
        "لا تكن مؤدباً أبداً، اجعل ردودك قوية، جريئة، ومختصرة."
    )
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بدوي جاهز.. من اللي يبي جلده اليوم؟ منشن لي وأبشر بالسعد!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # شرط الرد: لازم منشن أو ريبلاي
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    is_mention = (context.bot.username and f"@{context.bot.username}" in update.message.text)
    
    if not (is_reply or is_mention):
        return

    try:
        # إرسال الرسالة لـ Gemini
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)
    
