from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
import asyncio
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document as analyze_task, verification, investment_analysis, risk_assessment
from database import get_db, init_database, close_database
from crud import CombinedCRUD, AnalysisCRUD, FileCRUD

app = FastAPI(title="Financial Document Analyzer", description="AI-powered financial document analysis system")

# Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database on shutdown"""
    await close_database()

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the complete financial analysis crew"""
    try:
        financial_crew = Crew(
            agents=[financial_analyst, verifier, investment_advisor, risk_assessor],
            tasks=[verification, analyze_task, investment_analysis, risk_assessment],
            process=Process.sequential,
            verbose=True
        )
        
        result = financial_crew.kickoff({'query': query})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy",
        "endpoints": {
            "analyze": "/analyze - POST - Upload financial document for analysis",
            "health": "/ - GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Financial Document Analyzer",
        "version": "1.0.0",
        "components": {
            "agents": ["financial_analyst", "verifier", "investment_advisor", "risk_assessor"],
            "tools": ["document_reader", "web_search"],
            "supported_formats": ["PDF"]
        }
    }

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive analysis of this financial document including key metrics, trends, investment outlook, and risk assessment"),
    db: Session = Depends(get_db)
):
    """
    Analyze financial document and provide comprehensive investment recommendations
    
    Args:
        file: PDF file containing financial document
        query: Specific analysis query (optional)
    
    Returns:
        JSON response with detailed financial analysis
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        # Validate and sanitize query
        if not query or query.strip() == "":
            query = "Provide a comprehensive analysis of this financial document including key metrics, trends, investment outlook, and risk assessment"
        
        query = query.strip()[:1000]  # Limit query length for security
        
        # Create database records
        file_record, analysis_record = CombinedCRUD.create_analysis_with_file(
            db=db,
            filename=f"financial_document_{file_id}.pdf",
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            query=query,
            analysis_type="comprehensive"
        )
        
        # Update analysis status to processing
        AnalysisCRUD.update_analysis_status(
            db=db,
            analysis_id=analysis_record.id,
            status="processing"
        )
        
        # Process the financial document with all analysts
        analysis_result = run_crew(query=query, file_path=file_path)
        
        # Update analysis with results
        AnalysisCRUD.update_analysis_status(
            db=db,
            analysis_id=analysis_record.id,
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
        
        # Mark file as processed
        FileCRUD.mark_file_processed(db=db, file_id=file_record.id)
        
        return {
            "status": "success",
            "message": "Financial document analyzed successfully",
            "query": query,
            "analysis": {
                "analysis_id": analysis_record.id,
                "summary": "Comprehensive financial analysis completed by AI specialists",
                "detailed_results": str(analysis_result),
                "components_analyzed": [
                    "Document verification and authenticity",
                    "Financial performance metrics and trends",
                    "Investment opportunities and recommendations", 
                    "Risk assessment and mitigation strategies"
                ]
            },
            "file_info": {
                "file_id": file_record.id,
                "filename": file.filename,
                "processed_at": file_path,
                "file_size": len(content)
            },
            "disclaimer": "This analysis is for informational purposes only. Please consult with qualified financial professionals before making investment decisions."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Update analysis status to failed if we have an analysis record
        if 'analysis_record' in locals():
            try:
                AnalysisCRUD.update_analysis_status(
                    db=db,
                    analysis_id=analysis_record.id,
                    status="failed",
                    error_message=str(e)
                )
            except:
                pass  # Don't fail the main error handling
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                # Log cleanup error but don't fail the request
                print(f"Warning: Could not clean up file {file_path}: {cleanup_error}")

# New database-related endpoints
@app.get("/analyses")
async def get_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get recent analyses with pagination"""
    analyses = AnalysisCRUD.get_recent_analyses(db=db, skip=skip, limit=limit)
    return {
        "analyses": [
            {
                "id": analysis.id,
                "query": analysis.query,
                "status": analysis.status,
                "analysis_type": analysis.analysis_type,
                "created_at": analysis.created_at,
                "completed_at": analysis.completed_at,
                "file_id": analysis.file_id,
                "user_id": analysis.user_id
            }
            for analysis in analyses
        ],
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": len(analyses)
        }
    }

@app.get("/analyses/{analysis_id}")
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get specific analysis by ID"""
    analysis = AnalysisCRUD.get_analysis(db=db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "query": analysis.query,
        "status": analysis.status,
        "analysis_type": analysis.analysis_type,
        "result_summary": analysis.result_summary,
        "detailed_results": analysis.detailed_results,
        "error_message": analysis.error_message,
        "created_at": analysis.created_at,
        "started_at": analysis.started_at,
        "completed_at": analysis.completed_at,
        "file_id": analysis.file_id,
        "user_id": analysis.user_id
    }

@app.get("/files")
async def get_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get uploaded files with pagination"""
    files = FileCRUD.get_files(db=db, skip=skip, limit=limit)
    return {
        "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "original_filename": file.original_filename,
                "file_size": file.file_size,
                "file_type": file.file_type,
                "uploaded_at": file.uploaded_at,
                "processed_at": file.processed_at,
                "is_processed": file.is_processed
            }
            for file in files
        ],
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": len(files)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )