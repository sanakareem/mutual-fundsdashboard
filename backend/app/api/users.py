from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.auth import get_user_by_id, update_user, deactivate_user, activate_user
from app.api.auth import get_current_active_user, get_current_user
from app.core.exceptions import NotFoundError, ForbiddenError
from app.db.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    updated_user = update_user(
        db, 
        current_user.id, 
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password if user_data.password else None
    )
    return updated_user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific user by ID."""
    # Only allow users to access their own profile unless they are an admin
    if user_id != current_user.id:
        raise ForbiddenError("Not authorized to access this user")
    
    try:
        user = get_user_by_id(db, user_id)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(
    user_id: str,
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a specific user by ID."""
    # Only allow users to update their own profile
    if user_id != current_user.id:
        raise ForbiddenError("Not authorized to update this user")
    
    try:
        updated_user = update_user(
            db, 
            user_id, 
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password if user_data.password else None
        )
        return updated_user
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deactivate a user account."""
    # Only allow users to deactivate their own account
    if user_id != current_user.id:
        raise ForbiddenError("Not authorized to deactivate this user")
    
    try:
        deactivated_user = deactivate_user(db, user_id)
        return deactivated_user
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))