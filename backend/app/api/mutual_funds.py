from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.mutual_fund import MutualFundResponse, MutualFundDetail, MutualFundPerformance, SectorAllocation, StockHolding, CapAllocation
from app.services.mutual_fund import get_mutual_funds, get_mutual_fund_by_id, get_mutual_fund_performances, get_mutual_fund_allocations, get_mutual_fund_holdings, get_mutual_fund_cap_allocations
from app.api.auth import get_current_active_user

router = APIRouter(
    prefix="/mutual-funds",
    tags=["Mutual Funds"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[MutualFundResponse])
async def read_mutual_funds(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a list of mutual funds."""
    mutual_funds = get_mutual_funds(db, skip=skip, limit=limit)
    return mutual_funds

@router.get("/{fund_id}", response_model=MutualFundDetail)
async def read_mutual_fund(
    fund_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get detailed information about a specific mutual fund."""
    mutual_fund = get_mutual_fund_by_id(db, fund_id=fund_id)
    if mutual_fund is None:
        raise HTTPException(status_code=404, detail="Mutual fund not found")
    return mutual_fund

@router.get("/{fund_id}/performance", response_model=List[MutualFundPerformance])
async def read_mutual_fund_performance(
    fund_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get performance data for a specific mutual fund."""
    performances = get_mutual_fund_performances(db, fund_id=fund_id)
    if not performances:
        raise HTTPException(status_code=404, detail="Performance data not found")
    return performances

@router.get("/{fund_id}/allocations", response_model=List[SectorAllocation])
async def read_mutual_fund_allocations(
    fund_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get sector allocations for a specific mutual fund."""
    allocations = get_mutual_fund_allocations(db, fund_id=fund_id)
    if not allocations:
        raise HTTPException(status_code=404, detail="Allocation data not found")
    return allocations

@router.get("/{fund_id}/holdings", response_model=List[StockHolding])
async def read_mutual_fund_holdings(
    fund_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get stock holdings for a specific mutual fund."""
    holdings = get_mutual_fund_holdings(db, fund_id=fund_id)
    if not holdings:
        raise HTTPException(status_code=404, detail="Holding data not found")
    return holdings

@router.get("/{fund_id}/cap-allocations", response_model=List[CapAllocation])
async def read_mutual_fund_cap_allocations(
    fund_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get market cap allocations for a specific mutual fund."""
    cap_allocations = get_mutual_fund_cap_allocations(db, fund_id=fund_id)
    if not cap_allocations:
        raise HTTPException(status_code=404, detail="Cap allocation data not found")
    return cap_allocations