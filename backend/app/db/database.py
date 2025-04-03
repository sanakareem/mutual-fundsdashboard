from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Generator, Optional
import logging

from app.core.config import settings
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

# Create a metadata instance
metadata = MetaData()

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.SQL_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base(metadata=metadata)


def get_engine() -> Engine:
    """Returns the database engine instance"""
    return engine


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and ensure it's closed after use"""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logger.exception("Database session error")
        session.rollback()
        raise DatabaseError(detail=str(e))
    finally:
        session.close()


class DatabaseManager:
    """Class for managing database operations"""

    @staticmethod
    def create_tables() -> None:
        """Create all tables defined in models"""
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Successfully created database tables")
        except Exception as e:
            logger.exception("Error creating database tables")
            raise DatabaseError(detail=f"Failed to create tables: {str(e)}")

    @staticmethod
    def drop_tables() -> None:
        """Drop all tables (dangerous, use only in testing)"""
        try:
            Base.metadata.drop_all(bind=engine)
            logger.info("Successfully dropped all database tables")
        except Exception as e:
            logger.exception("Error dropping database tables")
            raise DatabaseError(detail=f"Failed to drop tables: {str(e)}")

    @staticmethod
    def check_connection() -> bool:
        """Check if database connection is working"""
        try:
            # Try to connect and execute a simple query
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.exception("Database connection failed")
            raise DatabaseError(detail=f"Failed to connect to database: {str(e)}")
            
    @staticmethod
    def execute_raw_sql(sql: str, params: Optional[dict] = None) -> list:
        """Execute raw SQL query"""
        try:
            with engine.connect() as connection:
                if params:
                    result = connection.execute(sql, params)
                else:
                    result = connection.execute(sql)
                return [dict(row) for row in result]
        except Exception as e:
            logger.exception(f"Error executing SQL: {sql}")
            raise DatabaseError(detail=f"SQL execution failed: {str(e)}")