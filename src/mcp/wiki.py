import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def get_wiki_summary(query: str) -> str:
    """
    Получает краткое описание по запросу через Wikipedia API.
    Возвращает первые 2–3 предложения статьи.
    Использует WIKI_USER_AGENT из переменных окружения.
    """
    try:
        # Правильно кодируем URL для кириллических символов
        query_encoded = quote(query.strip().replace(" ", "_"), safe='')
        # Используем старый, но рабочий Wikipedia API:
        url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{query_encoded}"

        # Получаем User-Agent из переменных окружения или используем значение по умолчанию
        user_agent = os.getenv("WIKI_USER_AGENT", "PomoshnikLiubyBot/1.0 (https://github.com/liuBA29; contact: liuba@example.com)")
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "application/json"
        }

        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code == 404:
            return f"[ВИКИ] Статья '{query}' не найдена."
        elif resp.status_code == 403:
            return f"[ВИКИ] Доступ запрещён (403). Возможно, блокировка по IP или неправильный User-Agent."
        elif resp.status_code != 200:
            return f"[ВИКИ] Ошибка {resp.status_code}: {resp.text[:200]}"

        data = resp.json()
        title = data.get("title", query)
        extract = data.get("extract")

        if not extract:
            return f"[ВИКИ] Не удалось получить описание для '{title}'."

        if len(extract) > 600:
            extract = extract[:600] + "..."

        return f"[ВИКИ] {title}:\n{extract}"

    except Exception as e:
        return f"[ОШИБКА ВИКИ] {e}"
