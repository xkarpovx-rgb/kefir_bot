import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from database import init_db, save_user
from ai_handler import get_ai_response
from scheduler import setup_scheduler
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await save_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        f"О, {message.from_user.first_name}! Кефир на связи 🥛 Рад познакомиться!"
    )

@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
    await save_user(message.from_user.id, message.from_user.first_name)
    reply = await get_ai_response(message.from_user.id, message.text)
    await message.answer(reply)

async def main():
    await init_db()
    scheduler = setup_scheduler(bot)
    scheduler.start()
    print("Кефир запущен! 🥛")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())