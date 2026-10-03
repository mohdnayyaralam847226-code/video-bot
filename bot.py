import os
import asyncio
from pyrogram import Client, filters

# Event loop error fix karne ke liye naya tarika
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

API_ID = int(os.environ.get("API_ID", "29235073")) 
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

# Bot ko chalane ka sahi tarika naye python ke liye
loop.run_until_complete(app.run())
