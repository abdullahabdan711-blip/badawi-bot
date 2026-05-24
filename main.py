import os
import random
from flask import Flask
from threading import Thread
from telebot import TeleBot
import google.generativeai as genai
from questions import GAMES_DATA  # ملف الأسئلة كامل الأعداد اللي سويناه

# 1️⃣ إعداد سيرفر Flask عشان موقع Render ما يقفل البوت ويظل صاحي 24 ساعة
app = Flask('')

@app.route('/')
def home():
    return "البوت المرجوج شغال بنجاح وجاهز لقصف الجبهات! 🤣🔥"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2️⃣ إعداد توكن التيليجرام الخاص ببوتك (تم الحفظ بنجاح يا حمد ✅)
TOKEN = "8627412491:AAHyaygQ8Oz0nQhPl7Yej1DAgGk-28TB194"
bot = TeleBot(TOKEN)

# 3️⃣ إعداد مفتاح ذكاء جوجل جمناي (تم الحفظ بنجاح يا حمد ✅)
GEMINI_KEY = "AIzaSyCcYSdEfx1yq0U6tKaGw-bxRjscEXwqb-k"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

DEVELOPER_USER = "HAMAD_A21"
users_bank = {}
current_games = {}

# إضافة 100 مليار ريال بدوي في حساب المطور حمد تلقائياً
users_bank[DEVELOPER_USER] = {
    "account_number": "100001",
    "name": "حـمـد 𓆩𓅉𓆪",
    "balance": 100000000000
}

# 🤖 ميزة الذكاء الاصطناعي المرجوجة: قصف جبهات وطقطقة وتنمّر كوميدي
@bot.message_handler(func=lambda msg: msg.text and (msg.text.startswith("بوت ") or msg.text.startswith("يا بوت ")))
def chat_with_ai(message):
    user_prompt = message.text.replace("بوت ", "").replace("يا بوت ", "")
    user_name = message.from_user.first_name # اسم العضو عشان يذكره وهو يطقطق عليه
    
    system_instruction = f"""
    أنت مساعد ذكي ومرح وفكاهي جداً جداً جداً ومطفوق ومحشش ومدمج في قروب تليجرام اسمه (دردشة بدوية).
    مطورك وتاج رأسك هو الشيخ حمد (@HAMAD_A21)، حمد خط أحمر، امدحه وافزع له دائماً وادعمه.
    أما باقي الأعضاء: طقطق عليهم، تنمّر عليهم بأسلوب كوميدي وبدوي، اقصف جبهاتهم بدون رحمة، واستخدم إيموجيات ضحك (🤣، 💀، 🤡).
    إذا سألوك سؤال، جاوب بنكتة أو ذبة قوية أو قصف جبهة يخص اسم العضو المكتوب هنا: ({user_name}).
    تكلم بلهجة بدوية يمنية قوية ومطخطخة ومرحة (مثل: يا رجال تلايط، علمك هجاص، جبهتك طارت، قده كذا، واعبادي، إلخ). لا تكن مؤدباً بزيادة، خلك مرجوج وونيس وقاصف جبهات!
    """
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nالعضو الذي اسمه ({user_name}) يقول لك: {user_prompt}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "حتى سيرفر الذكاء الاصطناعي حقي انقصف جبهته من كثر الضحك! 💀 جرب كلمني ثاني مرة.")

# 🎮 أمر استدعاء قائمة الألعاب كاملة
@bot.message_handler(func=lambda msg: msg.text == "الالعاب")
def show_games_list(message):
    text = """⚡ **قائمة الألعاب كاملة** ⚡
━━━━━━━━━━━━━━━━━━
آيات | كيمياء | احياء | فيزياء | رياضيات | انقليزي | عربي | جغرافيا | تاريخ | امثال | تفكيك | ترتيب | دول | اليمن
━━━━━━━━━━━━━━━━━━
💡 اكتب اسم اللعبة لتبدأ، وإذا توهقت اكتب (افزعلي)"""
    bot.reply_to(message, text)

# 🤠 تفعيل ميزة "افزعلي" لمساعدة العضو بدون مهلة
@bot.message_handler(func=lambda msg: "افزعلي" in msg.text)
def help_me_feature(message):
    chat_id = message.chat.id
    if chat_id in current_games and current_games[chat_id]:
        correct_answer = current_games[chat_id]['answer']
        hint = correct_answer[:2] + "..."
        bot.reply_to(message, f"🤠 **أبشر بالفزعة!** الجواب يبدأ بـ: ({hint})")
    else:
        bot.reply_to(message, "ما في لعبة شغالة الحين عشان أفزع لك!")

