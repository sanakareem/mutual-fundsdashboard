from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.portfolio import PortfolioSummary, PortfolioPerformance, PortfolioComposition, FundOverlap
from app.services.portfolio import get_portfolio_summary, get_portfolio_performance, get_portfolio_composition, get_fund_overlap
from app.api.auth import get_current_active_user

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
    responses={404: {"description": "Not found"}},
)

@router.get("/summary", response_model=PortfolioSummary)
async def read_portfolio_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get summary of the user's portfolio."""
    summary = get_portfolio_summary(db, user_id=current_user.id)
    return summary

@router.get("/performance", response_model=List[PortfolioPerformance])
async def read_portfolio_performance(
    timeframe: str = Query("1M", description="Timeframe for performance data (1M, 3M, 6M, 1Y, 3Y, MAX)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get performance data for the user's portfolio."""
    performance = get_portfolio_performance(db, user_id=current_user.id, timeframe=timeframe)
    return performance

@router.get("/composition", response_model=PortfolioComposition)
async def read_portfolio_composition(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get composition details of the user's portfolio."""
    composition = get_portfolio_composition(db, user_id=current_user.id)
    return composition

@router.get("/overlap", response_model=List[FundOverlap])
async def read_fund_overlap(
    fund_id1: str = Query(..., description="ID of the first mutual fund"),
    fund_id2: Optional[str] = Query(None, description="ID of the second mutual fund (optional)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get overlap analysis between mutual funds in the portfolio."""
    overlap = get_fund_overlap(db, fund_id1=fund_id1, fund_id2=fund_id2)
    return overlap