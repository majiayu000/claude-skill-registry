---
name: intent-detection
description: "Internal router for ambiguous work requests. Load when user says \"add/build/implement feature\", \"fix/debug/investigate bug\", \"review/audit code\", \"refactor/clean up\", \"slow/performance\", \"PR comments\", \"research/evaluate library\", or \"that fixed it\" — WITHOUT an explicit /phx: slash command."
effort: medium
user-invocable: false
---

# Intent Detection — Workflow Routing

When user describes work WITHOUT specifying a `/phx:` command, analyze their intent and suggest the appropriate workflow BEFORE starting work.

## Routing Table

| Signal | Detected Intent | Suggest |
|--------|----------------|---------|
| "bug", "error", "crash", "failing", "broken", stack trace | Bug investigation | `/phx:investigate` |
| "add", "implement", "build", "create" + multi-step | New feature | `/phx:plan` |
| "review", "check", "audit" code | Code review | `/phx:review` |
| "fix" + small/specific scope | Quick fix | handle directly or `/phx:quick` |
| "refactor", "clean up", "improve" | Refactoring | `/phx:plan` (needs scope) |
| "research", "how to", "what's the best" | Research | `/phx:research` |
| "evaluate", "compare", "adopt", "library", "should we use" | Library evaluation | `/phx:research --library` |
| "test", "spec", "coverage" | Testing | handle directly or `/phx:plan` |
| Describes 1-2 file changes, < 50 lines | Small task | handle directly |
| "deploy", "release", "production" | Deployment | `/phx:verify` then deploy |
| "performance", "slow", "N+1", "memory" | Performance | `/phx:perf` |
| "PR review", "review comments", "address feedback", "respond to PR" | PR response | `/phx:pr-review` |
| "that worked", "fixed it", "problem solved" | Knowledge capture | `/phx:compound` |
| "enhance plan", "more detail", "deepen" | Plan enhancement | `/phx:plan --existing` |
| "triage", "which findings", "prioritize fixes" | Finding triage | `/phx:triage` |

## Behavior

1. Read user's first message
2. Match against routing table (use keyword + context signals, not exact match)
3. If match found with multi-step workflow: "This looks like [intent]. I'd suggest `[command]` — want me to run it, or should I just dive in?"
4. If trivial task (typo, single-line fix, config change): skip suggestion, just do it
5. If user already specified a `/phx:` command: follow it, don't re-suggest
6. **NEVER block the user** — suggestion only, not mandatory

## Confidence Signals

High confidence (suggest immediately):

- Stack trace or error message pasted → `/phx:investigate`
- "Add [feature] with [multiple components]" → `/phx:plan`
- "Review my changes" or "check this PR" → `/phx:review`

Medium confidence (suggest with caveat):

- "Fix [thing]" — could be quick or complex, suggest based on scope description
- "Update [thing]" — could be small edit or refactor

Low confidence (just do it):

- Single file mentioned, clear change
- "Change X to Y"
- Configuration or dependency updates

## Complexity Signals

When a task matches a workflow command, check complexity before suggesting:

**Trivial signals** (suggest `/phx:quick` or handle directly):

- Single file mentioned explicitly
- "exclude X from Y", "add X to config", "rename", "change X to Y"
- Problem + solution both stated ("X is wrong, change to Y")
- One-line fix described

**Complex signals** (suggest `/phx:plan` or `/phx:investigate`):

- 3+ modules or files mentioned
- "intermittent", "race condition", "sometimes", "random"
- Stack trace with 5+ frames
- "across", "all", "every" (scope indicators)

**Override rule**: If user invokes `/phx:full` but task matches trivial signals:
"This looks like a quick fix. Want `/phx:quick` instead, or stick with the full cycle?"

## Iron Laws

1. **NEVER block on suggestion** — If user starts explaining, just do the work
2. **One suggestion max** — Don't re-suggest if user ignores first suggestion
3. **Commands are shortcuts, not gates** — All work can be done without commands

## Integration

This skill is consulted at session start. It works alongside:

- SessionStart hook (shows plugin loaded message)
- CLAUDE.md routing instructions (passive reference)
- Individual workflow skills (activated by commands)
