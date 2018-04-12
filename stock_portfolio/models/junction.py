from sqlalchemy import (
    Index,
    Column,
    Integer,
    String,
    ForeignKey,
)
# from sqlalchemy.orm import relationship

from .meta import Base


class Junction(Base):
    __tablename__ = 'user_portfolios'
    id = Column(Integer, primary_key=True)
    stock_id = Column(String, ForeignKey('stocks.symbol'), nullable=False)
    account_id = Column(String, ForeignKey('accounts.username'), nullable=False)
