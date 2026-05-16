"""End-to-end company analysis pipeline.

Collect → Synthesize → Validate. Returns a `CompanyAnalysisResponse`
matching the FastAPI router contract.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from pydantic import ValidationError

from app.models import CompanyAnalysisResponse
from agent.brightdata_client import BrightDataClient, BrightDataError
from agent.llm_client import LLMError, TokenRouterClient
from agent.prompts import SYSTEM_PROMPT, build_user_prompt
from agent.schemas import RawSignal, ScrapedPage, SearchHit, SearchIntent

log = logging.getLogger("agent.pipeline")

SEARCH_QUERIES: dict[SearchIntent, str] = {
    "overview": '"{name}" company wikipedia headquarters founded',
    "founders": '"{name}" founders CEO linkedin background',
    "funding": '"{name}" funding round valuation crunchbase',
    "news": '"{name}" news announcement 2024 2025',
    "competitors": '"{name}" vs alternatives competitors',
    "customers": '"{name}" pricing customers case study',
}

TOP_RESULTS_PER_QUERY = 5
PAGES_TO_SCRAPE_PER_QUERY = 2
MAX_TOTAL_SCRAPED_PAGES = 8


async def _collect(name: str, website: str) -> RawSignal:
    async with BrightDataClient() as bd:
        homepage_task = asyncio.create_task(bd.scrape_as_markdown(website))
        queries = [tmpl.format(name=name) for tmpl in SEARCH_QUERIES.values()]
        search_task = asyncio.create_task(
            bd.search_engine_batch(queries, num_results=TOP_RESULTS_PER_QUERY)
        )

        homepage_md: str | None
        try:
            homepage_md = await homepage_task
        except BrightDataError as exc:
            log.warning("homepage scrape failed for %s: %s", website, exc)
            homepage_md = None

        search_raw = await search_task

        search_results: dict[SearchIntent, list[SearchHit]] = {}
        urls_to_scrape: list[str] = []
        seen_urls: set[str] = {website}

        for intent, tmpl in SEARCH_QUERIES.items():
            q = tmpl.format(name=name)
            hits = [SearchHit(**h) for h in search_raw.get(q, [])]
            search_results[intent] = hits
            for hit in hits[:PAGES_TO_SCRAPE_PER_QUERY]:
                if hit.url in seen_urls:
                    continue
                seen_urls.add(hit.url)
                urls_to_scrape.append(hit.url)
                if len(urls_to_scrape) >= MAX_TOTAL_SCRAPED_PAGES:
                    break
            if len(urls_to_scrape) >= MAX_TOTAL_SCRAPED_PAGES:
                break

        scraped_map = await bd.scrape_batch(urls_to_scrape)
        scraped_pages = [
            ScrapedPage(url=url, markdown=md) for url, md in scraped_map.items()
        ]

    return RawSignal(
        company_name=name,
        company_website=website,
        homepage_markdown=homepage_md,
        search_results=search_results,
        scraped_pages=scraped_pages,
        scraped_at=datetime.now(timezone.utc),
    )


def _synthesize(raw: RawSignal, retry_error: str | None = None) -> dict:
    llm = TokenRouterClient()
    return llm.complete_json(
        system=SYSTEM_PROMPT,
        user=build_user_prompt(raw, retry_error=retry_error),
    )


def _build_response(
    company_name: str, company_website: str, draft: dict
) -> CompanyAnalysisResponse:
    payload = {k: v for k, v in draft.items() if k not in {"company_name", "company_website"}}
    return CompanyAnalysisResponse(
        company_name=company_name,
        company_website=company_website,
        **payload,
    )


def run(company_name: str, company_website: str) -> CompanyAnalysisResponse:
    """Synchronous entrypoint used by the FastAPI router."""
    raw = asyncio.run(_collect(company_name, company_website))

    draft = _synthesize(raw)
    try:
        return _build_response(company_name, company_website, draft)
    except ValidationError as exc:
        draft = _synthesize(raw, retry_error=str(exc))
        return _build_response(company_name, company_website, draft)


__all__ = ["run", "BrightDataError", "LLMError"]
