from fastapi import APIRouter

from app.models import CompanyAnalysisRequest, CompanyAnalysisResponse
from app.services.investment_analysis import build_company_analysis


router = APIRouter()


@router.post("/investment-analysis", response_model=CompanyAnalysisResponse)
def investment_analysis(request: CompanyAnalysisRequest) -> CompanyAnalysisResponse:
    return build_company_analysis(
        company_name=request.company_name,
        company_website=str(request.company_website),
    )
