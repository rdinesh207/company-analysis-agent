# Company Analysis Agent — Final Plan

End-to-end plan for the BrightData + TokenRouter agent that backs the
`POST /api/v1/investment-analysis` endpoint and feeds the React memo UI.

This supersedes the earlier scraping-only sketch. The output schema now
matches what the FastAPI backend already promises and what the React
frontend already renders, so no extra adapter layer is needed.

---

## 1. Goals

Given a **company name** and **website URL**, return a fully populated
`CompanyAnalysisResponse` (see `backend/app/models.py`) so the frontend
can render the investment memo without further transformation.

The agent has three responsibilities:

1. **Collect** signal from the open web with BrightData MCP.
2. **Synthesize** that signal into a strict JSON memo using an LLM via
   TokenRouter (OpenAI-compatible).
3. **Validate** the LLM output against the Pydantic response model
   before returning it to the API caller.

---

## 2. Where it lives

```
agent/
  __init__.py
  pipeline.py          # orchestrates collect → synthesize → validate
  brightdata_client.py # thin wrapper over BrightData (HTTP or MCP)
  llm_client.py        # OpenAI-compatible client pointing at TokenRouter
  prompts.py           # system + user prompt templates with JSON schema
  schemas.py           # internal collection schema (raw scraped buckets)
```

`backend/app/services/investment_analysis.py` becomes a thin adapter
that calls `agent.pipeline.run(name, url)` and returns the validated
`CompanyAnalysisResponse`. No other backend file needs to change.

---

## 3. Inputs

```json
{
  "company_name": "Acme Inc",
  "company_website": "https://acme.com"
}
```

`CompanyAnalysisRequest` (already defined) enforces a non-blank name
and an `AnyHttpUrl` website.

---

## 4. Phase 1 — Collect (BrightData)

All collection happens in `agent/brightdata_client.py`. Two viable
integration modes; we pick (a):

- **(a) Direct HTTPS calls** to BrightData's public API using
  `BRIGHTDATA_API_TOKEN`. Simplest to deploy with the FastAPI process.
- **(b) MCP stdio subprocess** that spawns `npx @brightdata/mcp` and
  speaks JSON-RPC. Useful for parity with the Claude Code dev setup,
  but heavier at runtime.

### Calls (run concurrently where possible)

1. `scrape_as_markdown(company_website)` — homepage / product / about.
2. `search_engine_batch` with five queries:
   - `"<name>" founders CEO linkedin`
   - `"<name>" funding crunchbase pitchbook`
   - `"<name>" news 2024 2025`
   - `"<name>" competitors alternatives vs`
   - `"<name>" pricing customers case study`
3. `scrape_batch` on the **top 2 URLs from each search** (≤ 10 pages),
   skipping anything already scraped in step 1.

### Internal collection bucket (`schemas.py`)

```python
class RawSignal(BaseModel):
    homepage_markdown: str | None
    search_results: dict[str, list[SearchHit]]  # keyed by query intent
    scraped_pages: list[ScrapedPage]            # url, title, markdown
    scraped_at: datetime
```

Total payload is bounded — homepage + ≤ 10 short markdown pages — so
it fits comfortably in a single LLM request after truncation.

---

## 5. Phase 2 — Synthesize (TokenRouter LLM)

`agent/llm_client.py` instantiates the `openai` SDK pointed at
`TOKENROUTER_BASE_URL` with `TOKENROUTER_API_KEY`. We use
**structured outputs / JSON mode** with a schema mirrored from
`CompanyAnalysisResponse`.

### Prompt shape (`prompts.py`)

- **System:** "You are a junior VC analyst. Use only the supplied
  evidence. If a field is unknown, write 'Unknown — not found in
  sources'. Never invent investors, dates, or numbers."
- **User:** the raw `RawSignal` rendered as labeled markdown blocks,
  followed by the JSON schema and the input company/url.

### Output contract

The model must return a JSON object matching
`CompanyAnalysisResponse` exactly:

