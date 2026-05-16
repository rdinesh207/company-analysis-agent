# BrightData Scraping Plan

## Overview
Given a company name and website URL, scrape data from multiple sources to support VC risk analysis.

## Input
```json
{
  "name": "Acme Inc",
  "url": "acme.com"
}
```

## Steps

### 1. Scrape Company Website
Use `scrape_as_markdown(url)` on the provided website.

Extracts: product description, about page, team page.

### 2. Parallel Searches
Use `search_engine_batch` with 3 queries run in parallel:

- `"<name> founders CEO linkedin"`
- `"<name> funding crunchbase"`
- `"<name> news 2024 2025"`

### 3. Scrape Top Results
Use `scrape_batch` on the **top 2 URLs** from each search (up to 6 pages total).

### 4. Structure into JSON
Normalize all scraped data into the output schema below.

## Output Schema
```json
{
  "company": {
    "name": "Acme Inc",
    "website": "acme.com",
    "description": "...",
    "product": "...",
    "founded": "..."
  },
  "founders": [
    {
      "name": "...",
      "role": "...",
      "linkedin_url": "...",
      "background": "...",
      "prior_companies": []
    }
  ],
  "funding": {
    "total_raised": "...",
    "rounds": [
      {
        "round": "Seed / Series A / ...",
        "amount": "...",
        "date": "...",
        "investors": []
      }
    ]
  },
  "news": [
    {
      "title": "...",
      "url": "...",
      "date": "...",
      "summary": "..."
    }
  ],
  "sources": [
    {
      "url": "...",
      "scraped_at": "2026-05-16T..."
    }
  ]
}
```

## Tools Used
| Tool | Purpose |
|---|---|
| `scrape_as_markdown` | Scrape the company website |
| `search_engine_batch` | Run 3 searches in parallel |
| `scrape_batch` | Scrape top 2 results per search |

## MCP Server Setup
BrightData is configured as a project-level MCP server in `.mcp.json`.
Each teammate needs to set the following environment variable:
```
BRIGHTDATA_API_TOKEN=your_api_token_here
```
See `.env.example` for reference.
