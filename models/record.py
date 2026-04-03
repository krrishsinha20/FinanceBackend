from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)        # income or expense
    category = Column(String, nullable=False)    # salary, food, rent etc
    date = Column(DateTime, nullable=False)
    notes = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)  # soft delete
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())