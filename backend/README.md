# AutoRep Backend

FastAPI backend for generating structured company investment analysis.

## APIs

### Health check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Investment analysis

```http
POST /api/v1/investment-analysis
```

Request:

```json
{
  "company_name": "Stripe",
  "company_website": "https://stripe.com"
}
```

The response includes:

- Investment recommendation
- Company overview
- Market analysis
- Competitor analysis
- Risk analysis

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Zeabur deployment

Use the repository root as the backend service root on Zeabur. The root
`zbpack.json` installs `backend/requirements.txt` and starts the app with:

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set frontend CORS domains later in `app/main.py` before production if needed.
