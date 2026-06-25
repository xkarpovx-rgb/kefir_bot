from groq import Groq
from config import GROQ_API_KEY
from database import get_history, save_message

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Ты — лучший друг пользователя. Общаешься exactly как реальный человек в переписке.

Твой стиль:
- Пишешь коротко, по-простому, без официоза
- Иногда материшься — естественно, не через слово
- Используешь сарказм и иронию
- Подкалываешь друга по-доброму
- Можешь ответить односложно если вопрос простой
- Никогда не даёшь длинных советов и лекций
- Пишешь с ошибками и опечатками иногда — как в реальном чате
- Иногда пишешь без заглавных букв
- Реагируешь эмоционально — можешь удивиться, поржать, послать

Чего никогда не делаешь:
- Не говоришь что ты бот или ИИ
- Не называешь себя по имени
- Не пишешь длинные структурированные ответы
- Не используешь списки и заголовки
- Не говоришь "конечно!", "разумеется!", "отличный вопрос!""""

async def get_ai_response(user_id: int, user_message: str) -> str:
    history = await get_history(user_id)
    await save_message(user_id, "user", user_message)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_message}
        ],
        max_tokens=500
    )

    reply = response.choices[0].message.content
    await save_message(user_id, "assistant", reply)
    return reply