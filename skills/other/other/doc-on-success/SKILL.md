---
name: doc-on-success
description: After a feature is implemented or a bug is fixed, confirm success with the user and then update project documentation.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
model: sonnet
---

# Document on Success

After completing a feature implementation or bug fix, follow this process **every time**.

## Recent Changes
!`git diff --stat HEAD~3 2>/dev/null || echo "(no git history)"`
!`git log --oneline -5 2>/dev/null || echo "(no git history)"`

## Step 1: Confirm Success with the User

**Never skip this step.** Before writing any documentation, explicitly ask:

> "That looks like it's working — can you confirm the [feature/fix] is behaving correctly before I update the docs?"

Wait for the user to confirm. Acceptable confirmations include:
- Explicit: "yes", "confirmed", "it works", "looks good", "perfect"
- Implicit: the user moves on to the next task without reporting issues

**Do NOT document if:**
- The user reports it's still broken
- Tests are failing
- The user hasn't had a chance to verify yet
- You're unsure whether the change actually works

## Step 2: Determine What Changed

Categorize the work:

| Type | Description | Example |
|------|-------------|---------|
| **Feature** | New capability that didn't exist before | Discord bot, session persistence |
| **Bug fix** | Something was broken and is now working | Session store path resolution |
| **Enhancement** | Improvement to existing functionality | PID file guard, atomic file writes |
| **Infrastructure** | Build, deploy, or tooling changes | LaunchAgent setup, Python runner |

## Step 3: Update Documentation

Update the appropriate files based on what changed:

### Always update: `ARCHITECTURE.md`

For **features and infrastructure**, add or update the relevant section:
- Describe what the component does
- Explain the design decisions and trade-offs (especially "why" — not just "what")
- Include a flow diagram if the interaction involves multiple components
- Document any non-obvious gotchas or constraints

For **bug fixes**, add to the Troubleshooting section:
- What the symptom looked like
- What the root cause was
- How to prevent or fix it

### Always update: `README.md`

- Add new features to the feature list or project structure
- Update the Quick Start section if setup steps changed
- Update the Discord Commands table if commands were added
- Update the Build Phases table if a phase status changed

### Update if relevant: Memory file (`ai-harness.md`)

- Add new key files or architectural decisions
- Update the Status section
- Add new git commit hashes
- Document any new gotchas or patterns discovered

### Update if relevant: `PLAN.md`

- Check off completed tasks
- Update phase status markers

## Step 4: Keep It Human-Readable

Documentation should be written for a person who has never seen the project. Follow these principles:

- **Lead with "why"** — explain the reasoning before the implementation
- **Use diagrams** — ASCII flow charts for multi-component interactions
- **Include examples** — show actual commands, not abstract descriptions
- **Document failures** — what was tried and didn't work is as valuable as what did
- **No jargon without context** — if you reference a concept (e.g., "atomic rename"), explain it briefly

## Step 5: Update AI-Optimized Documentation

Alongside human docs, maintain `CONTEXT.md` at the project root. This file is structured for an AI agent (including yourself in future sessions) to rapidly understand the project state and make correct decisions without re-reading every file.

### `CONTEXT.md` Format

```markdown
# AI Harness — Agent Context

> Machine-readable project state. Updated after every confirmed change.
> Last updated: YYYY-MM-DDTHH:MM:SS

## System Map

<!-- One-line-per-component. Format: component | file | status | depends_on -->

| Component | Entry Point | Status | Dependencies |
|-----------|-------------|--------|--------------|
| Discord bot | bridges/discord/bot.ts | active | claude-runner.py, session-store.ts |
| Claude runner | bridges/discord/claude-runner.py | active | claude CLI |
| ... | ... | ... | ... |

## Interfaces

<!-- How components talk to each other. Keep exact file paths, function names, data shapes. -->

### bot.ts → claude-runner.py
- Spawn: `python3 claude-runner.py <output_file> -p --output-format json [--resume <id>] <prompt>`
- Output file schema: `{ stdout: string, stderr: string, returncode: number }`
- Polling: 1s interval, 120s timeout

### bot.ts → session-store.ts
- `getSession(channelId): string | null`
- `setSession(channelId, sessionId): void`
- `clearSession(channelId): boolean`
- Storage: `sessions.json` (lazy path via `getStorePath()`)

## Constraints & Gotchas

<!-- Things that WILL break if you ignore them. Format: short rule → consequence. -->

- NEVER spawn `claude` directly from Node.js → hangs indefinitely (issue #771)
- NEVER pass CLAUDE* env vars to claude-runner.py → "nested session" error
- Session store path MUST be lazy (function, not constant) → dotenv loads after imports
- Only ONE bot instance at a time → PID file guard at .bot.pid
- Discord messages > 2000 chars → must split with code block preservation

## Change Log

<!-- Append-only. One line per confirmed change. Format: date | type | description | commit -->

| Date | Type | Description | Commit |
|------|------|-------------|--------|
| 2025-03-09 | feature | Discord bot with Claude integration | cc621e6 |
| 2025-03-09 | docs | README + ARCHITECTURE | 2e9b246 |
```

### CONTEXT.md Rules

1. **Keep it flat** — no nested sections deeper than H3. An AI scanning this file should get the full picture in one pass.
2. **Use tables over prose** — structured data is faster to parse than paragraphs.
3. **Exact names only** — use real file paths, function signatures, and data shapes. No paraphrasing.
4. **Constraints are imperative** — write them as rules ("NEVER do X → Y happens"), not explanations.
5. **Change log is append-only** — never edit old entries, only add new ones.
6. **Update on every confirmed change** — add new components to System Map, new interfaces to Interfaces, new gotchas to Constraints, and a new row to Change Log.

### Why Both Human and AI Docs?

| | `README.md` / `ARCHITECTURE.md` | `CONTEXT.md` |
|---|---|---|
| **Audience** | Humans (developer reading for the first time) | AI agents (including future you) |
| **Style** | Narrative, explanatory, "why" focused | Structured, terse, "what" focused |
| **Diagrams** | ASCII flow charts with labels | Tables with exact function signatures |
| **Constraints** | Explained with context and history | Stated as imperative rules |
| **Change tracking** | Implicit in git history | Explicit append-only table |

## Step 6: Commit Documentation Separately

Documentation should be committed as its own commit, separate from the code change:

```
git add README.md ARCHITECTURE.md CONTEXT.md
git commit -m "Update docs: [brief description of what was documented]"
```

This keeps the git history clean — code changes and doc changes are independently reviewable.

## Trigger Conditions

This skill activates when ANY of these are true:
- A feature implementation is confirmed working by the user
- A bug fix is confirmed resolved by the user
- A phase in PLAN.md is completed
- Infrastructure or tooling changes are verified working
- The user explicitly asks for documentation

## What NOT to Document

- Work in progress (document only after confirmation)
- Temporary debugging steps or experiments
- Changes that were reverted
- Internal implementation details that don't affect understanding (e.g., variable names)
