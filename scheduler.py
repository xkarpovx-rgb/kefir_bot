import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_all_users

PROACTIVE_MESSAGES = [
    "Эй, как дела? Кефир соскучился 🥛",
    "Привет! Что делаешь?",
    "Хей, думал о тебе. Всё норм?",
    "Давно не слышались, как ты вообще? 😄",
    "О чём думаешь? Кефир слушает",
    "Эй, живой? 👋",
]

async def send_proactive_messages(bot):
    users = await get_all_users()
    for user_id, name in users:
        if random.random() < 0.3:
            msg = random.choice(PROACTIVE_MESSAGES)
            try:
                await bot.send_message(user_id, msg)
            except Exception:
                pass

def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_proactive_messages, "interval", hours=48, args=[bot])
    return scheduler