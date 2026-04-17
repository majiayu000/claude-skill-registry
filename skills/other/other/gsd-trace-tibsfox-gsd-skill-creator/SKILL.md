---
name: gsd-trace
description: Traces decisions and requirements through GSD artifacts. Use when user asks "why did we...", "what happened to...", or mentions decision history.
---

# GSD Decision Archaeology

Excavate GSD artifact timeline to reconstruct decision chains, requirement evolution, and phase rationale.

## Sources (authority order)

1. PROJECT.md Key Decisions
2. STATE.md Session Continuity
3. ROADMAP.md phase goals/criteria
4. Phase CONTEXT.md / RESEARCH.md
5. Plan SUMMARY.md outcomes
6. Git commit messages
7. Archived milestone docs

## Trace Process

1. **Identify query type** — decision rationale, requirement status, phase outcome, impact analysis
2. **Search sources** — start with highest authority, cross-reference downward
3. **Build timeline** — chronological events from artifacts
4. **Trace causality** — link decisions to requirements to implementation
5. **Answer directly** — cite specific sources and dates

## Query Types

| Type | Primary Sources |
|------|----------------|
| Why decision X? | PROJECT.md Key Decisions, RESEARCH.md |
| What happened to req Y? | REQUIREMENTS.md, STATE.md, milestones/ |
| Phase N outcome? | ROADMAP.md, SUMMARY files, git commits |
| What depends on X? | PLAN files, git history, code search |
| What was tried/abandoned? | RESEARCH.md, STATE.md |

## Limitations

Can only trace what GSD documented. Undocumented decisions, verbal discussions, and vague commit messages are untraceable.
