import os
import json
import telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN") 
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "user_progress.json"

# 🍿 यहाँ हम वीडियो लिस्ट रखेंगे। जब आपको असली IDs मिल जाएं, तो उन्हें यहाँ डालें
VIDEO_LIST = [
    "BAACAgUAAxkBAAIsnmrF4LJbQrnqZ70dvmFSUZwxPw8eAAI8IgAC9rAxVi443A7Xspl-PQQ"
]

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🎯 जादू वाला फीचर: जब आप अपने बॉट को कोई भी वीडियो भेजेंगे, तो यह असली एरर या File ID दिखाएगा
@bot.message_handler(content_types=['video'])
def get_real_video_id(message):
    try:
        file_id = message.video.file_id
        bot.reply_to(message, f"🎯 आपके इस बॉट की बिल्कुल असली File ID मिल गई है!\n\nइसे कॉपी करें:\n\n`{file_id}`")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# जब कोई /start दबाएगा
@bot.message_handler(commands=['start'])
def send_next_video(message):
    user_id = str(message.from_user.id)
    progress = load_progress()
    
    current_index = progress.get(user_id, 0)
    
    if current_index >= len(VIDEO_LIST):
        bot.reply_to(message, "🎉 आपने हमारे सारे वीडियो देख लिए हैं! धन्यवाद।")
        return
        
    next_video = VIDEO_LIST[current_index]
    try:
        bot.send_video(
            message.chat.id, 
            next_video, 
            caption=f"वीडियो नंबर {current_index + 1} 🍿\n\nअगला वीडियो देखने के लिए दोबारा /start भेजें!",
            has_spoiler=True
        )
        progress[user_id] = current_index + 1
        save_progress(progress)
    except Exception as e:
        # 🛠️ यहाँ यह असली कारण बताएगा कि टेलीग्राम वीडियो क्यों नहीं भेज रहा
        bot.reply_to(message, f"❌ टेलीग्राम एरर: {e}\n\nकृपया अपनी गैलरी से वीडियो सीधे इस बॉट को भेजें ताकि नई ID मिल सके।")

# 24 घंटे लाइव रखने के लिए वेब सर्वर
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    print("Bot started...")
    bot.infinity_polling()
    

@app.route('/')
def home():
    return "बॉट सफलतापूर्ण 24 घंटे लाइव है!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive() # वेब सर्वर शुरू करें
    bot.remove_webhook() # पुराना कनेक्शन डिलीट करें
    print("बॉट सफलतापूर्ण चालू हो गया है...")
    bot.infinity_polling()
    
    
