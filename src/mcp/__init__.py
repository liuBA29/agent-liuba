# MCP (Model Context Protocol) модули
# Этот файл делает папку mcp Python пакетом

__version__ = "1.0.0"
__author__ = "Agent Liuba"

# Импорты всех MCP модулей
from .weather import get_weather

__all__ = [
    "get_weather",
]
