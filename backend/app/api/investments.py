from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.investment import InvestmentCreate, InvestmentResponse, InvestmentUpdate
from app.services.investment import create_investment, get_investments_by_user, get_investment_by_id, update_investment, delete_investment
from app.api.auth import get_current_active_user
from app.core.exceptions import NotFoundError, ForbiddenError
from app.db.models import User

router = APIRouter(
    prefix="/investments",
    tags=["Investments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=InvestmentResponse)
async def add_investment(
    investment_data: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add a new investment."""
    try:
        return create_investment(db, investment_data, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[InvestmentResponse])
async def read_investments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all investments for the current user."""
    return get_investments_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{investment_id}", response_model=InvestmentResponse)
async def read_investment(
    investment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific investment."""
    try:
        investment = get_investment_by_id(db, investment_id=investment_id)
        
        # Check if the investment belongs to the current user
        if investment.user_id != current_user.id:
            raise ForbiddenError("Not authorized to access this investment")
        
        return investment
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.put("/{investment_id}", response_model=InvestmentResponse)
async def update_investment_by_id(
    investment_id: str,
    investment_data: InvestmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific investment."""
    try:
        # Check if investment exists and belongs to the user
        existing_investment = get_investment_by_id(db, investment_id=investment_id)
        if existing_investment.user_id != current_user.id:
            raise ForbiddenError("Not authorized to update this investment")
        
        # Update the investment
        updated_investment = update_investment(db, investment_id, investment_data)
        return updated_investment
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{investment_id}", response_model=InvestmentResponse)
async def remove_investment(
    investment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific investment."""
    try:
        # Check if investment exists and belongs to the user
        existing_investment = get_investment_by_id(db, investment_id=investment_id)
        if existing_investment.user_id != current_user.id:
            raise ForbiddenError("Not authorized to delete this investment")
        
        # Delete the investment
        deleted_investment = delete_investment(db, investment_id)
        return deleted_investment
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))