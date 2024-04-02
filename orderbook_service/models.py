from sqlalchemy import Column, Integer, String, Float, DateTime

from config.db import Base


class OrderBookData(Base):
    __tablename__ = "orderbook_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime)
    mid_price = Column(Float)
    buy_volume = Column(Float)
    sell_volume = Column(Float)
