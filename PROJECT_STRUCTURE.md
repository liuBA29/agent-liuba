# Структура проекта Agent Liuba

```
agent-liuba/
├── .env                          # Переменные окружения (токен бота, user-agent для Wikipedia)
├── .git/                         # Git репозиторий
├── .idea/                        # Настройки PyCharm
│   ├── agent-liuba.iml
│   ├── misc.xml
│   ├── modules.xml
│   ├── vcs.xml
│   ├── workspace.xml
│   └── inspectionProfiles/
│       └── profiles_settings.xml
├── .venv/                        # Виртуальное окружение Python
├── Dockerfile                    # Образ приложения (python:3.11-slim)
├── docker-compose.yml            # Сервис бота, монтирование папок и .env
├── README.md                     # Краткая документация: установка, запуск, команды
├── requirements.txt              # Список зависимостей проекта
├── conversations/                # Папка для сохранения диалогов
├── data/                         # Данные и файлы базы знаний
├── src/                          # Исходный код
|   ├── memory.py                   # 
│   ├── main.py                   # Главный файл запуска
│   ├── telegram_bot.py           # Telegram-бот с командами /help, /health, /weather
│   └── mcp/                      # MCP (Model Context Protocol) утилиты/интеграции
│       ├── weather.py            # Получение погоды через Open-Meteo (геокодинг + текущая температура)
│       └── wiki.py               # Поиск информации в Википедии через Wikipedia REST API
└── PROJECT_STRUCTURE.md          # Этот файл со структурой проекта
```

## Описание файлов и папок

### Основные файлы
- **`main.py`** — точка входа в приложение, запускает Telegram‑бота
- **`telegram_bot.py`** — реализация Telegram‑бота с командами `/help`, `/health`, `/weather`, `/wiki`
- **`mcp/weather.py`** — модуль погоды: геокодирование города и запрос текущей температуры через Open‑Meteо
- **`mcp/wiki.py`** — модуль Википедии: поиск краткого описания статей через Wikipedia REST API
- **`.env`** — файл с переменными окружения (`TELEGRAM_TOKEN`, `WIKI_USER_AGENT`)
- **`requirements.txt`** — список зависимостей проекта
- **`README.md`** — установка, настройка, запуск, команды и краткая справка

### Папки данных
- **`conversations/`** - для сохранения истории диалогов с пользователями
- **`data/`** - для хранения данных, векторной базы знаний, файлов
- **`src/mcp/`** - утилиты/интеграции (содержит `weather.py`, `wiki.py`)

### Системные файлы
- **`.git/`** - Git репозиторий
- **`.idea/`** - настройки IDE PyCharm
- **`.venv/`** - виртуальное окружение Python

## Текущий статус

✅ **Основные зависимости установлены:**
- `python-telegram-bot>=20.0` — работа с Telegram API
- `python-dotenv` — загрузка переменных окружения из `.env`
- `requests` — HTTP‑запросы (используется модулем погоды)

ℹ️ **На будущее (пока не используется в коде):**
- `chromadb`, `sentence-transformers` — для векторной БД и эмбеддингов

✅ **Файл `.env`** — требуется переменная `TELEGRAM_TOKEN` и опционально `WIKI_USER_AGENT`

⚠️ **В разработке:**
- Дополнительные MCP‑интеграции
- Векторная база данных и сохранение диалогов

## Команды для запуска

```bash
# Запуск основного приложения
python src/main.py

#добавить инфу про memory.py

# Запуск только Telegram бота
python src/telegram_bot.py
```

## Docker
```bash
# Сборка образа
docker build -t agent-liuba .

# Запуск контейнера с .env
docker run --rm --name agent-liuba-bot --env-file .env agent-liuba
```

## Docker Compose
```bash
# Старт в фоне
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

## Переменные окружения
Создайте файл `.env` в корне и укажите:
```env
TELEGRAM_TOKEN=<ваш_telegram_bot_token>
WIKI_USER_AGENT=<ваш_user_agent_для_wikipedia_api>
```

Подробнее см. `README.md`.
