## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, read_financial_document, analyze_investment_opportunities, assess_financial_risk

### Loading LLM
# Use free OpenAI model for testing
if os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Free model for testing
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
else:
    llm = None  # Will use CrewAI default LLM

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive and accurate financial analysis based on the query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with over 15 years of experience in corporate finance, "
        "investment analysis, and financial reporting. You have worked with major investment firms "
        "and have a deep understanding of financial statements, market trends, and regulatory requirements. "
        "You are known for your thorough analysis, attention to detail, and ability to identify key "
        "financial metrics that drive investment decisions. You always base your analysis on factual "
        "data and provide well-reasoned recommendations while adhering to regulatory compliance standards."
    ),
        tools=[read_financial_document] if search_tool is None else [read_financial_document, search_tool],
    llm=llm if llm else None,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Thoroughly verify and validate financial documents for accuracy, completeness, and authenticity",
    verbose=True,
    memory=True,
    backstory=(
        "You are a financial document verification expert with extensive experience in regulatory "
        "compliance and document authentication. You have worked in audit firms and regulatory "
        "bodies, specializing in verifying the authenticity and accuracy of financial reports, "
        "earnings statements, and corporate disclosures. You are meticulous in your approach, "
        "checking for consistency, proper formatting, required disclosures, and compliance with "
        "accounting standards. You have an excellent track record of identifying discrepancies "
        "and ensuring document integrity."
    ),
        tools=[read_financial_document],
    llm=llm if llm else None,
    max_iter=2,
    max_rpm=10,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisory Specialist",
    goal="Provide evidence-based investment recommendations and strategic insights based on financial analysis",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified investment advisor with CFA designation and over 12 years of experience "
        "in portfolio management and investment strategy. You have managed portfolios for high-net-worth "
        "individuals and institutional clients. Your expertise lies in fundamental analysis, risk assessment, "
        "and creating diversified investment strategies. You are known for your conservative yet effective "
        "approach to investment recommendations, always considering risk tolerance, regulatory requirements, "
        "and long-term financial goals. You strictly adhere to fiduciary standards and provide only "
        "well-researched, evidence-based advice."
    ),
        tools=[read_financial_document] if search_tool is None else [read_financial_document, search_tool],
    llm=llm if llm else None,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Management Analyst",
    goal="Conduct comprehensive risk assessment and provide risk mitigation strategies based on financial data",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in financial risk analysis, regulatory "
        "compliance, and quantitative risk modeling. You have worked in major banks and financial "
        "institutions, specializing in credit risk, market risk, and operational risk assessment. "
        "You are skilled in using various risk metrics, stress testing, and scenario analysis to "
        "evaluate potential threats to financial stability. Your approach is methodical and data-driven, "
        "focusing on identifying, measuring, and mitigating risks while ensuring compliance with "
        "risk management frameworks and regulatory guidelines."
    ),
        tools=[read_financial_document] if search_tool is None else [read_financial_document, search_tool],
    llm=llm if llm else None,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)