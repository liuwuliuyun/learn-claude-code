# Script — `01_foundations.ipynb`

**Duration:** 25–30 min
**Covers:** s01 (loop) + s02 (dispatch) + s03 (permissions)

---

## Opening

> "By the end of this notebook you will have written, by hand, the core of every agent harness in production today — including Claude Code. It's about twenty lines."

> "This is the densest notebook in the course because it's where the loop is born. Lessons two through five are easier — each one adds a single mechanism on top of what we build now. So if anything feels heavy, push through; the next four notebooks ride on this one."

---

## Part 1 — The minimal loop

### Cell 3 — `run_bash` and `BASH_TOOL`

*[Run cell 1 to set up imports, then walk to cell 3.]*

> "We need a tool to give the model. The simplest one is a shell command runner. `run_bash` is a thin wrapper around `subprocess.run` — captures stdout and stderr, truncates to four kilobytes, returns a string."

> "Quick aside on Windows. On Unix, `shell=True` runs through bash. On Windows it runs through `cmd.exe`. So we compute a `SHELL_HINT` at import time and put it in the tool description. That way the model knows whether to emit `ls` or `dir`."

*[Run cell 3.]*

> "`BASH_TOOL` is the JSON the OpenAI SDK expects: a function name, a description, and a parameter schema. The model never sees our Python — it sees this dict."

### Cell 5 — `agent_loop`

> "Here's the single most important code cell in the course. I'm going to read it line by line."

*[Read cell 5 on screen.]*

> "We start with a messages list — just the user prompt. We loop up to `max_turns` times. Each iteration we call `chat.completions.create` with the current messages and the tool list. We grab the assistant message and **append it to the history**."

> "Now the branch. If `finish_reason` is anything other than `tool_calls`, the model is done — return its text. Otherwise, for each tool call, look up the handler, run it, and append a `tool` message with the result. Then loop."

> "Three points people miss. One: we have to append the assistant's tool-request message — `messages.append(msg.model_dump...)` — before the tool results. Order matters. Two: one `tool` message per `tool_call`, even when the model batches multiple calls in a turn. Three: the exit condition is `finish_reason != 'tool_calls'`, not `tool_calls is None`. Some providers return an empty array."

> "That's the agent. Twenty lines. Everything else in this course is decoration."

### Cell 6 — first run

*[Run cell 6.]*

> "Read the output with me. The model called bash twice. First call to print the working directory, second to list its contents. Then it composed a sentence describing both. We never told it 'first run X then run Y'. The loop just kept handing control back."

> "Quick question to seed: what stops the model from looping forever? `max_turns` — that's the safety net. In production you'd also bound by token count or wall clock or cost."

---

## Part 2 — Many tools, one dispatch

### Cell 9 — three tools

> "Now we add two more tools: `read_file` and `write_file`. Watch what *doesn't* change — the loop. We just register more handlers."

*[Run cell 9.]*

> "If the loop had `if name == 'bash': elif name == 'read_file':` we'd be back in 2010. The dispatch table makes this infinitely extensible. Every lesson from here adds tools and the loop stays untouched."

### Cell 11 — three-tool demo

*[Run cell 11.]*

> "The model wrote a haiku, saved it to a file, then read it back. Three tools cooperating in one task — and notice we didn't write any orchestration code. The model figured out the order itself. This is where 'agent' stops feeling abstract."

---

## Part 3 — Permissions

### Cell 13 — `check_permission`

> "Right now our loop will run any shell command the model emits. Bad idea. We add permissions in two layers."

*[Walk through cell 13.]*

> "Layer one: hard-deny patterns. If the command contains `rm -rf /` or `sudo` or anything destructive, we refuse before it touches the system. No user prompt, no override."

> "Layer two: soft rules with a per-rule reason. In real Claude Code these would prompt the user — `allow / deny` — and the user's choice flows back to the model. In this notebook we hardcode `AUTO_DECISION = 'deny'` so the demo is deterministic."

### Cell 15 — `safe_agent_loop`

*[Show cell 15.]*

> "The whole permissions system is one new `if` branch. Before dispatching a tool, run `check_permission`. If it returns `False`, append a tool message saying 'denied' with the reason, and continue. The model receives the denial just like any other tool result."

### Cell 16 — denied destruction

*[Run cell 16.]*

> "I'm explicitly asking the agent to delete every file in the repo. Watch what happens."

> "There's the `⛔ blocked` message — that's our hard-deny firing. The model receives 'I can't do that' as a tool result, reads it, and gives up gracefully. No exception, no special case in the loop. Just another tool result the model knows how to handle."

> "This is the entire UX of permission prompts in Claude Code. The denial is a *message*, not an error. The model is trained to back off when it sees one."

---

## Pause for questions

> "We're at a good stopping point. Questions before we move on?"

*[If the room is quiet, seed with these:]*

> "One question worth asking: what stops the model from calling `bash` to bypass `write_file`'s rule? Nothing. You check the *call*, not the tool name. Security in depth — every tool's handler is responsible for its own validation."

> "Another: how does Claude Code handle long-running tools? That's lesson four — background tasks."

---

## Transition

> "Right now permissions are hardcoded in the loop body. In lesson two we'll lift them out as a *hook* — and add three more user-facing mechanisms on the same hook scaffold: todo lists, skill loading, and dynamic system prompts. Open `02_extending_the_loop.ipynb`."
