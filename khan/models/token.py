from sqlalchemy import Column, Integer, String, DateTime, Float, Time
from sqlalchemy.sql import func
from ..database import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, index=True)
    refresh_token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    
    
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime)
    account_id = Column(String)
    amount_type = Column(String)
    amount = Column(Float)
    transaction_remarks = Column(String)
    txn_time = Column(Time(timezone=False))
    begin_balance = Column(Float)
    end_balance = Column(Float)
    # txn_branch_id = Column(String)

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_date='{self.transaction_date}', account_id='{self.account_id}')>"