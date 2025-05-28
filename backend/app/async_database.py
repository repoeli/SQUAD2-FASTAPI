"""
Async database configuration module.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import Base for schema reference in the startup event in main.py.
# Base is used in app.main:startup_db_client to create database tables.
from app.database import Base  # noqa: F401
__all__ = ["async_engine", "AsyncSessionLocal", "get_async_db", "Base"]

# Get database URL from environment variable
# Convert regular PostgreSQL URL to async version by adding +asyncpg
# The DATABASE_URL should point to the Docker service name 'db' on port 5432 (internal container port)
# For local development without Docker, you can modify this to localhost:5434
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://grc_user:grc_pass@db:5432/grc_dashboard")

# Always use PostgreSQL with asyncpg driver
ASYNC_DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

# Create SQLAlchemy async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=os.getenv("DEBUG_MODE", "False").lower() == "true",  # SQL logging when in debug mode
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Async dependency for FastAPI
async def get_async_db():
    """
    Get async database session for dependency injection.
    
    Yields:
        SQLAlchemy AsyncSession
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
