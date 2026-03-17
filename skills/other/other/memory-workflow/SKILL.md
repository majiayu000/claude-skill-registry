---
name: memory-workflow
description: "Data workflow, memory system separation, and observation rules for git-review. Defines which memory system to use for what, and how to avoid duplication. Use when saving decisions, recording observations, or managing cross-session state."
---

# Memory & Data Workflow

## Data Workflow (ENFORCED)

- **Linear** = single source of truth for requirements, status, and acceptance criteria
- **claude-mem** = cross-session decision memory (supplements Linear, never duplicates)
- **Local plan files** = ONLY the planner agent writes these (`plans/<feature>-plan.md`), for code-level implementation detail too granular for Linear. All other agents write to Linear comments.
- Requirements, specs, critiques, and review results go to **Linear comments**, not local files

## Memory System Separation

| System | Purpose | What to Store |
|--------|---------|---------------|
| claude-mem | Human-driven | User preferences, architectural decisions, debugging insights, cross-session learnings |
| Claude-Flow | Agent-driven | Agent coordination patterns, code optimization history, model performance data |
| Serena | Code-driven | Project code structure, conventions, build commands (auto-discovered via onboarding) |
| Linear | Project management | Ticket requirements, acceptance criteria, status tracking |

**No overlap:** Each memory system serves a distinct purpose; never duplicate content across systems.

## claude-mem 3-Layer Workflow

1. **`search(query)`** — Get compact index with IDs (~50-100 tokens/result)
2. **`timeline(anchor=ID)`** — Get chronological context around interesting results
3. **`get_observations([IDs])`** — Fetch full details ONLY for filtered IDs

NEVER skip to `get_observations` without filtering first (saves ~10x tokens).

## When to Save (claude-mem)

- User states a preference or working style
- An architectural or design decision is made
- You discover a non-obvious project convention or pattern
- A debugging session yields a reusable insight
- A mistake is made that others (or future you) should avoid

## When NOT to Save

- Transient debugging context (one-off stack traces, temp workarounds)
- Information already in CLAUDE.md, README, or docs
- Obvious facts derivable from reading the code

## Observation Rules

- Memory observer agents are DEPRECATED — use `/checkpoint` skill instead
- If observers must be used: only record what was actually observed. Never fabricate details.
- If a session has minimal activity, record that limitation explicitly rather than padding with assumptions

## MCP Server Usage

- **claude-mem:** Cross-session memory only. Save decisions/patterns (brief). NEVER duplicate Linear content.
- **Linear:** Source of truth for requirements, status, and acceptance criteria. ALL tickets tracked there.
