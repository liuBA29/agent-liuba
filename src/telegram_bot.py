# telegram_bot.py

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()  # загружает переменные из .env если он есть
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не найден. Создайте .env с TELEGRAM_TOKEN")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я Pomoshnik Liuby 😊\n\n"
        "Команды:\n"
        "/help - показать это сообщение\n"
        "/health - показать статус агента\n\n"
        "Просто напиши что-нибудь — и я отвечу."
    )
    await update.message.reply_text(text)

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Здесь позже будем проверять интеграции; пока — базовый ответ
    status = {
        "telegram": "ok",
        "mcp1": "not_connected",
        "vector_db": "not_initialized",
    }
    pretty = "\n".join(f"{k}: {v}" for k, v in status.items())
    await update.message.reply_text(f"Health status:\n{pretty}")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("health", health_command))

    print("Бот запускается. Нажмите Ctrl+C для остановки.")
    app.run_polling()
