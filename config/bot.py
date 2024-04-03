from aiogram import Bot
from aiogram.enums import ParseMode

from .config import settings

bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
