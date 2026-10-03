import os
from pyrogram import Client, filters

# Aapka Bot Token aur API credentials yahan auto-detect honge
API_ID = int(os.environ.get("API_ID", "29235073")) # Default test ID hai, aap badal sakte hain
API_HASH = os.environ.get("API_HASH", "b7cb1370dfda0134dbfcd969cc72b640")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("video_share_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Mujhe koi bhi video bhejiye, main aapko uski File ID nikal kar dunga jise aap share kar sakte hain.")

@app.on_message(filters.video)
async def get_video_id(client, message):
    video_file_id = message.video.file_id
    await message.reply_text(f"✅ Aapki video ki File ID ye hai:\n\n`{video_file_id}`")

app.run()
