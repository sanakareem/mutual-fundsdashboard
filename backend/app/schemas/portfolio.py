from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Portfolio summary schema
class PortfolioSummary(BaseModel):
    current_value: float
    initial_investment: float
    total_return: float
    return_percentage: float
    best_performing_fund: str
    best_performing_return: float
    worst_performing_fund: str
    worst_performing_return: float

# Portfolio performance schema
class PortfolioPerformance(BaseModel):
    date: date
    value: float

# Sector allocation schema
class SectorAllocation(BaseModel):
    sector: str
    amount: float
    percentage: float

# Stock allocation schema
class StockAllocation(BaseModel):
    stock_name: str
    amount: float
    percentage: float

# Market cap allocation schema
class CapAllocation(BaseModel):
    cap_type: str  # Large Cap, Mid Cap, Small Cap
    amount: float
    percentage: float

# Portfolio composition schema
class PortfolioComposition(BaseModel):
    sector_allocations: List[SectorAllocation]
    stock_allocations: List[StockAllocation]
    cap_allocations: List[CapAllocation]

# Fund overlap schema
class FundOverlap(BaseModel):
    fund1_name: str
    fund2_name: str
    overlap_percentage: float
    common_stocks: List[str]