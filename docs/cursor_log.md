Хронология (примерная)

1) Инициализация проекта и среды
   - Создан репозиторий и структура `src/`, `data/`, `conversations/`.
   - Настроено виртуальное окружение, установлены зависимости из `requirements.txt`.

2) Базовый Telegram-бот
   - Добавлен `src/telegram_bot.py` на базе python-telegram-bot v20+.
   - Реализованы команды: `/help`, `/health`, `/weather`, `/wiki`, `/github`, `/search`, `/chat`, `/context`, `/forget`.
   - Точка входа: `src/main.py` с вызовом `run_bot()`.

3) Интеграции (MCP/внешние сервисы)
   - `src/mcp/weather.py` — Open-Meteo API.
   - `src/mcp/wiki.py` — Wikipedia REST API (с `WIKI_USER_AGENT`).
   - `src/mcp/github.py` — GitHub REST API v3.
   - `src/knowledge_base.py` — локальная БЗ (ChromaDB + SentenceTransformers).

4) Память и контекст диалога
   - Хранение истории в `data/memory.json`.
   - Команда `/context [N]` для показа последних сообщений (дефолт 10, предел 1–50).

5) Докеризация
   - Добавлены `Dockerfile` и `docker-compose.yml`.
   - Запуск: `docker build -t agent-liuba .` и `docker run --rm --env-file .env agent-liuba`.
   - В compose проброшены тома для `data/`, `conversations/` и кэша моделей.

6) Документация
   - Обновлён `README.md` с инструкциями по установке, запуску и командам.
   - Уточнены формулировки про `/context 10` (вместо [N]).

7) Конфигурация окружения
   - Добавлен пример `.env.example` (ключи: `TELEGRAM_TOKEN`, `WIKI_USER_AGENT`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`).

8) Дополнительно
   - Создан каталог `docs/`.
   - В `docs/chat_screens/` хранить скриншоты переписки (есть `.gitkeep`).
   - Этот файл (`docs/cursor_log.md`) зафиксировал ключевые шаги.

Примечание: порядок шагов отражён обобщённо; отдельные правки и мелкие изменения могли выполняться между пунктами.

