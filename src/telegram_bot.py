# telegram_bot.py

import os
import signal
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__)))
from mcp.weather import get_weather
from mcp.wiki import get_wiki_summary


load_dotenv()  # загружает переменные из .env если он есть
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я Помощник Любы 😊\n\n"
        "Команды:\n"
        "/help - показать это сообщение\n"
        "/health - показать статус агента\n"
        "/weather <город> - узнать погоду в городе\n"
        "/wiki <тема> - найти информацию в Википедии\n\n"
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


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши название города, например: /weather Минск")
        return

    city = " ".join(context.args)
    report = get_weather(city)
    await update.message.reply_text(report)


async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск краткого описания в Википедии"""
    if not context.args:
        await update.message.reply_text("Напиши тему, например: /wiki Минск")
        return

    query = " ".join(context.args)
    result = get_wiki_summary(query)
    await update.message.reply_text(result)




def run_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("health", health_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("wiki", wiki_command))

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

