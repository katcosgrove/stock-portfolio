from sqlalchemy import (
    Index,
    Column,
    Integer,
    String,
)


from .meta import Base


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    CEO = Column(String)
    exchange = Column(String)
    website = Column(String)
    description = Column(String)
    industry = Column(String)
    sector = Column(String)
    issueType = Column(String)


Index('entry_index', Stock.id, unique=True, mysql_length=255)
