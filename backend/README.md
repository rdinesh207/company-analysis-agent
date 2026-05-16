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

## Deploying to Zeabur

This backend is ready to deploy as a Zeabur service from the `backend` directory. It includes `zbpack.json` and a Dockerfile.

### Zeabur GitHub deployment steps

1. Push the repository to GitHub.
2. Open `https://zeabur.com/new`.
3. Select the GitHub repository.
4. Create a backend service with root directory `backend`.
5. Use Python 3.11 if prompted.
6. Deploy the service.
7. Verify the health check at `https://<your-zeabur-domain>/health`.

### Build command

```bash
pip install -r requirements.txt
```

### Start command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Required environment variables

Zeabur supplies `PORT` automatically. The current backend does not require additional runtime secrets.

Optional future integration variables from the root `.env.example`:

```bash
BRIGHTDATA_API_TOKEN
TOKENROUTER_BASE_URL
TOKENROUTER_API_KEY
```

Only set optional variables when the backend code uses them. Keep real tokens in Zeabur environment variables.

### Health check URL

```text
https://<your-zeabur-domain>/health
```

Expected response:

```json
{"status":"ok"}
```

### Troubleshooting notes

- Confirm the Zeabur service root directory is `backend`.
- Confirm dependencies are installed from `requirements.txt`.
- Confirm the start command binds to `0.0.0.0` and uses `$PORT`.
- Check runtime logs for import errors or missing environment variables.
- Set frontend CORS domains in `app/main.py` before production if needed.
