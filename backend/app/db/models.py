from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    investments = relationship("Investment", back_populates="user")


class MutualFund(Base):
    __tablename__ = "mutual_funds"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    isn = Column(String, unique=True, index=True, nullable=False)
    fund_type = Column(String, nullable=False)
    fund_category = Column(String, nullable=False)
    fund_house = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    investments = relationship("Investment", back_populates="fund")
    performances = relationship("FundPerformance", back_populates="fund")
    allocations = relationship("FundAllocation", back_populates="fund")
    holdings = relationship("FundHolding", back_populates="fund")
    cap_allocations = relationship("FundCapAllocation", back_populates="fund")


class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    fund_id = Column(String, ForeignKey("mutual_funds.id"))
    investment_date = Column(Date, nullable=False)
    amount_invested = Column(Float, nullable=False)
    nav_at_investment = Column(Float, nullable=False)
    units = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="investments")
    fund = relationship("MutualFund", back_populates="investments")


class FundPerformance(Base):
    __tablename__ = "fund_performances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fund_id = Column(String, ForeignKey("mutual_funds.id"))
    date = Column(Date, nullable=False)
    nav = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    fund = relationship("MutualFund", back_populates="performances")


class FundAllocation(Base):
    __tablename__ = "fund_allocations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fund_id = Column(String, ForeignKey("mutual_funds.id"))
    sector = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    fund = relationship("MutualFund", back_populates="allocations")


class FundHolding(Base):
    __tablename__ = "fund_holdings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fund_id = Column(String, ForeignKey("mutual_funds.id"))
    stock_name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    fund = relationship("MutualFund", back_populates="holdings")


class FundCapAllocation(Base):
    __tablename__ = "fund_cap_allocations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fund_id = Column(String, ForeignKey("mutual_funds.id"))
    cap_type = Column(String, nullable=False)  # Large Cap, Mid Cap, Small Cap
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    fund = relationship("MutualFund", back_populates="cap_allocations")