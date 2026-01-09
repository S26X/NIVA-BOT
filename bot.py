import telebot
from telebot import types
import os

# আপনার বটের তথ্য
TOKEN = '8397437725:AAHL1xtvXy7SE6UbbQiN68lwmsLzgXMtOvc'
ADMIN_ID = 7665757155  # আপনার আইডি বসিয়ে দিয়েছি

bot = telebot.TeleBot(TOKEN)
USER_FILE = "users.txt"

# ইউজার আইডি সেভ করার ফাংশন
def save_user(chat_id):
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    if str(chat_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(str(chat_id) + "\n")

# স্টার্ট কমান্ড বা ওয়েলকাম মেসেজ
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    user_name = message.from_user.first_name
    
    welcome_text = (
        f"Welcome Back, {user_name}! ফাস্টেস্ট সেলিং, সেরা নিরাপত্তা!\n\n"
        "প্রতারণাময় মার্কেটে আপনার আস্থার একমাত্র প্রতীক, আমাদের BOT!\n"
        "যখন পুরো মার্কেট প্রতারণায় পূর্ণ, তখন আমরা দিচ্ছি—\n"
        "✅ ফাস্টেস্ট কয়েন সেলের গ্যারান্টি\n"
        "✅ সহজ হিসাবে ১০০% নিরাপদ লেনদেনের নিশ্চয়তা।\n\n"
        "Niva, NS, সহ সব ধরনের Coin সহজেই সেল করতে নিচে থাকা Order Now বাটনে ক্লিক করুন।"
    )
    
    # বাটন সেটআপ
    markup = types.InlineKeyboardMarkup()
    # এখানে আপনার বটের ইউজারনেম অনুযায়ী অ্যাপ লিঙ্ক দিন (আমি আপনার বটের নাম অনুযায়ী দিয়েছি)
    app_url = "https://t.me/NivaZoneBot/app" 
    btn = types.InlineKeyboardButton("Order Now 🛒", url=app_url)
    markup.add(btn)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# ব্রডকাস্ট মেসেজ (অ্যাডমিন যখন SEND: লিখে কিছু পাঠাবে)
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def broadcast(message):
    if message.text.startswith("SEND:"):
        msg_to_send = message.text.replace("SEND:", "").strip()
        
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                users = f.read().splitlines()
            
            success = 0
            for uid in users:
                try:
                    bot.send_message(uid, msg_to_send)
                    success += 1
                except:
                    continue
            bot.reply_to(message, f"✅ সফল হয়েছে! মোট {success} জন ইউজার মেসেজটি পেয়েছে।")
    else:
        # অ্যাডমিন কোনো সাধারণ মেসেজ দিলে তাকে নিয়ম মনে করিয়ে দিবে
        bot.reply_to(message, "সবার কাছে মেসেজ পাঠাতে চাইলে লিখুন- \nSEND: আপনার মেসেজ")

print("বটটি এখন চালু আছে... (পিসি বন্ধ করবেন না)")
bot.polling()
