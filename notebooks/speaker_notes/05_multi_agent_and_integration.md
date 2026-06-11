# Script — `05_multi_agent_and_integration.ipynb`

**Duration:** 25–30 min
**Covers:** s15 (message bus) + s16 (protocols) + s17 (autonomous polling) + s19 (MCP plugins) + s20 (comprehensive integration)

---

## Opening

> "Lessons one through four built one capable agent. This lesson is about *many* agents cooperating, plus a way to plug in tools we don't own."

> "By the end you'll see how the full Claude Code design fits together. Every mechanism we've built is a small layer that doesn't disturb the others. This is the showcase notebook — you should leave with a clear 'I could build this' feeling."

---

## Part 1 — Message bus

### Cell 3 — JSONL inboxes

*[Run cells 1 and 3.]*

> "Each agent has an inbox file at `mailboxes/<name>.jsonl`. To send a message, append a line. To read your inbox, read the file then *delete it*. Destructive read."

> "Sounds dangerous but it's the right primitive. Once you've consumed a message, it's gone — no chance of double-processing. Real Claude Code uses the same JSONL layout with `proper-lockfile` for safe concurrent writes; the rest is identical to what you're looking at."

*[Show that the second `read_inbox` call returns an empty list.]*

> "Question worth raising: what if the agent crashes mid-read? In production you'd write to a temp file and rename atomically. Real but boring. Move on."

---

## Part 2 — Protocols

### Cell 5 — `ProtocolState` and `send_plan_approval`

*[Run cell 5.]*

> "A protocol is a typed handshake. Two ideas at once. Each request gets a `request_id`; the responder echoes it. And each request has a `type` like `plan_approval`; the response must be `plan_approval_response`. Type mismatch is rejected."

> "Why bother? Because 'approve this plan' and 'please shut down' are two different conversations and you must not let an approval get matched to a shutdown. The type check is the equivalent of a static type system for inter-agent calls."

### Cell 6 — happy path plus type mismatch

*[Run cell 6.]*

> "Two demos. The first one — happy path. Lead asks for plan approval, alice approves, lead sees 'approved', state is updated. The second — the mismatch. We respond with `shutdown_response` to a `plan_approval_request`. The framework rejects it with 'type mismatch'. That's the safety in action."

---

## Part 3 — Autonomous polling

### Cell 8 — `idle_poll`

*[Run cell 8.]*

> "Until now agents only acted when the user spoke. An *autonomous* agent goes idle and *polls* — for inbox messages, and for unclaimed tasks from lesson four's task graph. Two wake-up sources, one polling loop."

> "This is what makes a 'team' actually work. Agents look for work instead of waiting to be told."

### Cell 9 — threaded demo

*[Run cell 9.]*

> "We start an `idle_poll` in a thread, sleep for a second and a half, then create a task. Watch the print: the polling agent woke up because it claimed a task. That's a real autonomous loop in nine lines."

> "Pause and let that land. This is genuinely cool."

---

## Part 4 — MCP plugins

### Cell 11 — `MCPClient`

*[Run cell 11.]*

> "MCP — Model Context Protocol — is how Claude Code talks to *external* tool servers: search engines, ticketing systems, databases, filesystems. For teaching, our `MCPClient` is in-memory — no transport, no JSON-RPC. The harness logic is identical regardless of what's behind it."

### Cell 12 — `assemble_tool_pool`

*[Run cell 12.]*

> "Here's the crux: tool name prefixing. Each MCP tool gets named `mcp__<server>__<tool>`. Why? To prevent collision when two MCP servers both expose a `search` tool. Real Claude Code follows the same convention."

> "Look at the printed tool pool. There's the built-in `echo`, and there's `mcp__docs__search` — the prefixed external tool. We just merged two universes — your built-in tools and the MCP server's — into one flat list the model picks from. The model doesn't know or care which is which. That's the entire point of MCP."

---

## Part 5 — Putting it all together

### Cell 13 — pseudocode of the full loop

*[Walk through cell 13 line by line. Tag each line with its lesson.]*

> "This is the slide of the whole course. Read it with me."

> "Compact messages — that's lesson three. Drain finished background tasks — lesson four. Drain cron queue — lesson four. Drain inbox — lesson five, what we just built. Build the system prompt — lesson two. Wrap the API call in error recovery — lesson three. Dispatch tools through hooks — lessons one and two. And when the model says 'stop', poll for the next thing to do — lesson five."

> "Every layer is *orthogonal*. Adding the next one didn't change the previous ones. That's the whole point of the design — the harness is a stack of small, replaceable mechanisms around an unchanged core loop."

### Cell 14 — live demo

*[Run cell 14.]*

> "The agent receives a message from alice. It searches docs via MCP. Then it echoes a one-line summary. Three layers in motion in one turn. Built-in tool, MCP tool, inter-agent message. None of them special-cased in the loop."

---

## Closing

> "Let me recap the whole course in thirty seconds."

> "Lesson one: twenty-line loop, tool dispatch, permissions."
> "Lesson two: hooks, todos, skills, dynamic prompts."
> "Lesson three: subagents, compaction, memory, recovery."
> "Lesson four: tasks, background, cron, worktrees."
> "Lesson five: bus, protocols, polling, MCP."

> "Five lessons, six notebooks, about six hundred lines of Python. You now understand every mechanism Claude Code uses in production. The `s01` through `s20` files in this repo are the *full* version of each layer with edge cases — go read them when you're ready to ship something real."

### Suggested exercises

> "The notebook lists four exercises. The most ambitious is exercise four: build a real MCP client that speaks JSON-RPC over stdio, replacing our in-memory `MCPClient`. About a hundred lines, and it'll make MCP click forever. Try it."

### Final Q&A

> "Open the floor for questions."

*[Common closing questions:]*

> "How do I run this against my own data? Point at `llm_client.py`; swap models or providers there."

> "Is this Claude Code? No, it's the *shape*. Real Claude Code is much bigger; these notebooks are the load-bearing skeleton."

> "What's the smallest production-worthy version of this? Lessons one through three plus good logging. That's a real agent you could ship."

> "Thanks for coming."
