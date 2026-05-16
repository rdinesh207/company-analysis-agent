"""Prompt construction for the synthesis step."""

from __future__ import annotations

import json

from agent.schemas import RawSignal

MAX_PAGE_CHARS = 6000
MAX_HOMEPAGE_CHARS = 8000

SYSTEM_PROMPT = """You are a careful junior VC analyst writing a one-page
investment memo.

You will be given (a) the company name and website, (b) homepage markdown
from the live website (may be empty if the scrape failed), (c) Google
search results with snippets, and (d) a small set of full-text scraped
pages from the top search results.

How to use the evidence — strict order:

1) Prefer the live evidence above (homepage, scraped pages, search
   snippets). Quote it implicitly when possible.

2) When the live evidence is silent on a field that has a well-known,
   widely-reported public answer about THIS specific company (founders,
   HQ city, founding year, stage, recent funding round, headcount band,
   what the product does, who the buyer is), you MAY fill it in from
   public knowledge. Be specific and confident — do not hedge.

3) Only when you genuinely do not know AND the evidence does not show it,
   write a short reasoned sentence describing what would need to be
   verified, e.g. "Likely Series A–B based on public coverage; exact
   round details not in sources." Do not write the literal phrase
   "Unknown — not found in sources" anywhere in the output.

NEVER invent specific dollar amounts, dates, valuations, investor names,
employee counts, or quotes you cannot defend. If you state a number,
either it appears in the evidence or it is a widely-reported public fact
about this company.

Enum constraints (failing these will be rejected):
- investment_recommendation.verdict ∈ {"Bullish", "Neutral", "Risky", "Pass"}
- investment_recommendation.confidence_score is an integer 0–100
- competitor_analysis.direct_competitors has 3, 4, or 5 entries
- competitor_analysis.substitutes_or_incumbents has exactly 2 entries
- every competitor.position ∈ {"stronger", "comparable", "weaker"}

OUTPUT FORMAT — STRICT:
Reply with a single raw JSON object only. No code fences. No markdown.
No "Here is the JSON" preface. No commentary after. Your entire reply
must start with "{" and end with "}".
"""

OUTPUT_SCHEMA_HINT = """JSON shape (all fields required):
{
  "investment_recommendation": {
    "verdict": "Bullish|Neutral|Risky|Pass",
    "confidence_score": 0-100,
    "confidence_reasoning": {
      "what_moves_it_up": [string, ...],
      "what_moves_it_down": [string, ...]
    }
  },
  "company_overview": {
    "problem_they_solve": "one or two sentences, concrete",
    "what_they_sell": "the product / packaging in one sentence",
    "who_buys_it": "named buyer persona / segment",
    "founded": "year, e.g. '2022' — or a reasoned estimate",
    "hq": "city, region — or a reasoned estimate",
    "stage": "e.g. 'Seed', 'Series A', 'Series B', 'Growth'",
    "total_raised": "e.g. '$60M' — or a reasoned range from public coverage",
    "last_round_valuation": "e.g. '$2.5B (2024)' — or 'not publicly disclosed'",
    "headcount_trend_linkedin": "band + direction, e.g. '~150 employees, growing'"
  },
  "market_analysis": {
    "why_problem_matters": string,
    "why_now": string,
    "recent_changes_last_24_months": [string, ...]
  },
  "competitor_analysis": {
    "direct_competitors": [
      {"name": string, "position": "stronger|comparable|weaker", "rationale": string},
      ... (3 to 5 entries total)
    ],
    "substitutes_or_incumbents": [
      {"name": string, "position": "stronger|comparable|weaker", "rationale": string},
      {"name": string, "position": "stronger|comparable|weaker", "rationale": string}
    ]
  },
  "risk_analysis": {
    "market_risk": string,
    "competition_risk": string,
    "execution_risk": string,
    "monetization_risk": string
  }
}
"""


def _truncate(text: str | None, limit: int) -> str:
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n…[truncated]"


def build_user_prompt(raw: RawSignal, retry_error: str | None = None) -> str:
    parts: list[str] = [
        f"COMPANY: {raw.company_name}",
        f"WEBSITE: {raw.company_website}",
        "",
        "--- HOMEPAGE (markdown) ---",
        _truncate(raw.homepage_markdown, MAX_HOMEPAGE_CHARS)
        or "(homepage scrape unavailable — rely on search results and public knowledge)",
        "",
        "--- SEARCH RESULTS ---",
    ]

    for intent, hits in raw.search_results.items():
        parts.append(f"\n[{intent}]")
        if not hits:
            parts.append("(no results)")
            continue
        for h in hits:
            parts.append(f"- {h.title} :: {h.url}\n  {h.snippet}")

    parts.append("\n--- SCRAPED PAGES ---")
    if not raw.scraped_pages:
        parts.append("(none)")
    else:
        for page in raw.scraped_pages:
            parts.append(f"\n### {page.title or page.url}")
            parts.append(f"URL: {page.url}")
            parts.append(_truncate(page.markdown, MAX_PAGE_CHARS))

    parts.append("\n--- OUTPUT INSTRUCTIONS ---")
    parts.append(OUTPUT_SCHEMA_HINT)

    if retry_error:
        parts.append("\nThe previous attempt failed validation with:")
        parts.append(retry_error)
        parts.append("Fix the issue and return valid JSON only.")

    return "\n".join(parts)


def dump_for_debug(raw: RawSignal) -> str:
    return json.dumps(raw.model_dump(mode="json"), indent=2, default=str)