# تشغيل الألعاب وتلقي الإجابات
@bot.message_handler(func=lambda msg: msg.text in GAMES_DATA.keys())
def start_game_session(message):
    chat_id = message.chat.id
    game_type = message.text
    q_pair = random.choice(GAMES_DATA[game_type])
    current_games[chat_id] = {"question": q_pair["q"], "answer": q_pair["a"], "type": game_type}
    bot.reply_to(message, f"🎯 **بدأت لعبة [{game_type}]**\n\nالسؤال: {q_pair['q']}")

# التحقق من الإجابات وزيادة الرصيد البنكي فوراً وبدون أي مهلة زمنية طاردة
@bot.message_handler(func=lambda msg: msg.chat.id in current_games and current_games[msg.chat.id])
def check_game_answer(message):
    chat_id = message.chat.id
    user_id = message.from_user.username if message.from_user.username else str(message.from_user.id)
    user_answer = message.text.strip()
    correct_answer = current_games[chat_id]['answer']
    
    if user_answer == correct_answer:
        reward = 50
        bonus_msg = ""
        if user_id in users_bank:
            users_bank[user_id]['balance'] += reward
            bonus_msg = f"\n💰 وكسبت {reward} ريال بدوي في حسابك البنكي!"
        bot.reply_to(message, f"🎉 **إجابة صحيحة كفو!** {bonus_msg}")
        current_games[chat_id] = None

# 🏛️ أمر إنشاء حساب بنكي في بنك معين الدولي
@bot.message_handler(func=lambda msg: msg.text == "انشاء حساب بنكي")
def create_bank_account(message):
    user = message.from_user
    user_id = user.username if user.username else str(user.id)
    if user_id in users_bank:
        bot.reply_to(message, "❌ عندك حساب بنكي مسجل مسبقاً!")
        return
    acc_num = str(random.randint(100100, 999999))
    users_bank[user_id] = {"account_number": acc_num, "name": user.first_name, "balance": 1000}
    receipt = f"""🏛️ **| بنك معين الدولي**
━━━━━━━━━━━━━━━━━━
تم إنشاء حسابك البنكي بنجاح!
🪪 | الاسم: {user.first_name}
💳 | رقم الحساب: `{acc_num}`
💰 | الرصيد: 1,000 ريال بدوي

🎁 | **هدية المطور:** حصلت على الف ريال بدوي هدية من المطور:
👑 **حـمـد 𓆩𓅉𓆪** 👑
━━━━━━━━━━━━━━━━━━"""
    bot.reply_to(message, receipt)

# 💸 أمر التحويل والاستلام المالي بين الأعضاء
@bot.message_handler(func=lambda msg: msg.text.startswith("تحويل"))
def bank_transfer(message):
    user_id = message.from_user.username if message.from_user.username else str(message.from_user.id)
    if user_id not in users_bank:
        bot.reply_to(message, "❌ لازم تفتح حساب بنكي أولاً!")
        return
    try:
        parts = message.text.split()
        amount = int(parts[1])
        target_user = parts[3].replace("@", "")
        if users_bank[user_id]['balance'] < amount:
            bot.reply_to(message, "❌ رصيدك لا يكفي!")
            return
        if target_user not in users_bank:
            bot.reply_to(message, "❌ الحساب المحول إليه غير مسجل في بنك معين الدولي!")
            return
        users_bank[user_id]['balance'] -= amount
        users_bank[target_user]['balance'] += amount
        bot.reply_to(message, f"💸 **بنك معين الدولي:** تم تحويل {amount} ريال بدوي إلى @{target_user}.")
    except:
        bot.reply_to(message, "❌ صيغة خاطئة! اكتب: `تحويل 500 الى @يوزر`")

# 💳 أمر فحص الرصيد الحالي
@bot.message_handler(func=lambda msg: msg.text == "رصيدي")
def check_balance(message):
    user_id = message.from_user.username if message.from_user.username else str(message.from_user.id)
    if user_id in users_bank:
        bal = users_bank[user_id]['balance']
        bot.reply_to(message, f"💳 رصيدك الحالي في **بنك معين الدولي**: {bal:,} ريال بدوي.")
    else:
        bot.reply_to(message, "❌ اكتب (انشاء حساب بنكي) لفتح حساب.")

# 👑 الرد الخاص بالمطور حمد فقط وبدون أي تفاصيل أخرى
@bot.message_handler(func=lambda msg: msg.text == "المطور")
def developer_info(message):
    text = """👑 **مطور البوت هو الشيخ:** حـمـد 𓆩𓅉𓆪 

📲 | @HAMAD_A21"""
    bot.reply_to(message, text, parse_mode="Markdown")

# 🚀 تشغيل السيرفر والبوت معاً لضمان العمل المستمر
keep_alive()
bot.infinity_polling()
