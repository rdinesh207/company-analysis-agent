# company-analysis-agent

FastAPI backend and Vite frontend for company investment analysis.

## Backend

- Framework: FastAPI
- Backend root: `backend`
- Entry point: `app.main:app`
- Health check: `GET /health`
- API docs locally or after deployment: `/docs`

## Bright Data MCP

```bash
claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=YOUR_ACTUAL_TOKEN"
```

Do not commit real MCP or API tokens.

## Deploying to Zeabur

The deployable backend service lives in `backend`. Point Zeabur at that directory when creating the service.

### Deploy from zeabur.com/new

1. Push this repository to GitHub.
2. Open `https://zeabur.com/new`.
3. Choose GitHub and select this repository.
4. Create a service for the backend.
5. Set the root directory to `backend`.
6. Use Python 3.11 if prompted.
7. Deploy the service.
8. Open `https://<your-zeabur-domain>/health` and confirm it returns `{"status":"ok"}`.

### Build command

```bash
pip install -r requirements.txt
```

### Start command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The backend also includes `backend/zbpack.json` and `backend/Dockerfile` with the same production start behavior.

### Required environment variables

Zeabur provides this automatically:

```bash
PORT
```

Optional future integration variables listed in `.env.example`:

```bash
BRIGHTDATA_API_TOKEN
TOKENROUTER_BASE_URL
TOKENROUTER_API_KEY
```

Only set optional secrets when the backend code is updated to use them. Store real values in Zeabur environment variables, not in Git.

### Health check URL

```text
https://<your-zeabur-domain>/health
```

Expected response:

```json
{"status":"ok"}
```

### Troubleshooting

- If imports fail, confirm the Zeabur service root directory is `backend`.
- If the service starts but is unreachable, confirm the start command uses `--host 0.0.0.0 --port $PORT`.
- If dependency installation fails, confirm Zeabur is reading `backend/requirements.txt`.
- If health checks fail, inspect runtime logs and call `/health`.
- If secrets are needed later, add them through Zeabur environment variables and redeploy.

## Zeabur MCP workflow

See `docs/ZEABUR_MCP_SETUP.md` for Zeabur MCP setup with:

```bash
npx @zeabur/mcp-server
```

Set `ZEABUR_TOKEN=<your_zeabur_token>` in your MCP client environment. An AI agent can then create the project and service, deploy this backend, check logs, update environment variables, and troubleshoot failed deployments through Zeabur MCP.
