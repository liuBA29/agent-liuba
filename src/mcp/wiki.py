# wiki.py
import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

# Загружаем переменные окружения один раз
load_dotenv()

def get_wiki_summary(query: str) -> str:
    """
    Получает краткое описание статьи из русской Википедии.
    Возвращает 2–3 предложения или сообщение об ошибке.
    Использует WIKI_USER_AGENT из .env (если указан).
    """
    try:
        query = query.strip()
        if not query:
            return "[ВИКИ] Укажи тему для поиска, например: /wiki Минск"

        # Кодируем запрос для URL, поддерживая кириллицу
        query_encoded = quote(query.replace(" ", "_"), safe='')

        url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{query_encoded}"

        # Используем кастомный User-Agent, чтобы API не блокировало
        user_agent = os.getenv(
            "WIKI_USER_AGENT",
            "PomoshnikLiubyBot/1.0 (https://github.com/liuBA29; contact: liuba@example.com)"
        )

        headers = {
            "User-Agent": user_agent,
            "Accept": "application/json"
        }

        resp = requests.get(url, headers=headers, timeout=10)

        # Отдельная обработка часто встречающихся ошибок
        if resp.status_code == 404:
            return f"[ВИКИ] Статья '{query}' не найдена."
        if resp.status_code == 403:
            return "[ВИКИ] Доступ запрещён (403). Проверь User-Agent в .env"
        if resp.status_code >= 500:
            return "[ВИКИ] Проблема на стороне Википедии. Попробуй позже."
        if resp.status_code != 200:
            return f"[ВИКИ] Ошибка {resp.status_code}: {resp.text[:200]}"

        data = resp.json()
        title = data.get("title", query)
        extract = data.get("extract")

        if not extract:
            return f"[ВИКИ] Не удалось получить описание для '{title}'."

        # Обрезаем длинные тексты, но без резкого обрыва
        if len(extract) > 600:
            extract = extract[:600].rsplit('.', 1)[0] + "..."

        return f"[ВИКИ] {title}:\n{extract}"

    except requests.exceptions.Timeout:
        return "[ВИКИ] Превышено время ожидания ответа."
    except requests.exceptions.RequestException as e:
        return f"[ВИКИ] Ошибка сети: {e}"
    except Exception as e:
        return f"[ОШИБКА ВИКИ] {type(e).__name__}: {e}"
