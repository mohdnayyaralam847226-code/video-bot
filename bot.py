import os
import telebot

# Bot Token environment variable se lega
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# /start command handle karne ke liye
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Mujhe koi bhi video bhejiye, main aapko uski File ID nikal kar dunga jise aap share kar sakte hain.")

# Video aane par uski file_id nikalne ke liye
@bot.message_handler(content_types=['video'])
def handle_video(message):
    video_file_id = message.video.file_id
    bot.reply_to(message, f"✅ Aapki video ki File ID ye hai:\n\n`{video_file_id}`\n\nIs ID ko use karke aap kisi ko bhi video share kar sakte hain!")

# Bot ko start karne ke liye
bot.infinity_polling()
