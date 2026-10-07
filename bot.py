import os
import json
import telebot
from flask import Flask
from threading import Thread

# Load token from Render settings
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "user_progress.json"

# Add your Telegram File IDs here
VIDEO_LIST = [
    "BAACAgUAAxkBAAIsnmrF4LJbQrnqZ70dvmFSUZwxPw8eAAI8IgAC9rAxVi443A7Xspl-PQQ",
    # Add more file IDs here separated by comma
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

# Handle /start command
@bot.message_handler(commands=['start'])
def send_next_video(message):
    user_id = str(message.from_user.id)
    progress = load_progress()
    
    current_index = progress.get(user_id, 0)
    
    # If all videos are watched
    if current_index >= len(VIDEO_LIST):
        bot.reply_to(message, "🎉 आपने हमारे सारे वीडियो देख लिए हैं! धन्यवाद।")
        return
        
    next_video = VIDEO_LIST[current_index]
    try:
        bot.send_video(
            message.chat.id, 
            next_video, 
            caption=f"वीडियो नंबर {current_index + 1} 🍿\n\nअगला वीडियो देखने के लिए दोबारा /start भेजें!"
        )
        progress[user_id] = current_index + 1
        save_progress(progress)
    except Exception as e:
        bot.reply_to(message, "❌ वीडियो भेजने में समस्या आई। कृपया अपनी File ID चेक करें।")

# Flask Server for Render 24/7 Keep-Alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is 24/7 Alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    
    # FIX: यह लाइन पुराने सभी Webhook कनेक्शन को डिलीट कर देगी ताकि एरर खत्म हो जाए
    print("Deleting old webhook...")
    bot.remove_webhook()
    
    print("Bot started successfully...")
    bot.infinity_polling()
    
