import os
import sys
import signal
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import openai
import requests

# ------------------ Настройка путей ------------------
sys.path.append(os.path.join(os.path.dirname(__file__)))

from mcp.weather import get_weather
from mcp.wiki import get_wiki_summary
from mcp.github import search_github

# ------------------ Загрузка токенов ------------------
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Нужны TELEGRAM_TOKEN и OPENAI_API_KEY в .env")

openai.api_key = OPENAI_API_KEY

# ------------------ Глобальные переменные ------------------
app = None
MEMORY_DIR = "conversations"
os.makedirs(MEMORY_DIR, exist_ok=True)

# ------------------ Обработка сигналов ------------------
def signal_handler(signum, frame):
    print("\nПолучен сигнал остановки. Завершаем работу...")
    if app:
        app.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ------------------ Работа с памятью ------------------
def get_memory_file(user_id):
    """Создаёт уникальный файл для каждой новой сессии"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(MEMORY_DIR, f"{user_id}_{timestamp}.json")

def load_memory(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(file_path, memory):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def append_message(file_path, role, text):
    memory = load_memory(file_path)
    memory.append({
        "role": role,
        "text": text,
        "time": datetime.now().isoformat(timespec="seconds")
    })
    memory = memory[-50:]  # хранить только последние 50 сообщений
    save_memory(file_path, memory)

def get_context(file_path):
    return load_memory(file_path)

# ------------------ Команды ------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
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
    await update.message.reply_text(text)

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    status = {
        "telegram": "ok",
        "mcp1": "connected",
        "vector_db": "not_initialized",
        "memory_dir": MEMORY_DIR,
    }
    pretty = "\n".join(f"{k}: {v}" for k, v in status.items())
    await update.message.reply_text(f"Health status:\n{pretty}")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши название города, например: /weather Минск")
        return

    city = " ".join(context.args)
    report = get_weather(city)

    user_id = update.message.from_user.id
    file_path = get_memory_file(user_id)
    append_message(file_path, "user", f"/weather {city}")
    append_message(file_path, "bot", report)

    await update.message.reply_text(report)

async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши тему, например: /wiki Минск")
        return

    query = " ".join(context.args)
    result = get_wiki_summary(query)

    user_id = update.message.from_user.id
    file_path = get_memory_file(user_id)
    append_message(file_path, "user", f"/wiki {query}")
    append_message(file_path, "bot", result)

    await update.message.reply_text(result)

async def github_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Напиши запрос, например: /github telegram bot")
        return

    query = " ".join(context.args)
    result = search_github(query)

    user_id = update.message.from_user.id
    file_path = get_memory_file(user_id)
    append_message(file_path, "user", f"/github {query}")
    append_message(file_path, "bot", result)

    await update.message.reply_text(result)

# ------------------ Универсальный чат ------------------
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    user_text_lower = user_text.lower()
    user_id = update.message.from_user.id
    file_path = get_memory_file(user_id)

    append_message(file_path, "user", user_text)

    # --- Простые живые ответы ---
    greetings = ["hi", "hello", "привет", "здравствуй", "добрый день"]
    farewells = ["bye", "пока", "до свидания", "увидимся"]

    if user_text_lower in greetings:
        bot_reply = "Привет! 😊 Как настроение сегодня?"
        append_message(file_path, "bot", bot_reply)
        await update.message.reply_text(bot_reply)
        return
    elif user_text_lower in farewells:
        bot_reply = "Пока! 🌸 Будет приятно снова с тобой пообщаться."
        append_message(file_path, "bot", bot_reply)
        await update.message.reply_text(bot_reply)
        return

    # --- Ответ через OpenAI без ссылок ---
    context_messages = get_context(file_path)
    messages = [
        {"role": "system", "content": (
            "Ты дружелюбный помощник Любы. "
            "Отвечай на вопросы только текстом, "
            "никогда не вставляй ссылки на GitHub или любые внешние сайты."
        )},
    ] + [
        {"role": "user", "content": msg["text"]} if msg["role"] == "user" else
        {"role": "assistant", "content": msg["text"]}
        for msg in context_messages
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"Ошибка при обращении к ChatGPT: {e}"

    append_message(file_path, "bot", bot_reply)
    await update.message.reply_text(bot_reply)

# ------------------ Запуск бота ------------------
def run_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("health", health_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("github", github_command))

    # Чат
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

if __name__ == "__main__":
    run_bot()
