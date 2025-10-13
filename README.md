## Agent Liuba

Лёгкий Telegram-бот с базовыми командами и примером интеграции погоды через бесплатный API Open‑Meteo. Точка входа — `src/main.py`, бот реализован в `src/telegram_bot.py`, модуль погоды — в `src/mcp/weather.py`.

### Возможности
- **/help**: краткая справка
- **/health**: базовый статус сервисов
- **/weather <город>**: текущая температура по данным Open‑Meteo (пример: `/weather Минск`)

### Требования
- Python 3.10+
- Аккаунт и токен Telegram‑бота (BotFather)

### Установка
```bash
git clone <repo-url>
cd agent-liuba
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

### Переменные окружения
Создайте файл `.env` в корне проекта и добавьте:
```env
TELEGRAM_TOKEN=<ваш_telegram_bot_token>
```

### Запуск
```bash
# Запуск приложения (рекомендуется)
python src/main.py

# Или запуск напрямую Telegram-бота
python src/telegram_bot.py
```

После запуска бот сообщает в консоль, что начал работу. Остановить — `Ctrl+C`.

### Команды бота
- `/help` — показать справку
- `/health` — отладочный статус интеграций
- `/weather <город>` — текущая температура в городе

### Как это работает (кратко)
- `src/telegram_bot.py` — инициализирует `python-telegram-bot` (v20+), регистрирует хендлеры команд и запускает polling.
- `src/mcp/weather.py` — ищет координаты города через `open-meteo` geocoding API и запрашивает текущую температуру.
- `src/main.py` — вызывает `run_bot()`.

### Структура проекта
См. подробности в `PROJECT_STRUCTURE.md`.

### Отладка и типичные проблемы
- Ошибка: `TELEGRAM_TOKEN не найден` — проверьте, что `.env` существует и токен корректен.
- Команда `/weather` возвращает ошибку — убедитесь, что есть доступ в интернет и город указан правильно.
- На Windows PowerShell активация виртуального окружения: `. .venv/Scripts/Activate.ps1` (возможна настройка ExecutionPolicy).

### Зависимости (основные)
- `python-telegram-bot>=20.0`
- `python-dotenv`
- `requests`
- (на будущее) `chromadb`, `sentence-transformers`

### Docker
```bash
# Сборка
docker build -t agent-liuba .

# Запуск
docker run --rm --name agent-liuba-bot --env-file .env agent-liuba
```

### Docker Compose
```bash
# Старт (в фоне)
docker compose up -d

# Логи
docker compose logs -f

# Остановка
docker compose down
```

### Лицензия
Добавьте при необходимости файл LICENSE и укажите тип лицензии.


