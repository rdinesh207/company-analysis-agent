"""BrightData client — direct HTTPS against the Unlocker + SERP zones.

Mirrors what `@brightdata/mcp` does internally. We call BrightData's
unified `/request` endpoint with the zone configured in the user's
BrightData dashboard. Defaults match the trial zones BrightData creates
for new accounts (`web_unlocker1`, `serp_api1`); override via env if
your account uses different names.
"""

from __future__ import annotations

import asyncio
import logging
import os
import urllib.parse
from dataclasses import dataclass

import httpx
from html2text import HTML2Text

BRIGHTDATA_URL = "https://api.brightdata.com/request"
# `mcp_unlocker` is the default zone the @brightdata/mcp package
# provisions. It handles both raw page scrapes and Google SERP requests
# (via ?brd_json=1), so we use it for both unless the user overrides.
DEFAULT_UNLOCKER_ZONE = "mcp_unlocker"
DEFAULT_SERP_ZONE = "mcp_unlocker"
REQUEST_TIMEOUT = 45.0

log = logging.getLogger("agent.brightdata")


class BrightDataError(RuntimeError):
    pass


@dataclass
class BrightDataConfig:
    api_token: str
    unlocker_zone: str = DEFAULT_UNLOCKER_ZONE
    serp_zone: str = DEFAULT_SERP_ZONE

    @classmethod
    def from_env(cls) -> "BrightDataConfig":
        token = os.environ.get("BRIGHTDATA_API_TOKEN", "").strip()
        if not token:
            raise BrightDataError("BRIGHTDATA_API_TOKEN is not set")
        return cls(
            api_token=token,
            unlocker_zone=os.environ.get(
                "BRIGHTDATA_UNLOCKER_ZONE", DEFAULT_UNLOCKER_ZONE
            ),
            serp_zone=os.environ.get("BRIGHTDATA_SERP_ZONE", DEFAULT_SERP_ZONE),
        )


def _html_to_markdown(html: str) -> str:
    converter = HTML2Text()
    converter.ignore_images = True
    converter.ignore_emphasis = False
    converter.body_width = 0
    return converter.handle(html).strip()


class BrightDataClient:
    def __init__(self, config: BrightDataConfig | None = None):
        self.config = config or BrightDataConfig.from_env()
        self._client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            headers={
                "Authorization": f"Bearer {self.config.api_token}",
                "Content-Type": "application/json",
            },
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "BrightDataClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def _post(self, zone: str, url: str) -> str:
        try:
            resp = await self._client.post(
                BRIGHTDATA_URL,
                json={"zone": zone, "url": url, "format": "raw"},
            )
        except httpx.HTTPError as exc:
            raise BrightDataError(f"BrightData request failed: {exc}") from exc

        if resp.status_code >= 400:
            raise BrightDataError(
                f"BrightData {resp.status_code} for {url}: {resp.text[:200]}"
            )
        return resp.text

    async def scrape_as_markdown(self, url: str) -> str:
        html = await self._post(self.config.unlocker_zone, url)
        return _html_to_markdown(html)

    async def scrape_batch(self, urls: list[str]) -> dict[str, str]:
        """Scrape multiple URLs concurrently. Returns {url: markdown}."""
        if not urls:
            return {}

        async def one(u: str) -> tuple[str, str | None]:
            try:
                return u, await self.scrape_as_markdown(u)
            except BrightDataError as exc:
                log.warning("scrape failed for %s: %s", u, exc)
                return u, None

        results = await asyncio.gather(*(one(u) for u in urls))
        return {u: md for u, md in results if md is not None}

    async def search_engine(self, query: str, num_results: int = 5) -> list[dict]:
        """Run a Google search via BrightData SERP, return parsed JSON hits."""
        q = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q}&num={num_results}&brd_json=1"
        try:
            raw = await self._post(self.config.serp_zone, url)
        except BrightDataError as exc:
            log.warning("search failed for %r: %s", query, exc)
            return []

        try:
            import json

            payload = json.loads(raw)
        except ValueError:
            log.warning("search returned non-JSON for %r", query)
            return []

        organic = payload.get("organic") or payload.get("results") or []
        hits: list[dict] = []
        for item in organic[:num_results]:
            link = item.get("link") or item.get("url")
            if not link:
                continue
            hits.append(
                {
                    "url": link,
                    "title": item.get("title", ""),
                    "snippet": (
                        item.get("description")
                        or item.get("snippet")
                        or item.get("text")
                        or ""
                    ),
                }
            )
        return hits

    async def search_engine_batch(
        self, queries: list[str], num_results: int = 5
    ) -> dict[str, list[dict]]:
        results = await asyncio.gather(
            *(self.search_engine(q, num_results) for q in queries)
        )
        return dict(zip(queries, results))
