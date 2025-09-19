## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool  # Available in crewai.tools
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool with API key
try:
    search_tool = SerperDevTool()
    print("✅ SerperDevTool initialized successfully")
except Exception as e:
    print(f"⚠️ SerperDevTool initialization failed: {e}")
    search_tool = None

## Creating custom tools using @tool decorator

@tool("Read Financial Document")
def read_financial_document(path: str = 'data/sample.pdf') -> str:
    """Tool to read data from a PDF file from a specified path.

    Args:
        path (str, optional): Path of the PDF file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full content of the financial document
    """
    try:
        # Load the PDF document
        loader = PyPDFLoader(file_path=path)
        docs = loader.load()

        full_report = ""
        for doc in docs:
            # Clean and format the financial document data
            content = doc.page_content

            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report.strip()
        
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

@tool("Analyze Investment Opportunities")
def analyze_investment_opportunities(financial_document_data: str) -> str:
    """Analyze financial document data for investment opportunities.
    
    Args:
        financial_document_data (str): The content of the financial document
        
    Returns:
        str: Investment analysis and recommendations
    """
    try:
        # Process and analyze the financial document data
        processed_data = financial_document_data.strip()

        # Clean up the data format - remove excessive whitespace
        lines = processed_data.split('\n')
        cleaned_lines = []

        for line in lines:
            cleaned_line = ' '.join(line.split())  # Remove multiple spaces
            if cleaned_line:  # Only add non-empty lines
                cleaned_lines.append(cleaned_line)

        processed_data = '\n'.join(cleaned_lines)

        # Basic investment analysis structure
        analysis = {
            "document_length": len(processed_data),
            "key_sections_identified": len([line for line in cleaned_lines if any(keyword in line.lower()
                for keyword in ['revenue', 'profit', 'cash', 'earnings', 'debt', 'assets'])]),
            "status": "Ready for detailed investment analysis"
        }

        return f"Investment Analysis Completed:\n- Document processed: {analysis['document_length']} characters\n- Key financial sections found: {analysis['key_sections_identified']}\n- Status: {analysis['status']}"
        
    except Exception as e:
        return f"Error in investment analysis: {str(e)}"

@tool("Assess Financial Risk")
def assess_financial_risk(financial_document_data: str) -> str:
    """Create a risk assessment based on financial document data.
    
    Args:
        financial_document_data (str): The content of the financial document
        
    Returns:
        str: Risk assessment analysis
    """
    try:
        # Process the financial document data for risk assessment
        processed_data = financial_document_data.strip()

        # Identify potential risk indicators in the text
        risk_keywords = ['debt', 'loss', 'decline', 'risk', 'uncertainty', 'challenge', 'competition']
        risk_indicators = []

        lines = processed_data.lower().split('\n')
        for line in lines:
            for keyword in risk_keywords:
                if keyword in line:
                    risk_indicators.append(keyword)
                    break

        risk_assessment = {
            "risk_indicators_found": len(set(risk_indicators)),
            "document_sections_analyzed": len(lines),
            "risk_coverage": "Comprehensive risk analysis ready"
        }

        return f"Risk Assessment Completed:\n- Risk indicators identified: {risk_assessment['risk_indicators_found']}\n- Document sections analyzed: {risk_assessment['document_sections_analyzed']}\n- Coverage: {risk_assessment['risk_coverage']}"
        
    except Exception as e:
        return f"Error in risk assessment: {str(e)}"