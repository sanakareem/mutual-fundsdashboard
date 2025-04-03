from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.models import Investment, MutualFund
from app.schemas.investment import InvestmentCreate, InvestmentUpdate
from app.core.exceptions import NotFoundError, ForbiddenError

def create_investment(db: Session, investment_data: InvestmentCreate, user_id: str) -> Investment:
    """Create a new investment record."""
    # Verify that the mutual fund exists
    fund = db.query(MutualFund).filter(MutualFund.id == investment_data.fund_id).first()
    if not fund:
        raise NotFoundError(f"Mutual fund with ID {investment_data.fund_id} not found")
    
    # Calculate units based on amount invested and NAV
    units = investment_data.amount_invested / investment_data.nav_at_investment
    
    # Create investment record
    db_investment = Investment(
        user_id=user_id,
        fund_id=investment_data.fund_id,
        investment_date=investment_data.investment_date,
        amount_invested=investment_data.amount_invested,
        nav_at_investment=investment_data.nav_at_investment,
        units=units
    )
    
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    
    return db_investment

def get_investments_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Investment]:
    """Get all investments for a user."""
    return db.query(Investment)\
        .filter(Investment.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_investment_by_id(db: Session, investment_id: str) -> Optional[Investment]:
    """Get an investment by ID."""
    investment = db.query(Investment).filter(Investment.id == investment_id).first()
    if not investment:
        raise NotFoundError(f"Investment with ID {investment_id} not found")
    return investment

def update_investment(db: Session, investment_id: str, investment_data: InvestmentUpdate) -> Investment:
    """Update an investment."""
    # Get the investment
    investment = get_investment_by_id(db, investment_id)
    
    # Update fields
    if investment_data.investment_date is not None:
        investment.investment_date = investment_data.investment_date
    
    if investment_data.amount_invested is not None:
        investment.amount_invested = investment_data.amount_invested
        # Recalculate units if amount invested or NAV changes
        if investment_data.nav_at_investment is not None:
            investment.nav_at_investment = investment_data.nav_at_investment
            investment.units = investment_data.amount_invested / investment_data.nav_at_investment
        else:
            investment.units = investment_data.amount_invested / investment.nav_at_investment
    elif investment_data.nav_at_investment is not None:
        # Only NAV changed
        investment.nav_at_investment = investment_data.nav_at_investment
        investment.units = investment.amount_invested / investment_data.nav_at_investment
    
    db.commit()
    db.refresh(investment)
    
    return investment

def delete_investment(db: Session, investment_id: str) -> Investment:
    """Delete an investment."""
    # Get the investment
    investment = get_investment_by_id(db, investment_id)
    
    # Delete the investment
    db.delete(investment)
    db.commit()
    
    return investment