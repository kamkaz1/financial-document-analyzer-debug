"""
CRUD operations for Financial Document Analyzer database
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import User, Analysis, File

# User CRUD operations
class UserCRUD:
    @staticmethod
    def create_user(db: Session, email: str = None, name: str = None) -> User:
        """Create a new user"""
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

# File CRUD operations
class FileCRUD:
    @staticmethod
    def create_file(
        db: Session, 
        filename: str, 
        original_filename: str, 
        file_path: str, 
        file_size: int,
        file_type: str = "pdf",
        upload_ip: str = None,
        user_agent: str = None
    ) -> File:
        """Create a new file record"""
        file_record = File(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            upload_ip=upload_ip,
            user_agent=user_agent
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        return file_record
    
    @staticmethod
    def get_file(db: Session, file_id: int) -> Optional[File]:
        """Get file by ID"""
        return db.query(File).filter(File.id == file_id).first()
    
    @staticmethod
    def get_files(db: Session, skip: int = 0, limit: int = 100) -> List[File]:
        """Get all files with pagination"""
        return db.query(File).filter(File.is_deleted == False).offset(skip).limit(limit).all()
    
    @staticmethod
    def mark_file_processed(db: Session, file_id: int) -> Optional[File]:
        """Mark file as processed"""
        file_record = db.query(File).filter(File.id == file_id).first()
        if file_record:
            file_record.is_processed = True
            file_record.processed_at = datetime.utcnow()
            db.commit()
            db.refresh(file_record)
        return file_record
    
    @staticmethod
    def delete_file(db: Session, file_id: int) -> bool:
        """Soft delete file"""
        file_record = db.query(File).filter(File.id == file_id).first()
        if file_record:
            file_record.is_deleted = True
            db.commit()
            return True
        return False

# Analysis CRUD operations
class AnalysisCRUD:
    @staticmethod
    def create_analysis(
        db: Session,
        file_id: int,
        query: str,
        user_id: int = None,
        analysis_type: str = "comprehensive"
    ) -> Analysis:
        """Create a new analysis record"""
        analysis = Analysis(
            file_id=file_id,
            user_id=user_id,
            query=query,
            analysis_type=analysis_type,
            status="pending"
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis
    
    @staticmethod
    def get_analysis(db: Session, analysis_id: int) -> Optional[Analysis]:
        """Get analysis by ID"""
        return db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    @staticmethod
    def get_analyses_by_file(db: Session, file_id: int) -> List[Analysis]:
        """Get all analyses for a specific file"""
        return db.query(Analysis).filter(Analysis.file_id == file_id).all()
    
    @staticmethod
    def get_analyses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Analysis]:
        """Get all analyses for a specific user"""
        return db.query(Analysis).filter(Analysis.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_recent_analyses(db: Session, skip: int = 0, limit: int = 100) -> List[Analysis]:
        """Get recent analyses"""
        return db.query(Analysis).order_by(desc(Analysis.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_analysis_status(
        db: Session, 
        analysis_id: int, 
        status: str, 
        result_summary: str = None,
        detailed_results: Dict[str, Any] = None,
        error_message: str = None
    ) -> Optional[Analysis]:
        """Update analysis status and results"""
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = status
            
            if status == "processing":
                analysis.started_at = datetime.utcnow()
            elif status in ["completed", "failed"]:
                analysis.completed_at = datetime.utcnow()
            
            if result_summary:
                analysis.result_summary = result_summary
            if detailed_results:
                analysis.detailed_results = detailed_results
            if error_message:
                analysis.error_message = error_message
            
            db.commit()
            db.refresh(analysis)
        return analysis
    

# Combined CRUD operations
class CombinedCRUD:
    @staticmethod
    def create_analysis_with_file(
        db: Session,
        filename: str,
        original_filename: str,
        file_path: str,
        file_size: int,
        query: str,
        user_id: int = None,
        analysis_type: str = "comprehensive",
        upload_ip: str = None,
        user_agent: str = None
    ) -> tuple[File, Analysis]:
        """Create both file and analysis records in a transaction"""
        # Create file record
        file_record = FileCRUD.create_file(
            db=db,
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            upload_ip=upload_ip,
            user_agent=user_agent
        )
        
        # Create analysis record
        analysis = AnalysisCRUD.create_analysis(
            db=db,
            file_id=file_record.id,
            user_id=user_id,
            query=query,
            analysis_type=analysis_type
        )
        
        return file_record, analysis
