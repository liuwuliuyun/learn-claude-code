# Script — `04_tasks_and_concurrency.ipynb`

**Duration:** 25–30 min
**Covers:** s12 (task graph) + s13 (background tasks) + s14 (cron) + s18 (worktree isolation)

---

## Opening

> "A single-threaded agent works fine for one-shot prompts. When you want it doing *operational* work — 'run every morning,' 'spawn this 8-minute build while you keep thinking,' 'work on three features in parallel' — you need four extra mechanisms."

> "None of them touch the core loop from lesson one. They all cooperate by dropping into one new step at the top of every turn: 'drain async signals.' That's the entire trick. Watch for it as we go."

---

## Part 1 — File-backed task graph

### Cell 3 — `Task` dataclass

*[Run cells 1 and 3.]*

> "Each task is a JSON file on disk. Three fields matter. `status` — pending, in progress, completed, or failed. `blockedBy` — list of task IDs that must complete first; this is what makes it a *graph*. `owner` — who claimed it, used in lesson five for multi-agent coordination."

> "Why files instead of an in-memory dict? Persistence. The agent process can crash, restart, and pick up exactly where it was. This is also what makes lesson five's multi-agent coordination work — many agents read and write the same files."

### Cell 4 — DAG demo

*[Run cell 4.]*

> "An A → B → C chain. Watch the prints: A can start, B can't, then we complete A and the helper tells us B is newly unblocked. That's the kernel of any task scheduler in fifteen lines."

> "Question worth seeding: what about cycles? In production you'd add cycle detection. Our demo will just refuse to start the cycle — `can_start` returns False forever."

---

## Part 2 — Background tasks

### Cell 6 — `start_background_bash`

*[Run cell 6.]*

> "Three steps. The tool call returns an ID *immediately* — it doesn't block. A daemon thread does the actual work in the background. Each agent turn drains a queue and injects 'task XYZ finished, here's the output' as a user message."

> "The model treats that notification just like a new user message. It reads the result and reacts. Notice what we *didn't* do: there's no special-casing in the loop for background results. Just another message."

### Cell 7 — sleep demo

*[Run cell 7.]*

> "The demo command is a Python one-liner — `python -c 'import time; time.sleep(1); print(...)'`. The original lesson used `sleep 1 && echo` which doesn't work on Windows `cmd`. Python is portable across all three operating systems."

> "Look at the prints. Immediately after kicking off the background task, the notifications list is empty — the work hasn't finished. After we sleep one and a half seconds, the notification has landed. That's the whole point: don't block the agent, harvest results later."

---

## Part 3 — Cron scheduler

### Cell 9 — two threads plus a queue

*[Run cell 9.]*

> "Two cooperating pieces. A scheduler thread wakes once per second, checks every job's `next_fire`, and drops matches into a shared queue. A drain function gets called by the agent at the top of each turn and returns queued items as user messages."

> "We skip real cron expression parsing for brevity. Just be aware that real Claude Code uses standard five-field cron — minute, hour, day, month, day-of-week — with deterministic jitter so a thousand users don't hit `0 9 * * *` at the exact same instant."

### Cell 10 — schedule plus drain

*[Run cell 10.]*

> "Schedule a job to fire in two seconds, sleep, drain. Watch the cron message land in the queue."

> "Same trick as background tasks: turn an external event — wall clock, in this case — into a fake user message at the top of the loop. The model never knows the difference between a real human and a cron firing."

---

## Part 4 — Worktree isolation

### Cell 12 — `git worktree add`

*[Run cell 12.]*

> "`git worktree` is git's built-in solution for parallel work. It creates a separate working directory on a separate branch, all backed by the same `.git`. Real-world value: two background tasks both editing `src/foo.py` would race without worktrees. With worktrees, you pass `cwd=worktree_path` to `subprocess.run` and they're isolated."

### Cell 13 — demo

*[Run cell 13.]*

> "We create a worktree, write a file inside it, and verify the file landed in the worktree but not in the main repo. The demo uses `Path.write_text` instead of shell commands because Windows `cmd` doesn't have `pwd` or `ls`. Same idea, portable code."

> "This is the cleanest concurrency primitive I know of. Git did all the hard work. We're just orchestrating."

---

## Putting it together

### Cell 15 — the unified loop

*[Walk through cell 15.]*

> "Look at the first lines of the loop body. Drain finished notifications. Drain cron queue. Both append messages to the conversation. Then call the LLM. *That's the whole integration*. Async signals become user messages. The loop didn't need to grow."

### Cell 16 — live run

*[Run cell 16.]*

> "The prompt asks the agent to plan two dependent tasks and list them — no actual work executed. We made that intentional; running real bash in the demo makes the timing flaky. But the planning shape is real."

---

## Pause for questions

> "Questions?"

*[Likely questions:]*

> "What if two tasks need the same worktree? They serialize via the task graph — one blocks the other."

> "How does this work on Windows without `fork`? Python threads are fine; `subprocess.run` is cross-platform. No fork needed."

> "What's the failure mode if the scheduler thread dies? Silent. In production you'd add a heartbeat and a supervisor. Skip the implementation; just be aware."

---

## Transition

> "We've now got *one* agent that's robust, persistent, scheduled, and isolated. Lesson five turns that into a *team* — many agents talking to each other through inboxes, with typed protocols, plus a way to plug in tools we don't own. Open `05_multi_agent_and_integration.ipynb`."
