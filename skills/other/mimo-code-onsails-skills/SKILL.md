---
name: mimo-code
description: Use when delegating a coding task to mimo (the mimo CLI / Xiaomi opencode fork) — offloading implementation to mimo, resuming a mimo session, or running work on a chosen provider/model. Triggers on "/mimo-code", "run mimo", "delegate to mimo", "resume the mimo session", "offload this to mimo".
argument-hint: "[<provider/model>] [variant] [task | resume]"
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
Raw slash-command arguments: `$ARGUMENTS`

Interpret as `[provider/model] [variant] <task>` (empty when triggered by description match rather than `/mimo-code` — then read intent from the user's message):
- A leading `xxx/yyy` token → model. A following `minimal|low|medium|high|max` → variant.
- The rest is the task; `resume`/`continue` → resume the recorded session (see Resume). Natural-language requests map the same way.

## Resolve the model — ASK, do not default (only when no model was given, fresh runs only)
1. **Gather options via the `mimo-resolve` subagent** (model sonnet). It runs the
   `resolve-models` launcher and returns the authenticated provider∩model `options`
   and `variants` — keeping the catalogue output out of the conductor's context.
   Empty options (no authenticated provider) → STOP and tell the user to run
   `mimo providers login`.
2. Using the returned `options` (the authenticated intersection — count **models**,
   not providers):
   **Exactly one usable model** → auto-pick (asking is pointless). **≤4** → one
   AskUserQuestion listing them. **>4** (the common real case — a single provider can
   expose *dozens*) → **narrow, never dump**: AskUserQuestion the **provider** first
   (the authenticated set is small), then AskUserQuestion **≤4 models** for that
   provider — lead with `mimo-resolve`'s recommended id, and rely on the auto-added
   **Other** free-text for the long tail. One authenticated provider offering several
   models is still "more than one" → ASK; "low-risk"/"mechanical"/cost or proactivity
   never justify a silent pick, and printing the whole catalogue for the user to
   retype an id verbatim is the anti-pattern to avoid.
3. **Ask effort/variant** with a **≤4 menu** — AskUserQuestion caps at 4 options, so
   you **cannot** list all five variants + a default. Offer `default` (omit `--variant`)
   plus a few variants, **each with a one-line description** (`default` is the safe
   recommendation for a one-shot delegation); `minimal`/`medium` reach via **Other**.

The conductor does the asking/auto-pick itself — `mimo-resolve` only gathers,
never asks.

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
| Skipping effort selection | Offer a ≤4 variant menu (`default` that omits `--variant`, + a few with one-line descriptions; `minimal`/`medium` via Other). |
| Dumping the whole model list for the user to type an id (when >4) | Narrow provider-first: ASK the provider, then ≤4 of its models (recommended id first, Other for the tail). Never a wall of ids to retype. |
| Running mimo inline to "keep it simple" | Pollutes the main context. Always the subagent. |
| Resuming with `--continue` | Attaches to "the last session" → cross-task pollution. Resume is by recorded session id only. |
