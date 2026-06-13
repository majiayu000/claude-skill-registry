---
name: mimo-code
description: Use when delegating a coding task to mimo (the mimo CLI / Xiaomi opencode fork) — offloading implementation to mimo, resuming a mimo session, or running work on a chosen provider/model. Triggers on "/mimo-code", "run mimo", "delegate to mimo", "resume the mimo session", "offload this to mimo".
---

# mimo-code

## Overview
Delegate a write-capable coding session to `mimo`, staying the conductor. Heavy
work and tokens move to mimo; you orchestrate and review the diff.

## When to use
- The user invokes `/mimo-code [provider/model] [variant] <task>` or asks to run/resume mimo.
- A prior mimo session needs continuation (it asked something or was cut off).

## The rule that shapes everything
**Never run mimo in the main thread.** ALWAYS dispatch the `mimo-delegate` subagent
(model sonnet) so the live NDJSON stream and any blocking stay out of the main
context. You only ever receive its distilled summary.

## Parse the invocation
`/mimo-code [provider/model] [variant] <task>`
- A leading `xxx/yyy` token → model. A following `minimal|low|medium|high|max` → variant.
- The rest is the task. Natural-language requests map the same way.

## Resolve the model — ASK, do not default (only when no model was given, fresh runs only)
1. `mimo providers list` → authenticated providers. None → STOP and tell the user to run `mimo providers login`.
2. `mimo models` → catalogue; keep only models whose provider is authenticated (the intersection).
3. **Exactly one usable model** → auto-pick (asking is pointless). **More than one → ASK the user** which one (AskUserQuestion when ≤4; else print the grouped list and have them name an id).
4. **Ask effort/variant** too, offering a "default" option that omits `--variant`.

Both reads are tiny and read-only — they do NOT pollute context. Do this in the main thread before dispatching.

## Pick a handle — unique per delegation
Generate a UNIQUE slug per fresh delegation: a task-derived stem **plus a short
random suffix**, e.g. `json-logger-a1b2` (`[a-z0-9_-]`). The handle is the registry
key (`<handle>.sessionid`/`.lock`/`.ndjson`); a unique handle is what keeps parallel
or repeated runs from clashing. Record the handle you used — resume reuses THAT exact
handle, never a freshly re-derived bare slug.

## Dispatch
Dispatch `mimo-delegate` with: `handle`, `cwd` (absolute), `model`/`variant` (fresh
only), the `prompt`, and `mode: fresh`. (The subagent resolves the launcher path
itself.) Relay its summary; never echo raw NDJSON.

## Resume
Re-dispatch `mimo-delegate` with the SAME handle, `mode: resume`, and the
continuation prompt. Do NOT re-ask for a model (the session remembers it). The
launcher resumes by recorded session id — never `--continue`.

## Parallel runs
Concurrent tasks → distinct handles, one `mimo-delegate` each (dispatch in one
message to run in parallel). Concurrent **write** tasks → give each its own git
worktree under `.worktrees/` and pass it as `cwd`; the registry is safe regardless,
but two mimos editing one tree is a workspace hazard.

## Common mistakes (counters to real failures)
| Tempting move | Why it's wrong |
|---|---|
| "Asking the model is annoying — just default / omit `-m`." | The user wants to choose. Resolve the intersection and ASK (unless exactly one usable). Silent defaults are a violation, not a convenience. |
| Bare task-slug handle (`json-logger`) | Two runs of the same task collide on the lock/state. Always add a unique suffix. |
| Skipping effort selection | Offer variant (with a "default" that omits it). |
| Running mimo inline to "keep it simple" | Pollutes the main context. Always the subagent. |
| Resuming with `--continue` | Attaches to "the last session" → cross-task pollution. Resume is by recorded session id only. |
