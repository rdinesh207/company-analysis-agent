from app.models import CompanyAnalysisResponse
from agent.pipeline import run as run_agent


def build_company_analysis(
    company_name: str,
    company_website: str,
) -> CompanyAnalysisResponse:
    """Run the BrightData + TokenRouter agent and return the validated memo."""
    return run_agent(
        company_name=company_name.strip(),
        company_website=company_website.strip(),
    )
