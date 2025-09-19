# Financial Document Analyzer

A professional AI-powered financial document analysis system built with CrewAI, featuring specialized agents for comprehensive financial analysis, investment recommendations, and risk assessment.





### API Endpoints
- `GET /` - Health check
- `GET /health` - Detailed system status
- `POST /analyze` - Upload and analyze financial documents

## 🐛 Bugs Found and Fixed

### Deterministic Bugs

#### 1. README.md
- **Bug**: Incorrect filename in install command (`requirement.txt` vs `requirements.txt`)
- **Fix**: Corrected to `pip install -r requirements.txt`

#### 2. agents.py
- **Bug**: Incorrect import (`from crewai.agents import Agent` vs `from crewai import Agent`)
- **Bug**: Missing 's' in tools parameter (`tool=[...]` vs `tools=[...]`)
- **Bug**: LLM configuration issues and tool validation errors
- **Bug**: Tool validation error when using custom functions as tools
- **Bug**: LLM parameter treated as required when it's optional
- **Fix**: 
  - Corrected import statement
  - Fixed tools parameter syntax
  - Implemented proper LLM configuration with graceful fallbacks
  - Used `@tool` decorator from `crewai.tools` for proper tool creation
  - Made LLM parameter optional - CrewAI uses default LLM when not specified
  - Added comprehensive multi-agent architecture

#### 3. tools.py
- **Bug**: Incorrect import paths and method signatures
- **Bug**: Tool validation issues with CrewAI
- **Bug**: Custom functions not recognized as valid CrewAI tools
- **Bug**: `ValidationError: Input should be a valid dictionary or instance of BaseTool`
- **Fix**:
  - Fixed import statements
  - Used `@tool` decorator from `crewai.tools` to create proper BaseTool instances
  - Converted custom tool classes to decorated functions
  - Implemented professional tool architecture
  - Added comprehensive error handling and data processing

#### 4. main.py
- **Bug**: Function naming conflict (`analyze_financial_document` vs `analyze_document`)
- **Bug**: Basic API with minimal functionality
- **Fix**:
  - Resolved naming conflicts
  - Implemented professional FastAPI with multiple endpoints
  - Added security features and file management

#### 5. task.py
- **Bug**: Inefficient and potentially harmful prompts
- **Fix**: Replaced with professional, structured task descriptions

#### 6. requirements.txt
- **Bug**: Missing dependencies (`python-multipart`, `langchain-openai`)
- **Bug**: Version conflicts (`onnxruntime==1.18.0`)
- **Fix**: Added missing dependencies and updated versions

### Inefficient Prompts Fixed

#### 1. Agent Prompts
- **Issue**: Encouraging fabrication and speculation
- **Fix**: Professional, evidence-based prompts with regulatory compliance focus

#### 2. Task Descriptions
- **Issue**: Vague, unprofessional language
- **Fix**: Structured, industry-standard task descriptions with clear objectives

#### 3. Expected Outputs
- **Issue**: Encouraging harmful or non-compliant advice
- **Fix**: Professional report formats with appropriate disclaimers

### Critical Tool Integration Bugs

#### 1. Tool Validation Error
- **Bug**: `ValidationError: 1 validation error for Agent tools.0 Input should be a valid dictionary or instance of BaseTool`
- **Root Cause**: Custom Python functions were being passed directly to agents as tools, but CrewAI expects BaseTool instances
- **Fix**: Used the `@tool` decorator from `crewai.tools` to properly create BaseTool instances
- **Example**:
  ```python
  # ❌ Before (caused validation error)
  def read_data_tool(path: str) -> str:
      return "data"
  
  # ✅ After (works correctly)
  @tool("Read Financial Document")
  def read_financial_document(path: str) -> str:
      return "data"
  ```

