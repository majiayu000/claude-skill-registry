---
name: browser
description: "Interactive browser automation via playwright-cli. Use when you need to navigate a site, click elements, fill forms, take snapshots, or triage a live app."
when_to_use: "Triggers: user says 'open browser', 'check this site', 'triage the app', 'test this flow', 'look at this page', or '/craft:browser'. Also when needing visual inspection of a running app, before/after screenshots of UI changes, or interactive site exploration."
allowed-tools: ["Read", "Bash", "Glob", "Grep", "Agent", "SendMessage"]
---

# Browser

Interactive browser automation powered by `playwright-cli`. Launches a persistent `playwright-browser` agent that owns a live browser session. You steer it via SendMessage - the agent remembers what it's seen and done across turns.

## Why This Exists

Chrome DevTools MCP works but has limitations: no persistent agent session between tool calls, no interactive steering, and full accessibility trees streamed into context (~114k tokens per task). playwright-cli saves snapshots to disk as YAML (~27k tokens per task, ~4x cheaper) and supports named sessions that persist across agent turns.

`/craft:dial` is the deliberate exception to this stance: that objection targets snapshot-heavy agent work, while dial runs in the main loop on `evaluate_script` plus at most two screenshots, and page state persists between its calls - so dial keeps Chrome DevTools MCP.

This skill is **purely additive**. It does not replace or modify Chrome DevTools MCP, the walkthrough-analyzer, or any existing analyzer agent.

## Prerequisites

Requires `playwright-cli` installed globally:

```bash
npm install -g @playwright/cli && playwright-cli install-browser
```

The skill checks prerequisites at every invocation and fails with copy-pasteable instructions if missing.

## The Flow

### Step 1: Check Prerequisites

```bash
command -v playwright-cli >/dev/null 2>&1 || { echo "PREREQ_MISSING: playwright-cli. Run: npm install -g @playwright/cli && playwright-cli install-browser"; exit 2; }
```

If the check fails, report the error with the install command. Do not proceed.

### Step 2: Parse Arguments

Arguments follow this pattern:

```
/craft:browser <url> [goal] [--headless] [--session=name]
```

- **url** (required): The URL to navigate to
- **goal** (optional): What to do - e.g., "triage the whole site", "test the login flow", "check accessibility"
- **--headless** (optional): Run without visible browser window. Default is **headed** (visible browser) so the user can watch
- **--session=name** (optional): Explicit session name (max 12 chars, lowercase alphanumeric). If omitted, auto-derive.

### Step 3: Determine Session Name

**CRITICAL: Session names must be <= 12 characters, lowercase alphanumeric only.** macOS has a 104-char Unix socket path limit. Long names cause silent socket lookup failures, which spawn duplicate browsers instead of erroring.

Auto-derive a short session name:

```bash
# Simple counter-based naming
SESSION="craft$(date +%H%M)"
```

If `--session=name` was provided explicitly, use that (after validating length <= 12).

**DO NOT derive session names from story/cycle slugs.** Those are too long and contain dashes. Use short, opaque names.

### Step 4: Clean Up Stale Sessions

Check for and kill any existing craft sessions before launching:

```bash
playwright-cli list 2>/dev/null
```

If sessions are listed that match a `craft*` pattern, close them:

```bash
playwright-cli kill-all 2>/dev/null
```

Only run `kill-all` if stale sessions are detected. For a clean state, this is a no-op.

When the target page may have hosted a `/craft:dial` session, have the agent run the canonical dial clear on arrival (remove `craft-dial-style`, `craft-dial-panel`, every `[data-craft-dial-injected]` node, delete `documentElement.dataset.craftDial` - idempotent on a clean page, see `commands/references/dial-inject.md`) so screenshots never capture dial scaffolding.

### Step 5: Launch the Agent

Invoke the `playwright-browser` agent with full context. The agent handles browser open, navigation, and initial snapshot internally.

```
Agent({
  subagent_type: "craft:playwright-browser",
  description: "Browser session: {url}",
  prompt: "SESSION: {session_name}
URL: {url}
GOAL: {goal or 'Interactive exploration - wait for instructions'}
HEADED: {true unless --headless}

Open the browser with the URL in a single command, check the console, and report what you see. Then wait for instructions unless a specific goal was provided."
})
```

**IMPORTANT:** Use `subagent_type: "craft:playwright-browser"` (with the craft: prefix).

The agent returns its agentId. Report this to the user so they know they can continue the session.

### Step 6: Relay Results

When the agent returns from its first pass:
1. Show the agent's summary to the user
2. Tell them they can continue steering the browser by talking to you (the orchestrator relays to the agent via SendMessage)
3. The browser session stays alive until explicitly closed

## Session Lifecycle

- **Created:** When the agent runs `playwright-cli -s=$SESSION open --headed $URL`
- **Active:** Agent owns the session, responds to SendMessage
- **Closed:** When user says "done" / "close" / "wrap up", or agent reaches budget cap
- **Cleanup:** Agent runs `playwright-cli -s=$SESSION close` before exiting

## Guard Rails

1. **Prerequisites checked every invocation.** Never cached, never assumed.
2. **Headed by default.** The user should see the browser. Use `--headless` only when explicitly requested.
3. **Session names <= 12 chars.** Lowercase alphanumeric only. No dashes. No story slugs.
4. **No existing agents/skills modified.** This is additive only.
5. **Agent budget:** The playwright-browser agent has a 60 tool-call budget. For longer sessions, the user can launch a new session.
6. **No raw YAML in context.** The agent reads snapshots from disk and returns summaries. YAML stays on disk, summaries go to context.
7. **`open` called exactly once.** The agent opens the browser once with the URL. Never re-opens on failure - checks `list` first.
