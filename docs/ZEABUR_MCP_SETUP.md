# Zeabur MCP Setup

This project can be managed through the Zeabur MCP server so an AI coding agent can create infrastructure, deploy the backend, inspect logs, and update environment variables from an MCP-enabled client.

## Prerequisites

- A Zeabur account.
- A Zeabur API token.
- Node.js with `npx` available.
- This repository pushed to GitHub.

## Install or run the MCP server

Run the Zeabur MCP server with:

```bash
npx @zeabur/mcp-server
```

Set the required token before starting the MCP server:

```bash
ZEABUR_TOKEN=<your_zeabur_token>
```

Do not commit `ZEABUR_TOKEN` or paste it into project documentation. Store it in your MCP client, shell environment, or secret manager.

## MCP client configuration

Configure your MCP-capable AI client to launch:

```bash
npx @zeabur/mcp-server
```

with this environment variable:

```bash
ZEABUR_TOKEN=<your_zeabur_token>
```

After the MCP server is connected, the agent should operate on the backend service rooted at `backend`.

## What an AI agent can do with Zeabur MCP

An AI agent can use the Zeabur MCP server to:

- Create a Zeabur project for this repository.
- Create a backend service from the GitHub repository.
- Set the service root directory to `backend`.
- Deploy the FastAPI app using the production start command.
- Check deployment status and service logs.
- Update service environment variables without exposing secrets in Git.
- Troubleshoot failed deployments by inspecting build logs, runtime logs, health check failures, and service configuration.

## Backend deployment settings

- Framework: FastAPI.
- Entry point: `app.main:app`.
- Build command: `pip install -r requirements.txt`.
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Health check path: `/health`.
- Health check URL after deployment: `https://<your-zeabur-domain>/health`.
- Required runtime variables: Zeabur-provided `PORT`.

## Troubleshooting with MCP

When a deployment fails, ask the agent to:

1. Read the latest build logs.
2. Confirm the service root directory is `backend`.
3. Confirm dependencies installed from `requirements.txt`.
4. Confirm the start command uses `--host 0.0.0.0 --port $PORT`.
5. Check runtime logs for import errors, missing packages, or invalid environment variables.
6. Call or inspect the `/health` endpoint.
7. Update environment variables through Zeabur if a configured integration requires secrets.
