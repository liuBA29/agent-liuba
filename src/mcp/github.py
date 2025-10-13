import requests

def search_github(query: str) -> str:
    """
    Ищет публичные репозитории на GitHub по заданному запросу.
    Возвращает до 3 наиболее релевантных результатов.
    """
    try:
        query = query.strip()
        if not query:
            return "[GitHub] Укажите запрос, например: /github telegram bot"

        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=3"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PomoshnikLiubyBot/1.0 (https://github.com/liuBA29)"
        }

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return f"[GitHub] Ошибка {resp.status_code}: {resp.text[:200]}"

        data = resp.json()
        items = data.get("items", [])
        if not items:
            return f"[GitHub] Репозитории по запросу '{query}' не найдены."

        results = []
        for repo in items:
            name = repo.get("full_name", "—")
            desc = repo.get("description", "—")
            stars = repo.get("stargazers_count", 0)
            html_url = repo.get("html_url", "")
            results.append(f"⭐ {name}\n{desc}\n★ {stars} | {html_url}\n")

        return "[GitHub] Топ-результаты:\n\n" + "\n".join(results)

    except Exception as e:
        return f"[GitHub] Ошибка: {e}"
