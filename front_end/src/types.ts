export type Verdict = "Bullish" | "Neutral" | "Risky" | "Pass" | string;

export type CompetitorPosition = "stronger" | "comparable" | "weaker" | string;

export interface AnalyzeRequest {
  company_name: string;
  company_website: string;
}

export interface ConfidenceReasoning {
  what_moves_it_up: string[];
  what_moves_it_down: string[];
}

export interface InvestmentRecommendation {
  verdict: Verdict;
  confidence_score: number;
  confidence_reasoning: ConfidenceReasoning;
}

export interface CompanyOverview {
  problem_they_solve: string;
  what_they_sell: string;
  who_buys_it: string;
  founded: string;
  hq: string;
  stage: string;
  total_raised: string;
  last_round_valuation: string;
  headcount_trend_linkedin: string;
}

export interface MarketAnalysis {
  why_problem_matters: string;
  why_now: string;
  recent_changes_last_24_months: string[];
}

export interface CompetitorEntry {
  name: string;
  position: CompetitorPosition;
  rationale: string;
}

export interface CompetitorAnalysis {
  direct_competitors: CompetitorEntry[];
  substitutes_or_incumbents: CompetitorEntry[];
}

export interface RiskAnalysis {
  market_risk: string;
  competition_risk: string;
  execution_risk: string;
  monetization_risk: string;
}

export interface CompanyAnalysisResponse {
  company_name: string;
  company_website?: string;
  investment_recommendation: InvestmentRecommendation;
  company_overview: CompanyOverview;
  market_analysis: MarketAnalysis;
  competitor_analysis: CompetitorAnalysis;
  risk_analysis: RiskAnalysis;
}

export type MemoSectionId =
  | "investment"
  | "company"
  | "market"
  | "competitors"
  | "risk"
  | "founder-questions";

export interface MemoCard {
  id: MemoSectionId;
  label: string;
}
