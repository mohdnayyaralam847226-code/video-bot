import os
import json
import telebot
from flask import Flask
from threading import Thread

# Render की सेटिंग्स (Environment Variables) से टोकन अपने आप लोड हो जाएगा
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "user_progress.json"

# 🍿 यहाँ अपने वीडियो की टेलीग्राम File IDs भरें (लाइन से कोमा लगाकर)
# मैंने आपकी पहली आईडी यहाँ डाल दी है, आगे और आईडी इसी तरह नीचे बढ़ाते जाएं
VIDEO_LIST = [
    "BAACAgUAAxkBAAIso2rF4O_GbchSmAEu7LoU9sWDzzsjAAI-IgAC9rAxVoHtNyZxETtzPQQ",
    # "यहाँ_दूसरे_वीडियो_की_File_ID_डालें",
    # "यहाँ_तीसरे_वीडियो_की_File_ID_डालें"
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

# जब कोई भी यूजर बॉट में /start भेजेगा
@bot.message_handler(commands=['start'])
def send_next_video(message):
    user_id = str(message.from_user.id)
    progress = load_progress()
    
    # पता करें कि यूजर अभी किस नंबर के वीडियो पर है
    current_index = progress.get(user_id, 0)
    
    # अगर यूजर ने लिस्ट के सारे वीडियो देख लिए हैं
    if current_index >= len(VIDEO_LIST):
        bot.reply_to(message, "chutiya adii")
        return
        
    next_video = VIDEO_LIST[current_index]
    try:
        # has_spoiler=True की वजह से वीडियो अपने आप धुंधला (Blur) होकर जाएगा
        bot.send_video(
            message.chat.id, 
            next_video, 
            caption=f"वीडियो नंबर {current_index + 1} 🍿\n\n🫤beta agla video dekhne ke le💨 /start भेजें!",
            has_spoiler=True
        )
        # यूजर का नंबर 1 आगे बढ़ाएं ताकि अगली बार अगला वीडियो जाए
        progress[user_id] = current_index + 1
        save_progress(progress)
    except Exception as e:
        bot.reply_to(message, "❌ वीडियो भेजने में समस्या आई। कृपया अपनी File ID चेक करें।")

# --- Render को 24 घंटे ऑनलाइन रखने के लिए वेब सर्वर ---
app = Flask('')

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
    
    
