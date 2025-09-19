"""
Database configuration and models for Financial Document Analyzer
"""

import os
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from databases import Database

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./financial_analyzer.db")

# For development, use SQLite. For production, use PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL configuration
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Async database connection
database = Database(DATABASE_URL)

# Database Models
class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user")

class Analysis(Base):
    """Analysis model for storing financial document analysis results"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    
    # Analysis metadata
    query = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    analysis_type = Column(String, default="comprehensive")  # comprehensive, investment, risk, verification
    
    # Results
    result_summary = Column(Text, nullable=True)
    detailed_results = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    file = relationship("File", back_populates="analyses")

class File(Base):
    """File model for storing uploaded file information"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, default="pdf")
    
    # File metadata
    upload_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Status
    is_processed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="file")

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization
async def init_database():
    """Initialize database tables"""
    await database.connect()
    Base.metadata.create_all(bind=engine)

async def close_database():
    """Close database connection"""
    await database.disconnect()
