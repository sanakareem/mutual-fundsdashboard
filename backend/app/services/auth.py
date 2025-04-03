from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union
from jose import jwt
from passlib.context import CryptContext
import logging

from app.db.models import User
from app.core.config import settings
from app.core.exceptions import ForbiddenError, NotFoundError

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash from plain password"""
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"Authentication failed: No user found with email {email}")
            return None
        
        if not verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: Invalid password for user {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Authentication failed: User {email} is inactive")
            raise ForbiddenError("Inactive user")
        
        logger.info(f"User {email} authenticated successfully")
        return user
    except Exception as e:
        logger.exception(f"Error during authentication for user {email}")
        raise


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.exception("Error creating access token")
        raise


def create_user(db: Session, email: str, password: str, full_name: str) -> User:
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            logger.warning(f"User creation failed: Email {email} already exists")
            raise ForbiddenError("Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            full_name=full_name,
            password_hash=hashed_password,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User {email} created successfully")
        return db_user
    except Exception as e:
        db.rollback()
        logger.exception(f"Error creating user: {str(e)}")
        raise


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(f"User with ID {user_id} not found")
    return user


def update_user(db: Session, user_id: str, **kwargs) -> User:
    """Update user information"""
    try:
        user = get_user_by_id(db, user_id)
        
        # Update user fields
        for key, value in kwargs.items():
            if key == 'password':
                user.password_hash = get_password_hash(value)
            elif hasattr(user, key):
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} updated successfully")
        return user
    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating user: {str(e)}")
        raise


def deactivate_user(db: Session, user_id: str) -> User:
    """Deactivate a user"""
    try:
        user = get_user_by_id(db, user_id)
        user.is_active = False
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} deactivated successfully")
        return user
    except Exception as e:
        db.rollback()
        logger.exception(f"Error deactivating user: {str(e)}")
        raise


def activate_user(db: Session, user_id: str) -> User:
    """Activate a user"""
    try:
        user = get_user_by_id(db, user_id)
        user.is_active = True
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} activated successfully")
        return user
    except Exception as e:
        db.rollback()
        logger.exception(f"Error activating user: {str(e)}")
        raise