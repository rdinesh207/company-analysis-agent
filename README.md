# Company Analysis Agent

FastAPI backend plus Vite/React frontend for generating company investment memos.

## Local run

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd front_end
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. The local Vite server proxies `/api` to `http://127.0.0.1:8000`.

## Zeabur deployment

Create two services from the same GitHub repo.

### Backend service

- Root directory: repository root
- Build/runtime config: `zbpack.json`
- Health check: `/health`
- Required environment variables:

```bash
BRIGHTDATA_API_TOKEN=...
TOKENROUTER_BASE_URL=https://api.tokenrouter.com/v1
TOKENROUTER_API_KEY=...
BUTTERBASE_API_KEY=...
```

Optional:

```bash
BRIGHTDATA_UNLOCKER_ZONE=mcp_unlocker
BRIGHTDATA_SERP_ZONE=mcp_unlocker
TOKENROUTER_MODEL=anthropic/claude-sonnet-4.6
```

### Frontend service

- Root directory: `front_end`
- Build/runtime config: `front_end/zbpack.json`
- Required environment variable:

```bash
VITE_API_BASE_URL=https://YOUR_BACKEND_ZEABUR_DOMAIN/api
```

After deployment, open the frontend service URL.

## MCP setup

Bright Data MCP:

```bash
claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=YOUR_ACTUAL_TOKEN"
```

Butterbase MCP:

```bash
export BUTTERBASE_API_KEY="your_butterbase_api_key_here"
codex mcp add butterbase \
  --url https://api.butterbase.ai/mcp \
  --bearer-token-env-var BUTTERBASE_API_KEY
```
