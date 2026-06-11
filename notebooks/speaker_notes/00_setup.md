# Script — `00_setup.ipynb`

**Duration:** 5–10 min

---

## Opening

*[Open the notebook on the projector. Have a terminal handy in case `gh` isn't installed.]*

> "Welcome. Over the next two and a half hours we're going to build a Claude-Code-style agent harness from scratch in five short notebooks. Before we start, we need to make sure everyone's environment can call an LLM. That's all this setup notebook does — confirm the pipe works."

> "We're using OpenAI's SDK pointed at GitHub Models, not the Anthropic SDK. That's a deliberate choice: nothing in this course is provider-specific, and GitHub Models gives every one of you a free, no-credit-card path to a working model. If you want to switch to the real Anthropic SDK at home, only the file `llm_client.py` changes."

## Cell 2 — pip install

*[Run cell 2. If pre-installed, this is a no-op.]*

> "Two packages: `openai` for the SDK, and `python-dotenv` for env loading. If you're on a shared kernel this is already done."

## Cell 4 — authentication

> "This is the cell that fails most often, so let me set expectations before I run it. We authenticate exclusively through GitHub CLI — no personal access tokens. Some organizations ban PATs, so we removed that path. If you've ever run `gh auth login` on this machine, this cell is silent. If not, expect a one-time browser prompt."

*[Run cell 4.]*

> "If you got 'Auth OK' with a masked token, you're done. If you got an error, raise your hand — there are three failure modes."

> "One: `gh` isn't installed. Install GitHub CLI from cli.github.com and re-run the cell."

> "Two: stale module cache from a previous failed run. Restart the kernel and re-run."

> "Three: corporate proxy is blocking `models.github.ai`. We can't fix that in the room — pair with a neighbor for the rest of the session."

> "Once you have a token, it's cached at `~/.claude/gh_models_token.json` for an hour. So even if you restart the kernel, you won't hit the gh CLI a second time."

## Cell 6 — hello world

*[Run cell 6.]*

> "Five-word greeting. The SDK works, the endpoint works, your token works. If you got an error here, it's almost certainly a 401 — your token expired. Delete the cache file and re-run."

## Cell 9 — the tool-call protocol

> "Now we're at the most important moment in the whole course. Slow down with me here."

> "Everything in lessons one through five is built on tool calling. The shape is exactly the same in every notebook — and it's exactly four messages."

*[Walk to the whiteboard or annotate on screen.]*

> "First message: user. We send the prompt plus a list of tool definitions. Second message: assistant, with `finish_reason: tool_calls`. The model didn't answer — it asked us to run a function. Third message: tool, one per tool call, with the result. Fourth message: assistant again, this time with the actual answer."

*[Run cell 9.]*

> "Look at the printout. `finish_reason` is `tool_calls`, and `tool_calls` is a list with one entry asking for `get_weather` with city Tokyo. We have not gotten an answer yet."

## Cell 11 — completing the round trip

*[Run cell 11.]*

> "There's the answer. Notice what we just did: we appended the assistant's tool-request message verbatim, then appended a tool-result message for each call, then re-sent the entire conversation. The model used the result to write the final reply."

> "Two things people miss here. One: the assistant's tool-call message has to be appended *before* the tool result — order matters. Two: `finish_reason` is your loop signal. `tool_calls` means keep going. `stop` means done."

## Closing

> "That's it. If your hello-tool cell printed a temperature sentence, you have everything you need. Open `01_foundations.ipynb` and we'll wrap that four-message dance in a `while` loop — that's the whole agent."
