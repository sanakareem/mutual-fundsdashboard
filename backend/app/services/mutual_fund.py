from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.models import MutualFund, FundPerformance, FundAllocation, FundHolding, FundCapAllocation

def get_mutual_funds(db: Session, skip: int = 0, limit: int = 100) -> List[MutualFund]:
    """Get a list of mutual funds."""
    return db.query(MutualFund).offset(skip).limit(limit).all()

def get_mutual_fund_by_id(db: Session, fund_id: str) -> Optional[MutualFund]:
    """Get a mutual fund by ID."""
    return db.query(MutualFund).filter(MutualFund.id == fund_id).first()

def get_mutual_fund_by_isn(db: Session, isn: str) -> Optional[MutualFund]:
    """Get a mutual fund by ISN."""
    return db.query(MutualFund).filter(MutualFund.isn == isn).first()

def get_mutual_fund_performances(db: Session, fund_id: str) -> List[FundPerformance]:
    """Get performance data for a mutual fund."""
    return db.query(FundPerformance).filter(FundPerformance.fund_id == fund_id).all()

def get_mutual_fund_allocations(db: Session, fund_id: str) -> List[FundAllocation]:
    """Get sector allocations for a mutual fund."""
    return db.query(FundAllocation).filter(FundAllocation.fund_id == fund_id).all()

def get_mutual_fund_holdings(db: Session, fund_id: str) -> List[FundHolding]:
    """Get stock holdings for a mutual fund."""
    return db.query(FundHolding).filter(FundHolding.fund_id == fund_id).all()

def get_mutual_fund_cap_allocations(db: Session, fund_id: str) -> List[FundCapAllocation]:
    """Get market cap allocations for a mutual fund."""
    return db.query(FundCapAllocation).filter(FundCapAllocation.fund_id == fund_id).all()

def create_mutual_fund(
    db: Session, 
    name: str,
    isn: str,
    fund_type: str,
    fund_category: str,
    fund_house: str
) -> MutualFund:
    """Create a new mutual fund."""
    db_fund = MutualFund(
        name=name,
        isn=isn,
        fund_type=fund_type,
        fund_category=fund_category,
        fund_house=fund_house
    )
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund

def add_fund_performance(
    db: Session,
    fund_id: str,
    date: str,
    nav: float
) -> FundPerformance:
    """Add performance data for a mutual fund."""
    db_performance = FundPerformance(
        fund_id=fund_id,
        date=date,
        nav=nav
    )
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance

def add_fund_allocation(
    db: Session,
    fund_id: str,
    sector: str,
    percentage: float
) -> FundAllocation:
    """Add sector allocation for a mutual fund."""
    db_allocation = FundAllocation(
        fund_id=fund_id,
        sector=sector,
        percentage=percentage
    )
    db.add(db_allocation)
    db.commit()
    db.refresh(db_allocation)
    return db_allocation

def add_fund_holding(
    db: Session,
    fund_id: str,
    stock_name: str,
    percentage: float
) -> FundHolding:
    """Add stock holding for a mutual fund."""
    db_holding = FundHolding(
        fund_id=fund_id,
        stock_name=stock_name,
        percentage=percentage
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

def add_fund_cap_allocation(
    db: Session,
    fund_id: str,
    cap_type: str,
    percentage: float
) -> FundCapAllocation:
    """Add market cap allocation for a mutual fund."""
    db_cap_allocation = FundCapAllocation(
        fund_id=fund_id,
        cap_type=cap_type,
        percentage=percentage
    )
    db.add(db_cap_allocation)
    db.commit()
    db.refresh(db_cap_allocation)
    return db_cap_allocation