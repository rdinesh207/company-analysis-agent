import type { CompanyAnalysisResponse } from "./types";

export function getDemoAnalysis(
  companyName: string,
  companyWebsite: string,
): CompanyAnalysisResponse {
  return {
    company_name: companyName,
    company_website: companyWebsite,
    investment_recommendation: {
      verdict: "Neutral",
      confidence_score: 55,
      confidence_reasoning: {
        what_moves_it_up: [
          "Verified revenue growth, customer retention, and gross margin data.",
          "Confirmed funding history, valuation, and investor quality from a trusted data source.",
          "Evidence that the company is winning against direct competitors in active deals.",
        ],
        what_moves_it_down: [
          "Weak differentiation versus incumbents or fast-following competitors.",
          "Unclear willingness to pay from the target buyer.",
          "Flat or declining headcount, customer concentration, or missed execution milestones.",
        ],
      },
    },
    company_overview: {
      problem_they_solve:
        "Payments infrastructure for internet businesses — reducing friction for online commerce.",
      what_they_sell: "Payment processing APIs, billing, and financial infrastructure.",
      who_buys_it: "Developers and product teams at startups and enterprises.",
      founded: "2010",
      hq: "San Francisco, CA",
      stage: "Late stage",
      total_raised: "$8.7B+",
      last_round_valuation: "Private",
      headcount_trend_linkedin: "8,000+ employees",
    },
    market_analysis: {
      why_problem_matters:
        "Global digital payments volume continues to grow; merchants need reliable, developer-friendly infrastructure.",
      why_now:
        "AI-native products, embedded finance, and cross-border commerce increase demand for programmable payments.",
      recent_changes_last_24_months: [
        "Expansion of revenue and billing products for subscription businesses.",
        "Increased regulatory scrutiny on fintech and money movement.",
        "Competition from embedded payment modules inside vertical SaaS platforms.",
      ],
    },
    competitor_analysis: {
      direct_competitors: [
        {
          name: "Adyen",
          position: "comparable",
          rationale: "Global enterprise payment platform with similar API-first positioning.",
        },
        {
          name: "PayPal / Braintree",
          position: "stronger",
          rationale: "Larger consumer brand and merchant base in many segments.",
        },
      ],
      substitutes_or_incumbents: [
        {
          name: "Legacy merchant acquirers",
          position: "stronger",
          rationale: "Established relationships with large brick-and-mortar and enterprise buyers.",
        },
      ],
    },
    risk_analysis: {
      market_risk: "Regulatory changes and macro slowdowns can reduce payment volume growth.",
      competition_risk: "Incumbents and vertical SaaS platforms may bundle payments at lower margin.",
      execution_risk: "Scaling compliance, support, and international operations remains complex.",
      monetization_risk: "Take-rate compression as the category matures.",
    },
  };
}
