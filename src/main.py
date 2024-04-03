import asyncio
from config.config import settings
from config.db import create_tables
from services import fetch_orderbook
from prometheus_client import start_http_server


async def main():
    await create_tables()
    tasks = [fetch_orderbook(symbol) for symbol in settings.SYMBOLS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        start_http_server(8000)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
