"""
Shared bot instance reference used across the application.
Avoids circular imports by providing a getter pattern.
"""
from typing import Optional
from aiogram import Bot

_bot_instance: Optional[Bot] = None


def set_bot(bot: Bot) -> None:
    global _bot_instance
    _bot_instance = bot


def get_bot() -> Optional[Bot]:
    return _bot_instance
