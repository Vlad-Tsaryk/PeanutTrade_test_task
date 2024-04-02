import asyncio
from config.config import settings
from config.db import create_tables
from orderbook_service.services import fetch_orderbook


async def main():
    # Отримання даних для кожної пари в асинхронному режимі
    await create_tables()
    tasks = [fetch_orderbook(symbol) for symbol in settings.SYMBOLS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
