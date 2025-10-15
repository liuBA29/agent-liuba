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
├── conversations/                # Папка для сохранения диалогов (если используется)
├── data/                         # Данные и файлы базы знаний
├── src/                          # Исходный код
│   ├── knowledge_base.py         # Локальная база знаний (ChromaDB + SentenceTransformers)
│   ├── main.py                   # Главный файл запуска
│   ├── telegram_bot.py           # Бот: /help, /health, /weather, /wiki, /github, /search, /context, /forget
│   └── mcp/                      # Интеграции (MCP-like утилиты)
│       ├── weather.py            # Погода через Open‑Метео (геокодинг + температура)
│       ├── wiki.py               # Краткие описания из Wikipedia REST API
│       └── github.py             # Поиск публичных репозиториев GitHub
└── PROJECT_STRUCTURE.md          # Этот файл со структурой проекта
```

## Описание файлов и папок

### Основные файлы
- `main.py` — точка входа в приложение, запускает Telegram‑бота
- `telegram_bot.py` — реализация Telegram‑бота с командами `/help`, `/health`, `/weather`, `/wiki`, `/github`, `/search`, `/context`, `/forget`
- `knowledge_base.py` — локальная база знаний (добавление фактов и семантический поиск)
- `mcp/weather.py` — модуль погоды: геокодирование города и запрос текущей температуры через Open‑Метео
- `mcp/wiki.py` — модуль Википедии: поиск краткого описания статей через Wikipedia REST API
- `mcp/github.py` — поиск публичных репозиториев GitHub
- `.env` — файл с переменными окружения (`TELEGRAM_TOKEN`, `WIKI_USER_AGENT`)
- `requirements.txt` — список зависимостей проекта
- `README.md` — установка, настройка, запуск, команды и краткая справка

### Папки данных
- `conversations/` — для сохранения истории диалогов (если используется)
- `data/` — для хранения данных, векторной базы знаний, файлов
- `src/mcp/` — утилиты/интеграции (`weather.py`, `wiki.py`, `github.py`)

### Системные файлы
- `.git/` — Git репозиторий
- `.idea/` — настройки IDE PyCharm
- `.venv/` — виртуальное окружение Python

## Зависимости
- `python-telegram-bot>=20.0` — работа с Telegram API
- `python-dotenv` — загрузка переменных окружения из `.env`
- `requests` — HTTP‑запросы
- `chromadb` — векторная база
- `sentence-transformers` — эмбеддинги для поиска

## Команды для запуска
```bash
# Запуск основного приложения
python src/main.py

# Память диалога сохраняется в файле memory.json. Команды: /context, /forget

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
