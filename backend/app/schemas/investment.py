from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional

# Base investment schema
class InvestmentBase(BaseModel):
    fund_id: str
    investment_date: date
    amount_invested: float = Field(gt=0, description="Amount must be greater than 0")
    nav_at_investment: float = Field(gt=0, description="NAV must be greater than 0")

# Schema for creating a new investment
class InvestmentCreate(InvestmentBase):
    @validator('amount_invested')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount invested must be positive')
        return v
    
    @validator('nav_at_investment')
    def validate_nav(cls, v):
        if v <= 0:
            raise ValueError('NAV must be positive')
        return v

# Schema for updating an investment
class InvestmentUpdate(BaseModel):
    investment_date: Optional[date] = None
    amount_invested: Optional[float] = Field(None, gt=0, description="Amount must be greater than 0")
    nav_at_investment: Optional[float] = Field(None, gt=0, description="NAV must be greater than 0")
    
    @validator('amount_invested')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount invested must be positive')
        return v
    
    @validator('nav_at_investment')
    def validate_nav(cls, v):
        if v is not None and v <= 0:
            raise ValueError('NAV must be positive')
        return v

# Schema for investment response
class InvestmentResponse(InvestmentBase):
    id: str
    user_id: str
    units: float
    created_at: datetime

    class Config:
        from_attributes = True  