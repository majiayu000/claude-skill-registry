---
name: agent-routing
description: "Agent pipeline, model routing, and delegation framework for git-review. Defines which agent handles which task, model tiers (Opus/Sonnet/Haiku), and when to use junior-coder vs coder vs senior-coder. Use when spawning agents or deciding task assignment."
---

# Agent Routing & Delegation

## Agent Pipeline (ordered workflow)

1. `requirements-interviewer` (Sonnet) — Gather and clarify requirements from the user
2. `explorer` (Sonnet) — Research libraries, APIs, prior art, technical approaches
3. `architect` (Sonnet) — Design module boundaries, data flow, type definitions
4. `planner` (Opus) — Write step-by-step implementation plan (ONLY agent that writes local plan files)
5. `red-teamer` (Opus) — Critique the plan, find bugs/edge cases/risks before implementation
6. `junior-coder` (Haiku) — Scaffolding, boilerplate, mechanical refactors from fully-specified plans
7. `coder` (Sonnet) — Standard implementation with TDD
8. `senior-coder` (Opus) — Complex/cross-cutting/performance-critical implementation
9. **`tech-lead` (Sonnet) — Cross-cutting review AFTER each implementation step, BEFORE commit** (see `.claude/agents/tech-lead.md`)
10. `reviewer` (Sonnet) — Code review after implementation (reads code, checks quality)
11. `qa` (Sonnet) — QA testing after implementation (runs things, verifies behavior, tests hooks/workflows)
12. `documentation` (Haiku) — Update README, doc comments, guides
13. `explainer` (Haiku) — Explain code at different expertise levels (junior → staff/architect)
14. `optimizer` (Haiku) — Meta-workflow audit (run after every major task completion)

## When to Use junior-coder vs coder vs senior-coder

- **junior-coder (Haiku):** Scaffolding new files from spec, struct/enum definitions, adding imports/mod declarations, moving functions between modules, writing boilerplate (constructors, getters, Display impls). Task MUST be fully specified with zero ambiguity.
- **coder (Sonnet):** Single-module changes, straightforward features, bug fixes with clear cause, test writing, anything requiring logic or design decisions
- **senior-coder (Opus):** Cross-module refactors, performance-critical paths, subtle/intermittent bugs, architecture-sensitive changes, tasks a coder failed at

## Orchestrator Rules

- The orchestrator (main session) MUST NOT write implementation code directly
- The orchestrator coordinates: spawns agents, assigns tasks, reviews results
- ALL code changes go through junior-coder, coder, or senior-coder agents
- The orchestrator MAY edit non-code files: CLAUDE.md, agent specs, hook scripts, plans
- **Use the decision framework**: subagent for independent tasks, team for peer communication
- **After each implementation step**: spawn tech-lead (subagent or team member) to review before committing
- The orchestrator commits ONLY after tech-lead approves (or for trivial/no-code changes)

## Model Routing

- **Agent specs** (`.claude/agents/*.md`) define the authoritative model for each agent type
- **Claude-Flow routing** provides suggestions based on task complexity and past performance
- **In case of conflict:** Agent spec always wins (manual configuration > automated suggestion)
- **Model tiers:** Opus (3: planner, red-teamer, senior-coder), Sonnet (7: requirements-interviewer, explorer, architect, coder, tech-lead, reviewer, qa), Haiku (4: junior-coder, documentation, explainer, optimizer)
- **Example:** `coder` uses Sonnet (per spec), even if Claude-Flow suggests Opus for a task

## Portability Notes

- SKILL.md standard works across Claude Code, ChatGPT, Cursor, Copilot
- Agent specs (.claude/agents/) are Claude Code-specific
- Hooks (.claude/hooks/) are Claude Code-specific
- Keep skills portable; keep enforcement tool-specific
