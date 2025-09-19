"""
Background tasks for Financial Document Analyzer using Redis Queue
"""

import os
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document as analyze_task, verification, investment_analysis, risk_assessment
from database import SessionLocal
from crud import AnalysisCRUD

def run_financial_analysis(analysis_id: int, query: str, file_path: str):
    """
    Background task to run financial analysis
    
    Args:
        analysis_id (int): ID of the analysis record in database
        query (str): Analysis query
        file_path (str): Path to the uploaded file
    """
    db = SessionLocal()
    
    try:
        # Update status to processing
        AnalysisCRUD.update_analysis_status(
            db=db,
            analysis_id=analysis_id,
            status="processing"
        )
        
        # Run the financial analysis crew
        financial_crew = Crew(
            agents=[financial_analyst, verifier, investment_advisor, risk_assessor],
            tasks=[verification, analyze_task, investment_analysis, risk_assessment],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute analysis
        analysis_result = financial_crew.kickoff({'query': query})
        
        # Update analysis with results
        AnalysisCRUD.update_analysis_status(
            db=db,
            analysis_id=analysis_id,
            status="completed",
            result_summary="Comprehensive financial analysis completed by AI specialists",
            detailed_results={
                "analysis_result": str(analysis_result),
                "components_analyzed": [
                    "Document verification and authenticity",
                    "Financial performance metrics and trends",
                    "Investment opportunities and recommendations",
                    "Risk assessment and mitigation strategies"
                ]
            }
        )
        
        print(f"✅ Analysis {analysis_id} completed successfully")
        
    except Exception as e:
        # Update analysis status to failed
        AnalysisCRUD.update_analysis_status(
            db=db,
            analysis_id=analysis_id,
            status="failed",
            error_message=str(e)
        )
        print(f"❌ Analysis {analysis_id} failed: {str(e)}")
        raise
        
    finally:
        db.close()
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Cleaned up file: {file_path}")
            except Exception as cleanup_error:
                print(f"⚠️ Could not clean up file {file_path}: {cleanup_error}")
