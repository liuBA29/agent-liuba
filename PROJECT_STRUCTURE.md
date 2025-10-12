# Структура проекта Agent Liuba

```
agent-liuba/
├── .env                          # Переменные окружения (токен бота)
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
├── conversations/                # Папка для сохранения диалогов
├── data/                         # Данные и файлы базы знаний
├── src/                          # Исходный код
│   ├── main.py                   # Главный файл запуска
│   ├── telegram_bot.py           # Telegram бот (частично реализован)
│   └── mcp/                      # MCP (Model Context Protocol) серверы
└── PROJECT_STRUCTURE.md          # Этот файл со структурой проекта
```

## Описание файлов и папок

### Основные файлы
- **`main.py`** - точка входа в приложение, запускает Telegram бота
- **`telegram_bot.py`** - реализация Telegram бота с командами /help и /health
- **`.env`** - файл с переменными окружения (токен Telegram бота)

### Папки данных
- **`conversations/`** - для сохранения истории диалогов с пользователями
- **`data/`** - для хранения данных, векторной базы знаний, файлов
- **`src/mcp/`** - для MCP серверов (пока пустая)

### Системные файлы
- **`.git/`** - Git репозиторий
- **`.idea/`** - настройки IDE PyCharm
- **`.venv/`** - виртуальное окружение Python

## Текущий статус

✅ **Установлены зависимости:**
- `python-dotenv` - для работы с .env файлами
- `python-telegram-bot` - для Telegram API

✅ **Создан .env файл** с токеном бота

⚠️ **В разработке:**
- Telegram бот (базовая структура готова)
- MCP интеграции
- Векторная база данных
- Система сохранения диалогов

## Команды для запуска

```bash
# Запуск основного приложения
python src/main.py

# Запуск только Telegram бота
python src/telegram_bot.py
```
