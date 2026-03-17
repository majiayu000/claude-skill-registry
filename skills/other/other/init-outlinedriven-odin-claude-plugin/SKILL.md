---
name: inits
description: Analyze a codebase and create or improve an AGENTS.md file for future agent instances. Use when onboarding to a repository and capturing hard-to-rediscover conventions, constraints, and rationale.
---

# Init - AGENTS.md Generator

Analyze this codebase and create or improve an `AGENTS.md` file for future ODIN Code Agent instances.

## Core principle

**Only encode knowledge that is expensive to rediscover.** An agent can `fd`, `rg`, `ast-grep`, and read files in seconds. If the information is one search away, omit it.

## Objective guard

`AGENTS.md` is for **priming and guiding** future agents with conventions, constraints, and rationale. It is **not** a repository summary.

## What to include

1. Cross-cutting conventions and boundaries that span multiple files.
2. Implicit contracts and operational constraints that are easy to miss in quick code exploration.
3. Non-obvious command guidance only when hidden constraints matter (required ordering, flags, env vars, caveats).
4. For each included item, state:
   - the rule or constraint
   - why it exists (rationale)

## What to omit (the agent can discover these)

- File trees, per-directory descriptions, or component inventories.
- Dependency/version tables.
- Generic development best practices.
- Information that is easily discoverable via search/read.
- Fabricated filler sections such as "Common Development Tasks", "Tips", or "Support".
- Any summary-style prose that restates code organization without conventions or rationale.

## Workflow

- If `AGENTS.md` already exists, suggest targeted improvements instead of rewriting.
- Do not repeat yourself. Each fact appears once.
- Every statement must be grounded in files you actually read. Never invent.
- If uncertain, omit the claim rather than speculate.
