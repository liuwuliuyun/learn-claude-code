"""Shared LLM client for the notebook lessons.

We use the OpenAI Python SDK pointed at Agent Maestro's local, OpenAI-compatible
endpoint. Agent Maestro (https://github.com/Joouis/agent-maestro) is a VS Code
extension that proxies VS Code's Language Model API; it auto-starts a local
server on VS Code startup.

Why this matters: the harness logic in each lesson is identical regardless of
which provider sits behind the chat completion. Centralizing the client here
keeps the lesson notebooks focused on agent mechanics, not provider setup.
"""

from __future__ import annotations

from functools import lru_cache

from openai import OpenAI

# Agent Maestro's OpenAI-compatible base URL. Default proxy port is 23333,
# override via the AGENT_MAESTRO_PROXY_PORT env var in VS Code if changed.
AGENT_MAESTRO_BASE_URL = "http://localhost:23333/api/openai/v1"

# Model IDs come from VS Code's Language Model API. List what your VS Code
# exposes via GET http://localhost:23333/api/v1/lm/chatModels.
DEFAULT_MODEL = "gpt-5.5"
FALLBACK_MODEL = "gpt-4o"

# Auth is disabled by default in Agent Maestro for local development. The SDK
# still requires a non-empty api_key, so we pass a placeholder.
PLACEHOLDER_API_KEY = "agent-maestro-local"


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(base_url=AGENT_MAESTRO_BASE_URL, api_key=PLACEHOLDER_API_KEY)


def chat(messages, *, model=DEFAULT_MODEL, tools=None, **kwargs):
    """Thin wrapper used by the lessons. Returns the raw OpenAI response."""
    client = get_client()
    params = {"model": model, "messages": messages}
    if tools:
        params["tools"] = tools
    params.update(kwargs)
    return client.chat.completions.create(**params)
