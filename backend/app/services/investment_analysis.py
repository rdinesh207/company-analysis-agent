from app.models import (
    CompanyAnalysisResponse,
    CompanyOverview,
    Competitor,
    CompetitorAnalysis,
    ConfidenceReasoning,
    InvestmentRecommendation,
    MarketAnalysis,
    RiskAnalysis,
)


def build_company_analysis(
    company_name: str,
    company_website: str,
) -> CompanyAnalysisResponse:
    """Return a structured placeholder analysis for the frontend contract.

    Replace this function with a real research/LLM pipeline when data providers
    and API keys are available.
    """
    company = company_name.strip()
    website = company_website.strip()

    return CompanyAnalysisResponse(
        company_name=company,
        company_website=website,
        investment_recommendation=InvestmentRecommendation(
            verdict="Neutral",
            confidence_score=55,
            confidence_reasoning=ConfidenceReasoning(
                what_moves_it_up=[
                    "Verified revenue growth, customer retention, and gross margin data.",
                    "Confirmed funding history, valuation, and investor quality from a trusted data source.",
                    "Evidence that the company is winning against direct competitors in active deals.",
                ],
                what_moves_it_down=[
                    "Weak differentiation versus incumbents or fast-following competitors.",
                    "Unclear willingness to pay from the target buyer.",
                    "Flat or declining headcount, customer concentration, or missed execution milestones.",
                ],
            ),
        ),
        company_overview=CompanyOverview(
            problem_they_solve=(
                f"{company} appears to target an important customer pain point, "
                "but this placeholder response needs live research before making an investment decision."
            ),
            what_they_sell=(
                f"Product and packaging should be confirmed from {website}, "
                "customer materials, and third-party data providers."
            ),
            who_buys_it=(
                "Likely buyers should be validated through customer logos, case studies, "
                "job postings, reviews, and sales collateral."
            ),
            founded="Unknown - requires live company data lookup.",
            hq="Unknown - requires live company data lookup.",
            stage="Unknown - requires funding database lookup.",
            total_raised="Unknown - requires funding database lookup.",
            last_round_valuation="Unknown - requires funding database lookup.",
            headcount_trend_linkedin="Unknown - requires LinkedIn or approved headcount data source.",
        ),
        market_analysis=MarketAnalysis(
            why_problem_matters=(
                "The market importance should be evaluated by measuring budget ownership, "
                "urgency, frequency of the workflow, and cost of the current alternative."
            ),
            why_now=(
                "A reliable why-now answer requires current evidence from technology shifts, "
                "regulation, buyer behavior, and competitor movement over the last 24 months."
            ),
            recent_changes_last_24_months=[
                "Check whether new AI, automation, or data infrastructure changed product feasibility.",
                "Check whether regulation or compliance pressure increased buyer urgency.",
                "Check whether budgets shifted toward this category based on recent customer behavior.",
            ],
        ),
        competitor_analysis=CompetitorAnalysis(
            direct_competitors=[
                Competitor(
                    name="Direct competitor 1",
                    position="comparable",
                    rationale="Placeholder until market mapping is connected.",
                ),
                Competitor(
                    name="Direct competitor 2",
                    position="comparable",
                    rationale="Placeholder until market mapping is connected.",
                ),
                Competitor(
                    name="Direct competitor 3",
                    position="comparable",
                    rationale="Placeholder until market mapping is connected.",
                ),
            ],
            substitutes_or_incumbents=[
                Competitor(
                    name="Incumbent or manual workflow",
                    position="stronger",
                    rationale="Often stronger because it already owns buyer trust and budget.",
                ),
                Competitor(
                    name="Internal build",
                    position="comparable",
                    rationale="Comparable when buyers have engineering capacity and custom requirements.",
                ),
            ],
        ),
        risk_analysis=RiskAnalysis(
            market_risk="The market may be smaller, slower, or less urgent than the pitch suggests.",
            competition_risk="Competitors or incumbents may copy the core workflow or bundle it into existing platforms.",
            execution_risk="The team may struggle to scale product, sales, implementation, or customer success.",
            monetization_risk="Customers may like the product but resist paying enough for venture-scale outcomes.",
        ),
    )
