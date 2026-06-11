# Script — `02_extending_the_loop.ipynb`

**Duration:** 25–30 min
**Covers:** s04 (hooks) + s05 (todo write) + s07 (skills) + s10 (system prompt assembly)

---

## Opening

> "This notebook has four parts, and they all *look* different on the surface — permissions, todo lists, skills, dynamic system prompts. But underneath they're the same shape: 'do something at point X in the loop.' Once you see the pattern, the next four mechanisms come almost for free."

> "Don't skip the part order. We do hooks first because the rest of the notebook reuses the hook registry as a mental model."

---

## Part 1 — Hooks

### Cell 3 — `HOOKS` registry

*[Run cells 1 and 3.]*

> "A hook is just a callback list keyed by event name. We define two events: `PreToolUse`, fires before a tool runs and can block it; `PostToolUse`, fires after and can transform the output. In real Claude Code there are about a dozen events — same shape."

### Cell 4 — three hooks

*[Run cell 4.]*

> "Three hooks at once. First, `logging_hook` — observability with one line of code. Every tool call now prints itself."

> "Second, `permission_hook` — last lesson's hardcoded permission check, lifted out as a hook. Same logic, different home."

> "Third, `truncate_hook` — runs after the tool, replaces output longer than 1500 chars with a snippet plus a count. Notice how clean this is: cap output size without touching tool implementations."

> "The big idea: hooks are userland. Anyone — anyone in the audience — can register one. Plugins, telemetry, content filters, custom permissioning — all the same shape."

### Cell 6 — `run_tool_with_hooks`

*[Show cell 6.]*

> "Look at this. The whole permission system from lesson one is now five lines. `fire_pre` returns either `None` (proceed) or a string (block, with this string as the tool result). The model sees a denial just like any other tool message."

> "That's lesson one's permission flow, but generalized. Any logic — not just permissions — can intercept tool calls."

---

## Part 2 — TodoWrite

### Cell 8 — `TODOS` and the `todo_write` tool

*[Run cell 8.]*

> "TodoWrite is interesting because it's the model managing its own state. We give it a tool that overwrites a list. The model uses that tool to plan, then to mark items done as it works."

> "Two things to note. First, the todos aren't *our* state — they're the model's. We just expose a tool. Second, the visible todo list keeps the model honest on multi-step tasks; it forces planning before execution."

> "Look at the parameter schema in the tool. We don't tell the model how to format todos in prose — the JSON schema does that. The schema is the prompt."

---

## Part 3 — Skills

### Cell 10 — skill registry

*[Run cell 10.]*

> "Skills are how Claude Code packages reusable how-to knowledge. Each skill has a *description* — one short line — and a *body* — the full instructions. The descriptions go into every system prompt. The bodies are loaded only when the model asks via `load_skill`."

> "Why two-stage? Token budget. If you put fifty skill bodies in every prompt, you'd burn 30,000 tokens before the user said anything. So descriptions in the prompt are cheap, bodies are opt-in."

> "This is the cheapest tool you'll ever build with the highest leverage. You add a new behavior by writing a markdown file. In real Claude Code these live as `SKILL.md` files in `~/.claude/skills/` and get read at startup."

---

## Part 4 — System prompt assembly

### Cell 12 — `get_system_prompt` with caching

*[Run cell 12.]*

> "The system prompt isn't a static string anymore — we rebuild it every turn because `cwd` might change, todos change, memory changes."

> "But each *piece* is cached separately, so we don't re-hash unchanged sections. This matters for prompt-caching APIs — Anthropic's prompt cache, OpenAI's prefix cache. Stable prefixes get reused, unstable ones don't."

> "Don't get lost in the cache mechanics. The point is: dynamic system prompt, but assembled from cached pieces."

---

## Putting it together

### Cell 14 — the unified loop

*[Walk through cell 14.]*

> "Look at the loop. System prompt assembled at the top of each turn — that's part four. Hooks fire around tool calls — part one. The `rounds_since_todo` counter — part two. `load_skill` is just another tool in the dispatch table — part three."

> "The only genuinely new piece is `rounds_since_todo`. If the model goes three rounds without touching todos, the harness injects a reminder message. This is a tiny example of harness-level nudges — the harness, not the model, decides to re-poke."

### Cell 15 — live demo

*[Run cell 15.]*

> "Read the printed `→ tool:` lines. That's the logging hook from part one doing its job. We're seeing every tool call labeled and traced — for free, because we registered one callback."

---

## Pause for questions

> "Questions before we move on?"

*[Likely questions:]*

> "Can hooks read each other's state? Yes — they're plain Python functions. Share globals if you want."

> "Can a `PostToolUse` hook block? In our implementation, no — it only transforms. The registry shape allows it; we just chose to keep it simple."

> "How does the system prompt cache key work? Hash of the section name plus content. Cheap."

---

## Transition

> "We've made the loop richer. But we haven't talked about *memory*. What happens when the conversation gets too long? What if the model loses an answer it knew two turns ago? What if a research task needs 30 tool calls — do we really want all that noise in the main conversation? Lesson three. Open `03_memory_and_context.ipynb`."
