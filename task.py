## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_financial_document

## Creating a task to analyze financial documents
analyze_financial_document = Task(
    description="""Conduct a comprehensive analysis of the financial document based on the user's query: {query}.
    
    Your analysis should include:
    1. Extract and summarize key financial metrics (revenue, profit, cash flow, debt, assets)
    2. Identify significant trends and changes from previous periods
    3. Evaluate the company's financial health and performance
    4. Highlight any notable financial risks or opportunities
    5. Provide context on market conditions affecting the company
    
    Base your analysis strictly on the financial document content and verified market data.
    Ensure all recommendations are evidence-based and professionally sound.""",

    expected_output="""A comprehensive financial analysis report containing:
    - Executive Summary of key findings
    - Financial Performance Metrics with period-over-period comparisons
    - Key Trends and Changes identified in the financial data
    - Financial Health Assessment including liquidity, profitability, and solvency
    - Risk Factors and Growth Opportunities
    - Market Context and industry positioning
    - Evidence-based conclusions and recommendations
    
    All analysis must be factual, well-structured, and based on the actual document content.""",

    agent=financial_analyst,
    tools=[read_financial_document, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""Analyze the financial document to provide professional investment insights based on the query: {query}.
    
    Focus on:
    1. Evaluation of financial ratios and key performance indicators
    2. Assessment of revenue growth trends and sustainability
    3. Analysis of profit margins and operational efficiency
    4. Review of cash flow patterns and liquidity position
    5. Evaluation of debt levels and capital structure
    6. Competitive positioning and market share analysis
    
    Provide evidence-based investment recommendations with appropriate risk disclaimers.""",

    expected_output="""Professional investment analysis including:
    - Financial Ratio Analysis (P/E, ROE, ROA, Debt-to-Equity, etc.)
    - Revenue and Growth Trend Analysis
    - Profitability and Margin Assessment
    - Cash Flow and Liquidity Evaluation
    - Capital Structure Analysis
    - Competitive Position Assessment
    - Investment Recommendation with risk considerations
    - Supporting rationale based on financial metrics
    
    Include appropriate disclaimers about investment risks and the need for professional advice.""",

    agent=investment_advisor,
    # tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""Conduct a thorough risk assessment of the company based on the financial document and user query: {query}.
    
    Analyze:
    1. Financial risks (liquidity, credit, market, operational)
    2. Business model sustainability and competitive threats
    3. Regulatory and compliance risks
    4. Macroeconomic factors affecting the business
    5. Industry-specific risks and challenges
    6. Management and governance considerations
    
    Provide a balanced risk profile with mitigation strategies.""",

    expected_output="""Comprehensive risk assessment report featuring:
    - Executive Risk Summary with overall risk rating
    - Financial Risk Analysis (credit, liquidity, market risks)
    - Operational Risk Factors
    - Industry and Competitive Risk Assessment
    - Regulatory and Compliance Risk Evaluation
    - Macroeconomic Risk Considerations
    - Risk Mitigation Strategies and Recommendations
    - Risk Matrix or Scoring Framework
    
    Provide actionable insights for risk management and monitoring.""",

    agent=risk_assessor,
    tools=[read_financial_document, search_tool],
    async_execution=False,
)
    
## Creating a document verification task
verification = Task(
    description="""Verify the authenticity, completeness, and accuracy of the uploaded financial document.
    
    Verification checklist:
    1. Document format and structure validation
    2. Required financial statement components presence
    3. Data consistency across different sections
    4. Proper financial reporting standards compliance
    5. Footnote and disclosure completeness
    6. Signature and authorization verification (if applicable)
    
    Flag any inconsistencies or missing required elements.""",

    expected_output="""Document verification report containing:
    - Document Authentication Status
    - Completeness Assessment (required sections present)
    - Data Consistency Verification
    - Compliance Standards Check
    - Identified Issues or Discrepancies (if any)
    - Overall Document Reliability Score
    - Recommendations for additional verification if needed
    
    Provide clear pass/fail status with detailed explanations for any concerns.""",

    agent=verifier,
    tools=[read_financial_document],
    async_execution=False
)