#### 2. LLM Parameter Misunderstanding
- **Bug**: Treating LLM parameter as required when it's optional
- **Root Cause**: Misunderstanding that CrewAI has a default LLM configuration
- **Fix**: Made LLM parameter optional with conditional loading
- **Implementation**:
  ```python
  # ✅ Correct approach - LLM is optional
  if os.getenv("OPENAI_API_KEY"):
      llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
  else:
      llm = None  # CrewAI will use default LLM
  
  agent = Agent(
      role="Financial Analyst",
      llm=llm if llm else None,  # Optional parameter
      # ... other parameters
  )
  ```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial-document-analyzer-debug
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create .env file for API keys (optional)
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "SERPER_API_KEY=your_serper_api_key_here" >> .env
   ```

### Running the Application

1. **Start the server**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Access the API**
   - API Documentation: http://127.0.0.1:8000/docs
   - Health Check: http://127.0.0.1:8000/
   - Detailed Health: http://127.0.0.1:8000/health

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Financial Document Analyzer API is running",
  "status": "healthy",
  "endpoints": {
    "analyze": "/analyze - POST - Upload financial document for analysis",
    "health": "/ - GET - Health check"
  }
}
```

#### 2. Detailed Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Financial Document Analyzer",
  "version": "1.0.0",
  "components": {
    "agents": ["financial_analyst", "verifier", "investment_advisor", "risk_assessor"],
    "tools": ["document_reader", "web_search"],
    "supported_formats": ["PDF"]
  }
}
```

#### 3. Analyze Financial Document
```http
POST /analyze
```

**Parameters:**
- `file` (form-data): PDF file containing financial document
- `query` (form-data, optional): Specific analysis query

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@financial_report.pdf" \
  -F "query=Analyze the company's financial performance and provide investment recommendations"
```

**Response:**
```json
{
  "status": "success",
  "message": "Financial document analyzed successfully",
  "query": "Analyze the company's financial performance...",
  "analysis": {
    "summary": "Comprehensive financial analysis completed by AI specialists",
    "detailed_results": "Detailed analysis results...",
    "components_analyzed": [
      "Document verification and authenticity",
      "Financial performance metrics and trends",
      "Investment opportunities and recommendations",
      "Risk assessment and mitigation strategies"
    ]
  },
  "file_info": {
    "filename": "financial_report.pdf",
    "processed_at": "data/financial_document_uuid.pdf",
    "file_size": 1024000
  },
  "disclaimer": "This analysis is for informational purposes only. Please consult with qualified financial professionals before making investment decisions."
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "Only PDF files are supported"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Error processing financial document: [error details]"
}
```

## 🔧 Usage Examples

### Python Client Example
```python
import requests

# Upload and analyze a financial document
with open('financial_report.pdf', 'rb') as f:
    files = {'file': f}
    data = {'query': 'Provide investment analysis and risk assessment'}
    
    response = requests.post(
        'http://127.0.0.1:8000/analyze',
        files=files,
        data=data
    )
    
    result = response.json()
    print(result['analysis']['detailed_results'])
```

## 🎁 Bonus Features

### Database Integration
- **SQLite Database**: Stores analysis results and user data
- **CRUD Operations**: Complete database management for analyses and users
- **Data Persistence**: All analysis results are saved and retrievable

### Redis Queue System
- **Asynchronous Processing**: Handle multiple analysis requests concurrently
- **Background Tasks**: Non-blocking document processing
- **Queue Management**: Monitor queue status and job statistics
- **Graceful Fallback**: Falls back to synchronous processing if Redis unavailable

### Project Structure
```
├── agents.py, task.py, tools.py    # Core CrewAI components
├── main.py                         # FastAPI application
├── database/                       # Database package
│   ├── database.py                # SQLAlchemy models
│   ├── crud.py                    # Database operations
│   └── init_db.py                 # Database initialization
└── redis_queue/                   # Queue package
    ├── queue_config.py            # Redis configuration
    ├── background_tasks.py        # Background processing
    └── worker.py                  # Queue worker
```


