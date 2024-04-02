from pydantic import BaseModel
from datetime import datetime


class OrderBookSchema(BaseModel):
    symbol: str
    timestamp: datetime
    mid_price: float
    buy_volume: float
    sell_volume: float
