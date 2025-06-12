from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os

from libs.captcha_solver import solve_captcha

# توكن البوت من متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تأكد إنه موجود
if not BOT_TOKEN:
    raise ValueError("لازم تحط BOT_TOKEN في متغيرات البيئة")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    os.makedirs("temp", exist_ok=True)  # تأكد المجلد موجود

    file_path = f"temp/{photo.file_id}.jpg"
    await photo.download(destination_file=file_path)

    try:
        result = solve_captcha(file_path)
        await message.reply(f"الإجابة: {result}")
    except Exception as e:
        await message.reply(f"حصل خطأ أثناء التحليل: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply("أرسل صورة كابتشا فيها رقم فوق و9 تحت، وأنا هقولك الإجابة ✅")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
