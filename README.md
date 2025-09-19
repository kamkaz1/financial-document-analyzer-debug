# Financial Document Analyzer

A professional AI-powered financial document analysis system built with CrewAI, featuring specialized agents for comprehensive financial analysis, investment recommendations, and risk assessment.

## 🚀 Features

- **Multi-Agent Architecture**: 4 specialized AI agents for different aspects of financial analysis
- **Professional API**: FastAPI-based REST API with comprehensive endpoints
- **Advanced Tools**: Specialized tools for document processing, investment analysis, and risk assessment
- **Security Features**: File validation, query sanitization, and secure file handling
- **Production Ready**: Comprehensive error handling, logging, and cleanup

## 🏗️ Architecture

### Specialized Agents
- **Financial Analyst**: Core financial analysis and reporting
- **Document Verifier**: Authentication and compliance checking
- **Investment Advisor**: Evidence-based investment recommendations
- **Risk Assessor**: Comprehensive risk analysis and mitigation strategies

### Professional Tools
- **FinancialDocumentTool**: Advanced PDF reading with text cleaning
- **InvestmentTool**: Intelligent investment analysis with keyword detection
- **RiskTool**: Comprehensive risk assessment with indicator identification

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

### JavaScript/Node.js Example
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('financial_report.pdf'));
form.append('query', 'Analyze financial performance and provide recommendations');

axios.post('http://127.0.0.1:8000/analyze', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log(response.data.analysis.detailed_results);
})
.catch(error => {
  console.error('Error:', error.response.data);
});
```

## 🏛️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   CrewAI Crew    │    │  Specialized    │
│                 │    │                  │    │    Agents       │
│  - File Upload  │───▶│  - Sequential    │───▶│                 │
│  - Validation   │    │    Processing    │    │  - Financial    │
│  - Security     │    │  - Task          │    │    Analyst      │
│  - Cleanup      │    │    Orchestration │    │  - Verifier     │
└─────────────────┘    └──────────────────┘    │  - Investment   │
                                               │    Advisor      │
                                               │  - Risk         │
                                               │    Assessor     │
                                               └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  Professional   │
                                               │     Tools       │
                                               │                 │
                                               │  - Document     │
                                               │    Reader       │
                                               │  - Investment   │
                                               │    Analysis     │
                                               │  - Risk         │
                                               │    Assessment   │
                                               └─────────────────┘
```

## 🔒 Security Features

- **File Type Validation**: Only PDF files accepted
- **Query Sanitization**: Input length limits and validation
- **Secure File Handling**: UUID-based naming and automatic cleanup
- **Error Handling**: Comprehensive exception management
- **Professional Disclaimers**: Appropriate legal and regulatory notices

## 📋 Supported File Formats

- **PDF**: Financial documents, reports, statements

## 🚨 Important Disclaimers

- This analysis is for informational purposes only
- Consult with qualified financial professionals before making investment decisions
- The system provides analysis based on document content and should not be considered as personalized financial advice
- All analysis results should be verified independently

## 🛠️ Development

### Project Structure
```
financial-document-analyzer-debug/
├── main.py                 # FastAPI application
├── agents.py              # CrewAI agents definition
├── task.py                # Task definitions
├── tools.py               # Tool implementations
├── requirements.txt       # Dependencies
├── README.md             # This file
└── BUGS_AND_FIXES_DOCUMENTATION.md  # Detailed bug fixes
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs` endpoint
- Review the comprehensive bug fixes documentation

---

**Built with ❤️ using CrewAI, FastAPI, and professional software engineering practices**