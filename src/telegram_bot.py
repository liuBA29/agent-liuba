from memory import append_message, get_context
import os
import signal
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__)))

from mcp.weather import get_weather
from mcp.wiki import get_wiki_summary
from mcp.github import search_github

# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не найден. Создайте .env с TELEGRAM_TOKEN")

# Глобальная переменная для приложения
app = None

def signal_handler(signum, frame):
    """Обработчик сигнала для корректной остановки бота"""
    print("\nПолучен сигнал остановки. Завершаем работу...")
    if app:
        app.stop()
    sys.exit(0)

# Регистрируем обработчик сигнала
signal.signal(signal.SIGINT, signal_handler)

# ------------------ Команды ------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я Помощник Любы 😊\n\n"
        "Команды:\n"
        "/help - показать это сообщение\n"
        "/health - показать статус агента\n"
        "/weather <город> - узнать погоду\n"
        "/wiki <тема> - найти информацию в Википедии\n"
        "/github <запрос> - поиск репозиториев на GitHub\n\n"
        "Просто напиши что-нибудь — и я отвечу 🌸"
    )
    if update.message:
        await update.message.reply_text(text)

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка состояния интеграций"""
    if not update.message:
        return
    user_id = update.message.from_user.id
    context_messages = get_context(user_id)
    status = {
        "telegram": "ok",
        "mcp1": "connected",
        "vector_db": "not_initialized",
        "memory": f"{len(context_messages)} сообщений сохранено",
    }
    pretty = "\n".join(f"{k}: {v}" for k, v in status.items())
    await update.message.reply_text(f"Health status:\n{pretty}")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /weather"""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши название города, например: /weather Минск")
        return

    city = " ".join(context.args)
    report = get_weather(city)

    user_id = update.message.from_user.id
    append_message(user_id, "user", f"/weather {city}")
    append_message(user_id, "bot", report)

    await update.message.reply_text(report)

async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /wiki"""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши тему, например: /wiki Минск")
        return

    query = " ".join(context.args)
    result = get_wiki_summary(query)

    user_id = update.message.from_user.id
    append_message(user_id, "user", f"/wiki {query}")
    append_message(user_id, "bot", result)

    await update.message.reply_text(result)

async def github_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /github"""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши запрос, например: /github telegram bot")
        return

    query = " ".join(context.args)
    result = search_github(query)

    user_id = update.message.from_user.id
    append_message(user_id, "user", f"/github {query}")
    append_message(user_id, "bot", result)

    await update.message.reply_text(result)

# ------------------ Универсальный чат ------------------

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает обычные сообщения пользователя и хранит контекст"""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_id = update.message.from_user.id

    append_message(user_id, "user", user_text)

    context_messages = get_context(user_id)
    context_text = "\n".join([f"{m['role']}: {m['text']}" for m in context_messages])
    reply = f"Ты сказала: {user_text}\n\n🧠 Контекст:\n{context_text}"

    append_message(user_id, "bot", reply)
    await update.message.reply_text(reply)

# ------------------ Запуск бота ------------------

def run_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("health", health_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("github", github_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    print("Бот запускается. Нажмите Ctrl+C для остановки.")

    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
    finally:
        if app:
            app.stop()
