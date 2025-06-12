from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os
from libs.captcha_solver import solve_captcha  # هنكتبه كمان شوية

# التوكن من متغير بيئة (هنحطه في Railway بعدين)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file_path = f"temp/{photo.file_id}.jpg"
    await photo.download(destination_file=file_path)

    result = solve_captcha(file_path)
    await message.reply(f"الإجابة: {result}")

    os.remove(file_path)

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply("أرسل صورة الكابتشا لحلها ✉️")

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    executor.start_polling(dp)
