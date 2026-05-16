"""TokenRouter LLM client — OpenAI-compatible wrapper."""

from __future__ import annotations

import json
import os
import re

from openai import BadRequestError, OpenAI

DEFAULT_MODEL = "anthropic/claude-sonnet-4.6"

_FENCED_JSON_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


class LLMError(RuntimeError):
    pass


def _extract_json(content: str) -> dict:
    """Best-effort JSON extraction from a model response.

    Handles three shapes: raw JSON object, ```json … ``` fence, or
    JSON embedded in prose. Raises LLMError if nothing parses.
    """
    stripped = content.strip()

    # 1. raw JSON
    if stripped.startswith("{"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    # 2. fenced code block
    fence = _FENCED_JSON_RE.search(stripped)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass

    # 3. greedy first-{ ... last-} match
    first = stripped.find("{")
    last = stripped.rfind("}")
    if first != -1 and last > first:
        try:
            return json.loads(stripped[first : last + 1])
        except json.JSONDecodeError as exc:
            raise LLMError(f"LLM returned malformed JSON: {exc}") from exc

    raise LLMError("LLM returned no JSON content")


class TokenRouterClient:
    def __init__(self) -> None:
        base_url = os.environ.get("TOKENROUTER_BASE_URL", "").strip()
        api_key = os.environ.get("TOKENROUTER_API_KEY", "").strip()
        if not base_url:
            raise LLMError("TOKENROUTER_BASE_URL is not set")
        if not api_key:
            raise LLMError("TOKENROUTER_API_KEY is not set")
        self.model = os.environ.get("TOKENROUTER_MODEL", DEFAULT_MODEL)
        self._client = OpenAI(base_url=base_url, api_key=api_key)

    def complete_json(self, system: str, user: str) -> dict:
        """Run a chat completion expected to return a single JSON object.

        Tries `response_format=json_object` first; on providers that
        reject the parameter (some upstreams behind TokenRouter do),
        retries without it and falls back to manual JSON extraction.
        """
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
            )
        except BadRequestError:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
            )
        except Exception as exc:
            raise LLMError(f"LLM call failed: {exc}") from exc

        content = (resp.choices[0].message.content or "").strip()
        if not content:
            raise LLMError("LLM returned empty content")
        return _extract_json(content)