```
investment_recommendation { verdict, confidence_score, confidence_reasoning{up,down} }
company_overview          { problem, product, buyer, founded, hq, stage, raised, valuation, headcount }
market_analysis           { why_problem_matters, why_now, recent_changes_last_24_months[] }
competitor_analysis       { direct_competitors[3-5], substitutes_or_incumbents[2] }
risk_analysis             { market, competition, execution, monetization }
```

Notes for the model:
- `verdict ∈ {Bullish, Neutral, Risky, Pass}` (matches backend enum).
- `confidence_score` is `0–100` integer.
- `direct_competitors` must contain **3–5** entries; `substitutes_or_incumbents` must contain **exactly 2** entries — Pydantic will reject otherwise. Prompt enforces this and we retry once on validation failure.

---

## 6. Phase 3 — Validate & return

`agent/pipeline.py`:

```python
def run(company_name: str, company_website: str) -> CompanyAnalysisResponse:
    raw = collect(company_name, company_website)         # Phase 1
    draft = synthesize(company_name, company_website, raw)  # Phase 2 -> dict
    return CompanyAnalysisResponse(**draft)              # Phase 3 (Pydantic)
```

On `ValidationError` we retry the synth step **once** with the error
message appended to the prompt, then surface a 502 with a concise
message if it still fails. The FastAPI router maps known agent
errors (`BrightDataError`, `LLMError`, `ValidationError`) to clean
HTTP responses; everything else becomes a 500.

---

## 7. Backend wiring

- `backend/requirements.txt` gains: `openai>=1.40`, `httpx>=0.27`,
  `python-dotenv>=1.0`, `tenacity>=8.2`.
- `backend/app/services/investment_analysis.py` becomes:

  ```python
  from agent.pipeline import run as run_agent

  def build_company_analysis(company_name, company_website):
      return run_agent(company_name, company_website)
  ```

- `backend/app/main.py` loads `.env` at startup (`python-dotenv`) so
  `BRIGHTDATA_API_TOKEN` and `TOKENROUTER_*` are visible to the agent.
- Project layout: `agent/` lives at repo root next to `backend/`. The
  backend imports it with `sys.path` extension in `main.py` or by
  installing the repo as editable (`pip install -e .`). We pick the
  `sys.path` route to keep deployment simple.

---

## 8. Frontend changes

Three small fixes; all already required regardless of the agent work.

1. **Add a website URL input** next to the company name on the landing
   page. Both fields are required to submit. Light client-side URL
   sanity check (must contain a dot, prepend `https://` if missing).
2. **Fix the API contract** in `front_end/src/api.ts` and
   `front_end/src/types.ts`:
   - Endpoint: `POST /api/v1/investment-analysis` (not `/analyze`).
   - `AnalyzeRequest` gains `company_website: string`.
   - Verdict type becomes `"Bullish" | "Neutral" | "Risky" | "Pass"`
     so it matches the backend enum.
3. **Fix the vite proxy** in `front_end/vite.config.ts` to forward
   `/api/*` to the backend **without stripping `/api`**, so the new
   path resolves to `/api/v1/investment-analysis` on the FastAPI side.

No changes are needed to the memo sections — `InvestmentSection`,
`CompanyOverviewSection`, etc. already render the response model.

---

## 9. Environment

`.env` (already in `.gitignore`):

```
BRIGHTDATA_API_TOKEN=...
TOKENROUTER_BASE_URL=https://api.tokenrouter.com/v1
TOKENROUTER_API_KEY=...
# optional
TOKENROUTER_MODEL=anthropic/claude-sonnet-4.6
```

`.env.example` already lists these — no change.

---

## 10. Out of scope (deliberately)

- Caching scraped pages or memo results (add later if cost spikes).
- Background jobs / async polling — the endpoint stays synchronous for
  now; expected latency 10–30 s, which the frontend already handles
  with the "Analyzing…" state.
- Auth, rate limiting, persistence. The current frontend hits
  the backend over a dev proxy with `allow_origins=["*"]`; production
  hardening is a separate task.
