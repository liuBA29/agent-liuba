# telegram_bot.py
import asyncio
import json
import os
import signal
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__)))
from mcp.weather import get_weather
from mcp.wiki import get_wiki_summary
from mcp.github import search_github
from knowledge_base import add_fact, search_fact



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
        "/start — приветствие и список команд\n"
        "/help — показать это сообщение\n"
        "/health — показать статус агента\n"
        "<code>/weather &lt;город&gt;</code> — узнать погоду в городе\n"
        "<code>/wiki &lt;тема&gt;</code> — найти информацию в Википедии\n"
        "/github &lt;запрос&gt; — поиск репозиториев на GitHub\n"
        "<code>/search &lt;запрос&gt;</code> — поиск по базе знаний\n"
        "<code>/remember &lt;факт&gt;</code> — сохранить факт в базу знаний\n"
        "/context [N] — показать последние N сообщений диалога\n"
        "/forget — забыть историю диалога\n\n"
        "Просто напиши что-нибудь — и я отвечу."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Показываем те же доступные команды, что и /help
    await help_command(update, context)

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = {
        "telegram": "ok",
        "github": "ok",
        "weather": "ok",
        "wiki": "ok",
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



async def github_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Асинхронный обработчик GitHub-команды"""
    if not context.args:
        await update.message.reply_text("Напиши запрос, например: /github telegram bot")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🔎 Ищу репозитории на GitHub...")

    # Выполняем блокирующий HTTP-запрос в отдельном потоке, чтобы не блокировать event loop
    result = await asyncio.to_thread(search_github, query)
    await update.message.reply_text(result)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши запрос, например: /search Python asyncio")
        return
    query = " ".join(context.args)
    results = search_fact(query)
    if results:
        text = "🔎 Нашлось в базе:\n" + "\n".join(results)
    else:
        text = "Ничего не нашлось."
    await update.message.reply_text(text)

async def remember_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши факт, например: /remember Python создан Гвидо ван Россумом")
        return
    fact = " ".join(context.args)
    try:
        add_fact(fact)
        await update.message.reply_text("✅ Запомнила: " + fact)
    except Exception as e:
        await update.message.reply_text(f"[KB] Ошибка сохранения: {e}")

# Файл для простой персистентной памяти (внутри тома data/)
MEMORY_FILE = "data/memory.json"
MAX_HISTORY_PER_USER = 200  # мягкий лимит на длину истории одного пользователя

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# Простая память в виде словаря: user_id -> список сообщений (загружаем при старте)
memory = load_memory()

def get_user_history(user_id: str, limit: int | None = None):
    history = memory.get(user_id, [])
    if limit is not None and limit > 0:
        return history[-limit:]
    return history

def append_user_entry(user_id: str, role: str, text: str):
    # Добавляем запись и придерживаемся мягкого лимита истории
    memory.setdefault(user_id, []).append({"role": role, "text": text})
    if len(memory[user_id]) > MAX_HISTORY_PER_USER:
        memory[user_id] = memory[user_id][-MAX_HISTORY_PER_USER:]
    save_memory()

def clear_user_history(user_id: str):
    memory[user_id] = []
    save_memory()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()

    # Добавляем сообщение пользователя в память
    append_user_entry(user_id, "user", text)

    # Примитивные ответы на ключевые фразы
    if "привет" in text.lower():
        reply = "Привет, рада тебя видеть! 😊"
    elif "как дела" in text.lower():
        reply = "У меня всё отлично, работаю как часы 🤖"
    elif "спасибо" in text.lower():
        reply = "Всегда пожалуйста 🌸"
    elif "что ты помнишь" in text.lower():
        past = [m['text'] for m in memory[user_id][-3:]]  # последние 3 сообщения
        reply = "Я помню, что мы недавно говорили о:\n" + "\n".join(past)
    else:
        # Попробуем подсказать из базы знаний
        kb_hits = []
        try:
            kb_hits = search_fact(text) or []
        except Exception:
            kb_hits = []
        if kb_hits:
            top = kb_hits[:3]
            reply = "Я пока не всё понимаю, но вот что нашла в базе:\n" + "\n".join(top)
        else:
            reply = "Я пока не всё понимаю, но стараюсь учиться с каждым сообщением 💫"

    # Сохраняем ответ бота тоже
    append_user_entry(user_id, "bot", reply)

    await update.message.reply_text(reply)

async def context_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать последние N сообщений контекста для текущего пользователя."""
    user_id = str(update.effective_user.id)
    try:
        limit = int(context.args[0]) if context.args else 10
    except Exception:
        limit = 10
    limit = max(1, min(limit, 50))

    history = get_user_history(user_id, limit)
    if not history:
        await update.message.reply_text("Контекст пуст.")
        return

    lines = []
    for entry in history:
        prefix = "user:" if entry.get("role") == "user" else "bot:"
        lines.append(f"{prefix} {entry.get('text','')}")
    await update.message.reply_text("\n".join(lines))

async def forget_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистить историю диалога текущего пользователя."""
    user_id = str(update.effective_user.id)
    clear_user_history(user_id)
    await update.message.reply_text("Я забыла наш предыдущий разговор для этой сессии.")


def run_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("health", health_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("github", github_command))
    app.add_handler(CommandHandler("remember", remember_command))
    app.add_handler(CommandHandler("context", context_command))
    app.add_handler(CommandHandler("forget", forget_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Пример: добавим пару фактов при запуске (можно убрать или заменить)
    try:
        add_fact("Python — это язык программирования, созданный Гвидо ван Россумом.")
        add_fact("Асинхронность в Python реализуется через asyncio и await.")
        add_fact("Telegram Bot API позволяет создавать ботов, которые взаимодействуют с пользователями через команды и сообщения.")
        add_fact("ChromaDB — это векторная база данных для семантического поиска по эмбеддингам.")
    except Exception:
        # Если embedding-модель ещё скачивается или нет доступа в интернет,
        # запуск бота не должен падать
        pass


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

