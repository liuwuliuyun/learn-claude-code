# Script — `03_memory_and_context.ipynb`

**Duration:** 25–30 min
**Covers:** s06 (subagents) + s08 (compaction) + s09 (memory) + s11 (error recovery)

---

## Opening

> "So far we've built a loop that grows linearly: every turn appends to `messages`. That works for small tasks. For real work, it explodes."

> "Context fills up. The model forgets what it knew. The API rate-limits us. A single research task can swallow the whole budget. This lesson is the four moves Claude Code uses to survive that."

> "Think of it as three escape valves on the conversation — branching out with subagents, shrinking with compaction, persisting across sessions with memory — plus a retry layer."

---

## Part 1 — Subagents

### Cell 3 — `spawn_subagent`

*[Run cells 1 and 3.]*

> "This is the cleanest example of recursion in the curriculum. A subagent is just `agent_loop` with a fresh `messages` list and a different system prompt. It runs to completion, then returns a *summary string* — not the conversation history."

> "The parent agent never sees the intermediate noise. If you're going to do thirty greps to find a function, do them in a subagent. The parent gets one tidy answer instead of thirty tool result blocks."

### Cell 4 — exposing subagent as a tool

*[Run cell 4.]*

> "Now the parent model can decide for itself when to spawn a subagent. We just registered it as another tool. This is exactly how Claude Code's `Task` tool works — same shape, more knobs in production: timeout, model selection, tool whitelist."

> "Common question: how does the subagent know what tools to use? In this demo, we hand it `[BASH_TOOL]`. In real Claude Code each subagent type has a curated tool list — an 'explore' subagent gets read-only tools, an 'editor' gets writes, and so on."

---

## Part 2 — Compaction

### Cell 7 — `approx_tokens` and the two compactors

*[Run cell 7.]*

> "Two cheap layers. `micro_compact` drops tool messages older than N turns — their content is rarely relevant later. `snip_compact` checks total tokens against a budget; if we're over, it replaces the middle of the conversation with a placeholder like `<snipped: N messages>`."

> "Real Claude Code has a third layer — an LLM call that *summarizes* the snipped middle. We skip it for time, but it's mentioned in the notebook."

> "Notice the order of cost: cheap layers run every turn, the expensive LLM-summary only when we're near the wall. This pattern — escalating layers of cost — is everywhere in production AI infra. Cheap first, expensive last."

### Cell 8 — token-drop demo

*[Run cell 8.]*

> "Look at the before-and-after token counts. That's compaction working. Don't dwell — move on."

---

## Part 3 — Memory

### Cell 10 — file-backed memory

*[Run cell 10.]*

> "Memory is not context. Context is per-conversation; memory persists across them."

> "On disk: `MEMORY.md` is a small index — just titles and one-line hooks — loaded into every system prompt. Each entry's *body* lives in its own markdown file, read on demand."

> "Notice we did this exact thing two lessons ago with skills. Index in the prompt, body on demand. It's the only way to scale knowledge without burning tokens. If you only remember one design pattern from this course, remember this one."

### Cell 11 — model picks its own memory

*[Run cell 11.]*

> "Watch this. The model sees `test_framework` in the index and calls `memory_read('test_framework')` — without us hinting which memory is relevant. The retrieval is *self-organized* by the model. The harness just makes it possible."

---

## Part 4 — Error recovery

### Cell 14 — `RecoveryState` and `call_with_recovery`

*[Run cell 14.]*

> "Three failure modes, three fixes. Rate limit error: exponential backoff, retry. BadRequestError that mentions context too long: aggressive compaction, retry. Other API errors: bounded retries, then surface."

> "The `consecutive_errors` counter is the kill-switch. Without it, you'd loop forever on a permanent failure."

> "This is what 'production' actually means in agent code: a polite retry policy and a kill-switch. Skip this and your agent dies the first time GitHub Models rate-limits you."

---

## Putting it together

### Cell 16 — full loop

*[Walk through cell 16.]*

> "Compact at the top of every turn — cheap layers only. Wrap the API call in `call_with_recovery`. `spawn_subagent` and `memory_read` are just tools the model can call. Four mechanisms, one loop, no special-casing."

### Cell 17 — live run

*[Run cell 17 if time allows.]*

> "The prompt should trigger at least one memory read. If it does, you'll see `memory_read` in the tool calls."

---

## Pause for questions

> "Questions?"

*[Likely questions:]*

> "What if the LLM summary itself is too long? Recursion — summarize the summary. In practice you cap output tokens."

> "Why is memory not just RAG? It can be. RAG is a retrieval mechanism; this design is *what to retrieve*. They compose — you can put your RAG-retrieved chunks behind the same `memory_read` interface."

> "How do you handle stale memory? Timestamp it, verify before acting. The next lesson hints at that pattern."

---

## Transition

> "We've made one agent very robust. Now: what if you want it doing *operational* work — running for hours, on a schedule, in the background, without stomping on git state? Lesson four. Open `04_tasks_and_concurrency.ipynb`."
