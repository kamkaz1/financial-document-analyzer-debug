"""
CRUD operations for Financial Document Analyzer database
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import Analysis


# Analysis CRUD operations
class AnalysisCRUD:
    @staticmethod
    def create_analysis(
        db: Session,
        query: str,
        analysis_type: str = "comprehensive"
    ) -> Analysis:
        """Create a new analysis record"""
        analysis = Analysis(
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
    

