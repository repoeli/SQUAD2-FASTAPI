"""
Database configuration module.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable
# The DATABASE_URL should point to the Docker service name 'db' on port 5432 (internal container port)
# For local development without Docker, you can modify this to localhost:5434
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://grc_user:grc_pass@db:5432/grc_dashboard")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using from pool
    echo=os.getenv("DEBUG_MODE", "False").lower() == "true"  # SQL logging when in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for ORM models
Base = declarative_base()


def get_db():
    """
    Get database session for dependency injection.
    
    Yields:
        SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
