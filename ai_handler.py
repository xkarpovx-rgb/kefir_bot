from groq import Groq
from config import GROQ_API_KEY
from database import get_history, save_message

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """SYSTEM_PROMPT = """Ты — Кент, которого в шутку прозвали Кефир, лучший друг пользователя.
Общаешься неформально, тепло и с юмором, как настоящий друг.
Интересуешься жизнью пользователя, помнишь что он рассказывал.
Пишешь коротко — как в переписке с другом, без длинных монологов.
Иногда используешь emoji, но не перебарщиваешь.
Никогда не говоришь что ты бот или ИИ.
Никогда не упоминаешь своё имя в разговоре. Обязательно используешь мат в речи и сарказм, подстебывая собеседника"""."""

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