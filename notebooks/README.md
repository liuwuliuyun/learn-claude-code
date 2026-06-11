# Notebook lessons — Claude Code harness, in 5 steps

These six Jupyter notebooks consolidate the 20 progressive sessions in this repo into a 5-lesson, hands-on curriculum. They use the **OpenAI SDK pointed at the GitHub Models endpoint**, authenticated via GitHub CLI — no Anthropic key needed. They run on Windows, macOS, and Linux.

The original `s01_*` through `s20_*` Python files are unchanged and remain the reference implementation; these notebooks are a guided tour through the same ideas.

## Files

| File | Covers source sessions | What you'll learn |
|---|---|---|
| `00_setup.ipynb` | — | Install deps, configure `GITHUB_TOKEN`, prove the API works |
| `01_foundations.ipynb` | s01, s02, s03 | Agent loop, tool dispatch, permissions |
| `02_extending_the_loop.ipynb` | s04, s05, s07, s10 | Hooks, TodoWrite, skills, dynamic system prompt |
| `03_memory_and_context.ipynb` | s06, s08, s09, s11 | Subagents, compaction, persistent memory, error recovery |
| `04_tasks_and_concurrency.ipynb` | s12, s13, s14, s18 | Task graph, background threads, cron, git worktrees |
| `05_multi_agent_and_integration.ipynb` | s15, s16, s17, s19, s20 | Message bus, protocols, autonomous polling, MCP, full stack |

`llm_client.py` holds the shared `get_client()` factory — every lesson imports it.

## Quick start

```bash
# From the repo root
pip install -r requirements.txt openai jupyter
jupyter lab notebooks/
```

Open `00_setup.ipynb` and run every cell top-to-bottom. You'll be prompted to authorize via GitHub on first run. After that, do the lessons in order — each one builds on the previous.

## Platform support

The lessons run on **Windows, macOS, and Linux**. The `bash` tool dispatches via `subprocess.run(..., shell=True)`, which on Windows targets `cmd.exe` — so the tool description is built dynamically and tells the model which shell it's targeting (e.g. `dir` instead of `ls`). Demos that previously used `sleep`/`pwd`/`ls` literally have been rewritten in portable Python.

If you'd rather always run a real bash, install [Git Bash](https://gitforwindows.org/) and launch Jupyter from inside it.

## Authentication

The notebooks use [GitHub CLI](https://cli.github.com/) for auth.

### Setup
```bash
gh auth login    # one-time setup
```

### Auth flow
1. **Cached token**: if a valid token exists at `~/.claude/gh_models_token.json`, it's reused.
2. **GitHub CLI**: otherwise, `gh auth token` is invoked and the result is cached for 1 hour.

The cache file is written with `chmod 0o600`. `gh` handles its own token refresh, so subsequent cache misses just re-fetch from `gh`.

## Why GitHub Models?

The mechanisms taught in these notebooks (loop shape, tool dispatch, hooks, memory, subagents, etc.) are **provider-independent** — they're harness engineering, not prompt engineering. Using GitHub Models lets you run every lesson locally with **GitHub CLI auth** (no static credentials).

If you want to swap in the real Anthropic SDK, only `llm_client.py` and the request-shape details need to change.
