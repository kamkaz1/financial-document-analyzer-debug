from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document as analyze_task, verification, investment_analysis, risk_assessment

app = FastAPI(title="Financial Document Analyzer", description="AI-powered financial document analysis system")

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
    query: str = Form(default="Provide a comprehensive analysis of this financial document including key metrics, trends, investment outlook, and risk assessment")
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
        
        # Process the financial document with all analysts
        analysis_result = run_crew(query=query, file_path=file_path)
        
        return {
            "status": "success",
            "message": "Financial document analyzed successfully",
            "query": query,
            "analysis": {
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
                "processed_at": file_path,
                "file_size": len(content)
            },
            "disclaimer": "This analysis is for informational purposes only. Please consult with qualified financial professionals before making investment decisions."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                # Log cleanup error but don't fail the request
                print(f"Warning: Could not clean up file {file_path}: {cleanup_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )