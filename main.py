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
from crud import AnalysisCRUD
from queue_config import get_queue, is_redis_available
from background_tasks import run_financial_analysis

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
        
        # Create analysis record
        analysis_record = AnalysisCRUD.create_analysis(
            db=db,
            query=query,
            analysis_type="comprehensive"
        )
        
        # Check if Redis queue is available
        if is_redis_available():
            # Queue the analysis task
            queue = get_queue()
            job = queue.enqueue(
                run_financial_analysis,
                analysis_record.id,
                query,
                file_path,
                timeout='10m'  # 10 minute timeout
            )
            
            return {
                "status": "queued",
                "message": "Financial document analysis queued for processing",
                "query": query,
                "analysis": {
                    "analysis_id": analysis_record.id,
                    "job_id": job.id,
                    "status": "queued",
                    "summary": "Analysis has been queued and will be processed in the background"
                },
                "file_info": {
                    "filename": file.filename,
                    "file_size": len(content)
                },
                "disclaimer": "This analysis is for informational purposes only. Please consult with qualified financial professionals before making investment decisions."
            }
        else:
            # Fallback to synchronous processing if Redis is not available
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
                    "filename": file.filename,
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
        # File cleanup is now handled in the background task
        pass

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
        "user_id": analysis.user_id
    }

@app.get("/queue/status")
async def get_queue_status():
    """Get queue status and statistics"""
    if not is_redis_available():
        return {
            "status": "unavailable",
            "message": "Redis queue is not available",
            "fallback": "Using synchronous processing"
        }
    
    queue = get_queue()
    
    return {
        "status": "available",
        "queue_name": "analysis",
        "pending_jobs": len(queue),
        "failed_jobs": len(queue.failed_job_registry),
        "finished_jobs": len(queue.finished_job_registry),
        "message": "Redis queue is operational"
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