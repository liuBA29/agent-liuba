Agent Liuba

Лёгкий Telegram-бот с базовыми командами и примером интеграции внешних сервисов через бесплатные API.
Точка входа — src/main.py, бот реализован в src/telegram_bot.py, модули — в src/mcp/.

Возможности

/help: краткая справка

/health: базовый статус сервисов

/weather <город>: текущая температура по данным Open-Meteo (пример: /weather Минск)

/wiki <тема>: поиск информации в Википедии (пример: /wiki Минск)

/github <запрос>: поиск репозиториев на GitHub (пример: /github telegram bot)

/search <запрос>: семантический поиск по локальной базе знаний (пример: /search кто создал python)

/chat <текст>: свободный диалог с ИИ (OpenRouter)

/context 10: показать последние 10 сообщений диалога

/forget: очистить историю текущего пользователя

MCP-интеграции (3 бесплатных инструмента)

Проект демонстрирует подключение внешних MCP-модулей (Micro-Capability Providers) и локальной базы знаний:

MCP-модуль	Описание	API
Weather	Получение текущей температуры и координат по городу	Open-Meteo API

Wikipedia	Краткие описания и справка по темам	Wikipedia REST API

GitHub	Поиск публичных репозиториев по ключевым словам	GitHub REST API v3

Knowledge Base	Семантический поиск по локальной базе фактов	ChromaDB + SentenceTransformers
Chat (/chat)	Свободный диалог с моделью	OpenRouter API
Требования

Python 3.10+

Аккаунт и токен Telegram-бота (через BotFather)

Установка
git clone <repo-url>
cd agent-liuba
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt

Переменные окружения

Создайте файл .env в корне проекта и добавьте:

TELEGRAM_TOKEN=<ваш_telegram_bot_token>
WIKI_USER_AGENT=<ваш_user_agent_для_wikipedia_api>
OPENROUTER_API_KEY=<ваш_openrouter_api_key>
OPENROUTER_MODEL=openrouter/auto

Запуск
# Запуск основного приложения
python src/main.py

# Или запуск напрямую Telegram-бота
python src/telegram_bot.py


После запуска бот сообщает в консоль, что начал работу.
Остановить — Ctrl+C.

Команды бота

/help — показать справку

/health — отладочный статус интеграций

/weather <город> — текущая температура

/wiki <тема> — краткая справка из Википедии

/github <запрос> — поиск репозиториев GitHub

/search <запрос> — поиск по локальной базе знаний

/context 10 — показать недавний контекст диалога

/forget — забыть историю пользователя

Как это работает (кратко)

src/telegram_bot.py — инициализирует python-telegram-bot (v20+), регистрирует команды и запускает polling.

src/mcp/weather.py — получает координаты города и температуру через Open-Meteo.

src/mcp/wiki.py — делает безопасный REST-запрос к Wikipedia API.

src/mcp/github.py — выполняет поиск публичных репозиториев на GitHub по ключевым словам.
src/knowledge_base.py — модуль базы знаний: добавление фактов и семантический поиск (ChromaDB + SentenceTransformers).
Память диалога хранится в файле memory.json; доступны команды /context и /forget.

src/main.py — точка входа, вызывает run_bot().

Отладка и типичные проблемы

TELEGRAM_TOKEN не найден — проверьте .env.

/weather возвращает ошибку — проверьте интернет и название города.

/wiki выдаёт 403 — добавьте корректный WIKI_USER_AGENT.

/github пустой ответ — убедитесь, что запрос содержит хотя бы одно ключевое слово.

На Windows PowerShell при активации окружения: . .venv/Scripts/Activate.ps1 (возможна настройка ExecutionPolicy).

Зависимости (основные)

python-telegram-bot>=20.0

python-dotenv

requests
chromadb
sentence-transformers

Docker
# Сборка
docker build -t agent-liuba .

# Запуск
docker run --rm --name agent-liuba-bot --env-file .env agent-liuba

Docker Compose
# Старт (в фоне)
docker compose up -d

# Логи
docker compose logs -f

# Остановка
docker compose down

Лицензия

Добавьте при необходимости файл LICENSE и укажите тип лицензии.

Пример .env

Создайте файл `.env` в корне проекта (можно скопировать из примера):

```bash
cp .env.example .env
```

Содержимое `.env.example`:

```env
TELEGRAM_TOKEN=
WIKI_USER_AGENT=PomoshnikLiubyBot/1.0 (docs-example)
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/auto
# Optional: adjust logging, timeouts, etc.
# LOG_LEVEL=INFO
```

Скриншоты

Положите изображения скриншотов переписки в каталог `screenshots/` в корне проекта. Каталог можно создать вручную, файлы попадут в репозиторий, если в нём есть хотя бы один файл (например, `.gitkeep`).

Скриншоты

Создайте каталог `screenshots/` и складывайте туда снимки диалогов с ботом. В репозитории можно держать пустую директорию с помощью файла-плейсхолдера `.gitkeep`.

Пример `.env`

Создайте файл `.env` по образцу ниже (или используйте `.env.example`, если он есть):

```
TELEGRAM_TOKEN=...
WIKI_USER_AGENT=YourAppName/1.0 (contact@example.com)
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openrouter/auto
```