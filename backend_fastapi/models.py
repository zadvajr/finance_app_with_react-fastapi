"""Database models"""
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Transactions(Base):
    """Transactions class"""
    __table_name__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    is_income = Column(Boolean)
    date = Column(String)
