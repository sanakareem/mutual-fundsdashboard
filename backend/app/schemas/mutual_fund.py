from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import List, Optional

# Base mutual fund schema
class MutualFundBase(BaseModel):
    name: str
    isn: str
    fund_type: str
    fund_category: str
    fund_house: str

# Schema for creating a new mutual fund
class MutualFundCreate(MutualFundBase):
    @validator('isn')
    def validate_isn(cls, v):
        # ISN should be alphanumeric and match a specific pattern
        if not v or len(v) < 5:
            raise ValueError('Invalid ISN format')
        return v

# Schema for updating a mutual fund
class MutualFundUpdate(BaseModel):
    name: Optional[str] = None
    fund_type: Optional[str] = None
    fund_category: Optional[str] = None
    fund_house: Optional[str] = None

# Response schema for list of mutual funds
class MutualFundResponse(MutualFundBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Performance schemas
class MutualFundPerformance(BaseModel):
    date: date
    nav: float

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Allocation schemas
class SectorAllocation(BaseModel):
    sector: str
    percentage: float

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Stock holding schemas
class StockHolding(BaseModel):
    stock_name: str
    percentage: float

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Market cap allocation schemas
class CapAllocation(BaseModel):
    cap_type: str  # Large Cap, Mid Cap, Small Cap
    percentage: float

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Detailed mutual fund schema
class MutualFundDetail(MutualFundResponse):
    performances: List[MutualFundPerformance] = []
    sector_allocations: List[SectorAllocation] = []
    holdings: List[StockHolding] = []
    cap_allocations: List[CapAllocation] = []

    class Config:
        from_attributes = True  # Updated from orm_mode = True

# Schema for mutual fund search
class MutualFundSearch(BaseModel):
    term: str
    fund_type: Optional[str] = None
    fund_category: Optional[str] = None
    fund_house: Optional[str] = None

# Schema for mutual fund comparison
class MutualFundCompare(BaseModel):
    fund_ids: List[str]

# Schema for mutual fund returns
class MutualFundReturns(BaseModel):
    fund_id: str
    name: str
    one_month: Optional[float] = None
    three_month: Optional[float] = None
    six_month: Optional[float] = None
    one_year: Optional[float] = None
    three_year: Optional[float] = None
    five_year: Optional[float] = None
    since_inception: Optional[float] = None

    class Config:
        from_attributes = True 