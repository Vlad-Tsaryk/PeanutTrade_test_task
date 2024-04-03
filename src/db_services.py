from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import OrderBookSchema
from models import OrderBookData
from config.decorators import add_session


@add_session
async def create_orderbook(orderbook: OrderBookSchema, session: AsyncSession):
    orderbook_data: dict[str, Any] = orderbook.dict()
    new_orderbook: OrderBookData = OrderBookData(**orderbook_data)
    session.add(new_orderbook)
    await session.commit()


@add_session
async def calculate_average_volumes(symbol: str, session: AsyncSession):
    one_hour_ago = datetime.utcnow() - timedelta(days=1)

    avg_query = select(
        func.avg(OrderBookData.buy_volume).label("avg_buy_volume"),
        func.avg(OrderBookData.sell_volume).label("avg_sell_volume"),
    ).where(
        and_(OrderBookData.symbol == symbol, OrderBookData.timestamp >= one_hour_ago)
    )

    result = await session.execute(avg_query)

    average_volumes = result.first()
    return average_volumes.avg_buy_volume, average_volumes.avg_sell_volume
