Agent Liuba

Лёгкий Telegram-бот с базовыми командами и примером интеграции внешних сервисов через бесплатные API.
Точка входа — src/main.py, бот реализован в src/telegram_bot.py, модули — в src/mcp/.

Возможности

/help: краткая справка

/health: базовый статус сервисов

/weather <город>: текущая температура по данным Open-Meteo (пример: /weather Минск)

/wiki <тема>: поиск информации в Википедии (пример: /wiki Минск)

/github <запрос>: поиск репозиториев на GitHub (пример: /github telegram bot)

MCP-интеграции (3 бесплатных инструмента)

Проект демонстрирует подключение внешних MCP-модулей (Micro-Capability Providers):

MCP-модуль	Описание	API
Weather	Получение текущей температуры и координат по городу	Open-Meteo API

Wikipedia	Краткие описания и справка по темам	Wikipedia REST API

GitHub	Поиск публичных репозиториев по ключевым словам	GitHub REST API v3
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

Как это работает (кратко)

src/telegram_bot.py — инициализирует python-telegram-bot (v20+), регистрирует команды и запускает polling.

src/mcp/weather.py — получает координаты города и температуру через Open-Meteo.

src/mcp/wiki.py — делает безопасный REST-запрос к Wikipedia API.

src/mcp/github.py — выполняет поиск публичных репозиториев на GitHub по ключевым словам.

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

(на будущее) chromadb, sentence-transformers

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