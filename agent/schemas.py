from datetime import datetime
from typing import Literal

from pydantic import BaseModel

SearchIntent = Literal[
    "overview",
    "founders",
    "funding",
    "news",
    "competitors",
    "customers",
]


class SearchHit(BaseModel):
    url: str
    title: str
    snippet: str = ""


class ScrapedPage(BaseModel):
    url: str
    title: str = ""
    markdown: str


class RawSignal(BaseModel):
    """Everything the collector gathered, fed straight to the LLM."""

    company_name: str
    company_website: str
    homepage_markdown: str | None = None
    search_results: dict[SearchIntent, list[SearchHit]] = {}
    scraped_pages: list[ScrapedPage] = []
    scraped_at: datetime
