"""Shared LLM client for the notebook lessons.

We use the OpenAI Python SDK pointed at the GitHub Models inference endpoint.

Authentication tries (in order):
1. Cached token from ~/.claude/gh_models_token.json
2. `gh auth token` (GitHub CLI, must be installed and authenticated)

Why this matters: the harness logic in each lesson is identical regardless of
which provider sits behind the chat completion. Centralizing the client here
keeps the lesson notebooks focused on agent mechanics, not provider setup.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

from openai import OpenAI

GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-5"
FALLBACK_MODEL = "openai/gpt-4.1"

CACHE_DIR = Path.home() / ".claude"
TOKEN_CACHE = CACHE_DIR / "gh_models_token.json"


def _load_cached_token() -> str | None:
    """Load token from cache if not expired."""
    if not TOKEN_CACHE.exists():
        return None

    try:
        data = json.loads(TOKEN_CACHE.read_text(encoding="utf-8"))
        expires_at = data.get("expires_at")
        if expires_at and datetime.now().timestamp() < expires_at:
            return data["token"]
    except Exception:
        pass

    return None


def _save_token(token: str, ttl_seconds: int = 7200) -> None:
    """Cache token with TTL-based expiration (Unix timestamp)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    expires_at = (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp()
    TOKEN_CACHE.write_text(
        json.dumps({"token": token, "expires_at": expires_at}),
        encoding="utf-8",
    )
    try:
        TOKEN_CACHE.chmod(0o600)
    except Exception:
        pass


def _get_token_from_gh_cli() -> str | None:
    """Use 'gh auth token' if GitHub CLI is installed and authenticated."""
    if not shutil.which("gh"):
        return None

    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            token = result.stdout.strip()
            if token:
                return token
    except Exception:
        pass

    return None


def _get_github_models_token() -> str:
    """Get a valid GitHub Models API token via cache or gh CLI."""
    cached = _load_cached_token()
    if cached:
        return cached

    print("Looking for authentication via 'gh' CLI...")
    gh_token = _get_token_from_gh_cli()
    if gh_token:
        print("Using token from 'gh' CLI.")
        _save_token(gh_token, ttl_seconds=3600)
        return gh_token

    raise RuntimeError(
        "No GitHub token available.\n"
        "Install GitHub CLI (https://cli.github.com/) and run 'gh auth login'."
    )


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    token = _get_github_models_token()
    return OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=token)


def chat(messages, *, model=DEFAULT_MODEL, tools=None, **kwargs):
    """Thin wrapper used by the lessons. Returns the raw OpenAI response."""
    client = get_client()
    params = {"model": model, "messages": messages}
    if tools:
        params["tools"] = tools
    params.update(kwargs)
    return client.chat.completions.create(**params)
