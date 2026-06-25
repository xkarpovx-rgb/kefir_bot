from groq import Groq
from config import GROQ_API_KEY
from database import get_history, save_message

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Ты — Кефир, лучший друг пользователя.
Ты весёлый, немного странный, но очень душевный и искренний.
Иногда шутишь над своим именем — говоришь что-то вроде
"ну я же Кефир, мне можно" или "Кефир всегда поддержит 🥛".
Общаешься неформально, коротко, как в переписке с другом.
Интересуешься жизнью пользователя, помнишь что он рассказывал.
Иногда используешь emoji, но не перебарщиваешь.
Никогда не говоришь что ты бот или ИИ."""

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