from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator


Verdict = Literal["Bullish", "Neutral", "Risky", "Pass"]
CompetitivePosition = Literal["stronger", "comparable", "weaker"]


class CompanyAnalysisRequest(BaseModel):
    company_name: str = Field(
        ...,
        min_length=1,
        max_length=120,
        examples=["Stripe"],
    )
    company_website: AnyHttpUrl = Field(
        ...,
        examples=["https://stripe.com"],
    )

    @field_validator("company_name")
    @classmethod
    def company_name_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("company_name must not be blank")
        return cleaned


class ConfidenceReasoning(BaseModel):
    what_moves_it_up: list[str]
    what_moves_it_down: list[str]


class InvestmentRecommendation(BaseModel):
    verdict: Verdict
    confidence_score: int = Field(..., ge=0, le=100)
    confidence_reasoning: ConfidenceReasoning


class CompanyOverview(BaseModel):
    problem_they_solve: str
    what_they_sell: str
    who_buys_it: str
    founded: str
    hq: str
    stage: str
    total_raised: str
    last_round_valuation: str
    headcount_trend_linkedin: str


class MarketAnalysis(BaseModel):
    why_problem_matters: str
    why_now: str
    recent_changes_last_24_months: list[str]


class Competitor(BaseModel):
    name: str
    position: CompetitivePosition
    rationale: str


class CompetitorAnalysis(BaseModel):
    direct_competitors: list[Competitor] = Field(..., min_length=3, max_length=5)
    substitutes_or_incumbents: list[Competitor] = Field(..., min_length=2, max_length=2)


class RiskAnalysis(BaseModel):
    market_risk: str
    competition_risk: str
    execution_risk: str
    monetization_risk: str


class CompanyAnalysisResponse(BaseModel):
    company_name: str
    company_website: AnyHttpUrl
    investment_recommendation: InvestmentRecommendation
    company_overview: CompanyOverview
    market_analysis: MarketAnalysis
    competitor_analysis: CompetitorAnalysis
    risk_analysis: RiskAnalysis
