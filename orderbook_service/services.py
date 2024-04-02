from datetime import datetime

import websockets
import json
import pandas as pd

from config.config import settings
from orderbook_service.schemas import OrderBookSchema
from db_services import create_orderbook
from .db_services import calculate_average_volumes
from loguru import logger


async def fetch_orderbook(symbol):
    url = f"wss://stream.binance.com:9443/ws/{symbol}@depth20@100ms"
    async with websockets.connect(url) as websocket:
        async for message in websocket:
            data = json.loads(message)
            await process_orderbook(data, symbol)


async def process_orderbook(data, symbol):
    bids = pd.DataFrame(data["bids"], columns=["price", "quantity"], dtype=float)
    asks = pd.DataFrame(data["asks"], columns=["price", "quantity"], dtype=float)

    # Розрахунок середньої ціни
    best_bid = bids["price"].max()
    best_ask = asks["price"].min()
    mid_price = (best_bid + best_ask) / 2

    # Визначення цінових діапазонів
    upper_bound = mid_price * 1.02
    lower_bound = mid_price * 0.98

    # Розрахунок обсягів
    buy_volume = bids[bids["price"] >= lower_bound]["quantity"].sum()
    sell_volume = asks[asks["price"] <= upper_bound]["quantity"].sum()

    # await calculate_average_volumes(symbol)
    # average_buy_volume, average_sell_volume = await calculate_average_volumes(symbol)
    #
    # buy_volume_deviation = abs(buy_volume - average_buy_volume) / average_buy_volume
    # sell_volume_deviation = abs(sell_volume - average_sell_volume) / average_sell_volume
    #
    # if buy_volume_deviation > settings.DEVIATION_THRESHOLD:
    #     logger.success(f"Відхилення за обсягом для {symbol}: Середня ціна - {mid_price}, " \
    #                    f"Купівля - {buy_volume} (Середнє - {average_buy_volume}), ")
    #
    # if sell_volume_deviation > settings.DEVIATION_THRESHOLD:
    #     logger.success(f"Відхилення за обсягом для {symbol}: Середня ціна - {mid_price}, " \
    #                    f"Продаж - {sell_volume} (Середнє - {average_sell_volume})")

    orderbook_schema = OrderBookSchema(
        symbol=symbol,
        timestamp=datetime.utcnow(),
        mid_price=mid_price,
        buy_volume=buy_volume,
        sell_volume=sell_volume,
    )
    await create_orderbook(orderbook_schema)
    logger.info(
        f"{symbol} - Mid Price: {mid_price}, Buy Volume (-2%): {buy_volume}, Sell Volume (+2%): {sell_volume}"
    )
