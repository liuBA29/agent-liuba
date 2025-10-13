import json
import os
from datetime import datetime

MEMORY_FILE = "conversations/memory.json"

# Убедимся, что папка существует
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

def load_memory():
    """Загружает историю диалогов"""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_memory(memory):
    """Сохраняет историю"""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def append_message(user_id, role, text):
    """Добавляет сообщение в историю пользователя"""
    memory = load_memory()
    history = memory.get(str(user_id), [])
    history.append({
        "role": role,
        "text": text,
        "time": datetime.now().isoformat(timespec="seconds")
    })
    memory[str(user_id)] = history[-50:]  # храним только последние 50 сообщений
    save_memory(memory)

def get_context(user_id):
    """Возвращает историю сообщений (для текущего диалога)"""
    memory = load_memory()
    return memory.get(str(user_id), [])
