---
name: workflow
description: Skill orchestration - user commands vs auto-triggered
user-invocable: false
model: haiku
---

# Workflow Overview

## User Commands (6)

```
┌─────────────────────────────────────────────────────────┐
│  "auto"          → Execute all tasks autonomously       │
│  "review"        → Code quality check on recent changes │
│  "brainstorm"    → Scan → propose → create stories      │
│  "test"          → npm test + browser tests on latest   │
│  "audit"         → Rate aspects → create stories        │
│  "status"        → Quick progress check                 │
└─────────────────────────────────────────────────────────┘

Aliases: "what next" = brainstorm
```

## Auto-Triggered (Internal)

| Trigger | Action |
|---------|--------|
| Task complete | `verify` runs automatically |
| Every 5 tasks | `checkpoint` saves context |
| User says "ship" | `deploy` runs |
| Artifacts pile up | `clean` suggested |

## Analysis → Stories Flow

```
brainstorm / audit / what next
    ↓
Parallel scans (6 Haiku agents)
    ↓
Rate aspects / Present scenarios
    ↓
Auto-create stories for top issues
    ↓
User says "auto" → Execute
```

## Task Lifecycle

```
TaskCreate (from brainstorm/audit)
    ↓
auto picks up task
    ↓
Implement → Typecheck → Build
    ↓
verify (auto) → Browser test if UX
    ↓
TaskUpdate: completed
    ↓
checkpoint (every 5) → Next task
```

## Quick Reference

| Want to... | Say |
|------------|-----|
| Work through tasks | `auto` |
| Check quality | `review` |
| Don't know what's next | `brainstorm` or `what next` |
| Run all tests | `test` |
| Rate the app | `audit` |
| See progress | `status` |
