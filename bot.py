import asyncio
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

def download_video(url):
    ydl_opts = {
        'format': 'mp4/best[height<=720]',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salam! Mənə Instagram, TikTok, YouTube linki at, videonu göndərim.")

@dp.message()
async def handle_link(message: types.Message):
    url = message.text
    if not url.startswith("http"):
        return await message.answer("Link at qardaş 😅")
    
    msg = await message.answer("Yüklənir... ⏳")
    
    try:
        file_path = download_video(url)
        if os.path.getsize(file_path) > 49 * 1024:
            await msg.edit_text("Video 50MB-dan böyükdür, Telegram göndərə bilmir 😔")
        else:
            await bot.send_video(message.chat.id, types.FSInputFile(file_path))
            await msg.delete()
        os.remove(file_path)
    except Exception as e:
        await msg.edit_text("Xəta baş verdi. Link private ola bilər ya da dəstəklənmir.")

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    asyncio.run(dp.start_polling(bot))
