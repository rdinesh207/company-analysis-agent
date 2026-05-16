import asyncio
import json
import os
import re
from datetime import datetime, timezone

from openai import OpenAI
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

COMPANY_NAME = "Pulumi"
COMPANY_URL = "https://www.pulumi.com"


async def scrape(company_name: str, company_url: str) -> dict:
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@brightdata/mcp"],
        env={"API_TOKEN": os.environ["BRIGHTDATA_API_TOKEN"]},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1: Scrape company website
            print(f"[1/4] Scraping {company_url}...")
            website_result = await session.call_tool(
                "scrape_as_markdown", {"url": company_url}
            )
            website_content = _text(website_result)

            # Step 2: Parallel searches
            print("[2/4] Running searches...")
            search_result = await session.call_tool(
                "search_engine_batch",
                {
                    "queries": [
                        {"query": f"{company_name} founders CEO linkedin"},
                        {"query": f"{company_name} funding crunchbase"},
                        {"query": f"{company_name} news 2024 2025"},
                    ]
                },
            )
            print(f"  -> Raw search result: {_text(search_result)[:500]}")
            search_data = _parse_json(search_result)
            print(f"  -> Got {len(search_data)} search result sets")
            for i, rs in enumerate(search_data):
                organic = rs.get("result", {}).get("organic", [])
                print(f"  -> Query {i+1}: {len(organic)} results")
                for r in organic[:2]:
                    print(f"     {r.get('link')}")

            # Step 3: Scrape top 2 URLs per search
            print("[3/4] Scraping top results...")
            urls_to_scrape = []
            for result_set in search_data:
                for item in result_set.get("result", {}).get("organic", [])[:2]:
                    link = item.get("link", "")
                    if link and "linkedin.com" not in link:
                        urls_to_scrape.append(link)
            urls_to_scrape = urls_to_scrape[:5]

            print(f"  -> Scraping {len(urls_to_scrape)} URLs")
            pages_content = ""
            if urls_to_scrape:
                pages_result = await session.call_tool(
                    "scrape_batch", {"urls": urls_to_scrape}
                )
                pages_content = _text(pages_result)
            print(f"  -> Pages content length: {len(pages_content)} chars")

            # Step 4: Structure into JSON via Claude
            print("[4/4] Structuring data...")
            return _extract(
                company_name=company_name,
                company_url=company_url,
                website_content=website_content,
                pages_content=pages_content,
                search_data=search_data,
                urls_scraped=urls_to_scrape,
            )


def _extract(
    company_name: str,
    company_url: str,
    website_content: str,
    pages_content: str,
    search_data: list,
    urls_scraped: list[str],
) -> dict:
    sources = [
        {"url": u, "scraped_at": datetime.now(timezone.utc).isoformat()}
        for u in urls_scraped
    ]

    # Flatten search snippets as a lightweight extra source
    search_snippets = []
    for rs in search_data:
        for item in rs.get("result", {}).get("organic", [])[:5]:
            search_snippets.append(f"- {item.get('title')}: {item.get('description')}")
    snippets_text = "\n".join(search_snippets)

    prompt = f"""Extract structured company data for VC risk analysis from the scraped content below.

Company: {company_name}
Website: {company_url}

--- WEBSITE CONTENT ---
{website_content[:3000]}

--- SEARCH SNIPPETS ---
{snippets_text}

--- SCRAPED PAGES ---
{pages_content[:20000]}

Return ONLY a JSON object with this exact schema (use null for unknown fields):
{{
  "company": {{
    "name": "{company_name}",
    "website": "{company_url}",
    "description": "",
    "product": "",
    "founded": ""
  }},
  "founders": [
    {{
      "name": "",
      "role": "",
      "linkedin_url": "",
      "background": "",
      "prior_companies": []
    }}
  ],
  "funding": {{
    "total_raised": "",
    "rounds": [
      {{
        "round": "",
        "amount": "",
        "date": "",
        "investors": []
      }}
    ]
  }},
  "news": [
    {{
      "title": "",
      "url": "",
      "date": "",
      "summary": ""
    }}
  ],
  "sources": {json.dumps(sources)}
}}"""

    client = OpenAI(
        base_url=os.environ["TOKENROUTER_BASE_URL"],
        api_key=os.environ["TOKENROUTER_API_KEY"],
    )
    response = client.chat.completions.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content.strip()
    # Extract the first complete JSON object from the response
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])


def _text(result) -> str:
    if not result.content:
        return ""
    return "\n\n".join(
        c.text for c in result.content if hasattr(c, "text")
    )


def _parse_json(result) -> list:
    text = _text(result)
    if not text:
        return []
    parsed = json.loads(text)
    return parsed if isinstance(parsed, list) else [parsed]


if __name__ == "__main__":
    result = asyncio.run(scrape(COMPANY_NAME, COMPANY_URL))

    output_path = "agents/output.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nSaved to {output_path}")
    print(json.dumps(result, indent=2))
