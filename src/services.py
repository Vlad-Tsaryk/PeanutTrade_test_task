from datetime import datetime

import websockets
import json
import pandas as pd

from config.bot import bot
from config.config import settings
from config.prometheus_collectors import (
    SEND_MESSAGE_TIME,
    PROCESS_ORDERBOOK_TIME,
    CALCULATE_DEVIATION_TIME,
)
from schemas import OrderBookSchema
from db_services import create_orderbook, calculate_average_volumes
from loguru import logger


async def fetch_orderbook(symbol):
    url = f"wss://stream.binance.com:9443/ws/{symbol}@depth20@100ms"
    async with websockets.connect(url) as websocket:
        async for message in websocket:
            data = json.loads(message)
            try:
                await process_orderbook(data, symbol)
            except Exception as e:
                logger.error(f"Failed to process orderbook for {symbol}: {e}")


async def send_telegram_message(message_text: str) -> None:
    await bot.send_message(settings.CHAT_ID, message_text)


async def calculate_deviation(symbol, mid_price, buy_volume, sell_volume) -> None:
    with CALCULATE_DEVIATION_TIME.time():
        average_buy_volume, average_sell_volume = await calculate_average_volumes(
            symbol
        )
        if average_buy_volume and average_sell_volume:
            buy_volume_deviation = (
                    abs(buy_volume - average_buy_volume) / average_buy_volume
            )
            sell_volume_deviation = (
                    abs(sell_volume - average_sell_volume) / average_sell_volume
            )

        if buy_volume_deviation > settings.DEVIATION_THRESHOLD:
            await send_telegram_message(
                f"Відхилення за обсягом для <b>{symbol}</b>:\n"
                f"Середня ціна - {mid_price};\n"
                f"Купівля - {buy_volume} (Середнє - {average_buy_volume})"
            )

        if sell_volume_deviation > settings.DEVIATION_THRESHOLD:
            await send_telegram_message(
                f"Відхилення за обсягом для <b>{symbol}</b>:\nСередня ціна - {mid_price};\n"
                f"Продаж - {sell_volume} (Середнє - {average_sell_volume})"
            )


async def process_orderbook(data, symbol):
    with PROCESS_ORDERBOOK_TIME.time():
        bids = pd.DataFrame(data["bids"], columns=["price", "quantity"], dtype=float)
        asks = pd.DataFrame(data["asks"], columns=["price", "quantity"], dtype=float)

        best_bid = bids["price"].max()
        best_ask = asks["price"].min()
        mid_price = (best_bid + best_ask) / 2

        upper_bound = mid_price * 1.02
        lower_bound = mid_price * 0.98

        buy_volume = bids[bids["price"] >= lower_bound]["quantity"].sum()
        sell_volume = asks[asks["price"] <= upper_bound]["quantity"].sum()

    await calculate_deviation(symbol, mid_price, buy_volume, sell_volume)

    orderbook_schema = OrderBookSchema(
        symbol=symbol,
        timestamp=datetime.utcnow(),
        mid_price=mid_price,
        buy_volume=buy_volume,
        sell_volume=sell_volume,
    )
    await create_orderbook(orderbook_schema)
    # logger.info(
    #     f"{symbol} - Mid Price: {mid_price}, Buy Volume (-2%): {buy_volume}, Sell Volume (+2%): {sell_volume}"
    # )
