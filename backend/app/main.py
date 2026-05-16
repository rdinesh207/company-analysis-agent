import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError


# Make the sibling `agent/` package importable when running from /backend.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Load .env from repo root so BrightData + TokenRouter creds are visible.
# Silently no-ops if the file is missing (e.g. on Zeabur where env vars come from the platform).
load_dotenv(_REPO_ROOT / ".env", override=False)

from app.routers.analysis import router as analysis_router  # noqa: E402
from agent.brightdata_client import BrightDataError  # noqa: E402
from agent.llm_client import LLMError  # noqa: E402


app = FastAPI(
    title="AutoRep Backend",
    description="FastAPI backend for company investment analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BrightDataError)
def _brightdata_error(_: Request, exc: BrightDataError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": f"BrightData error: {exc}"})


@app.exception_handler(LLMError)
def _llm_error(_: Request, exc: LLMError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": f"LLM error: {exc}"})


@app.exception_handler(ValidationError)
def _validation_error(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=502, content={"detail": f"Model returned invalid data: {exc}"}
    )


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(analysis_router, prefix="/api/v1", tags=["Investment Analysis"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
