---
name: brainstorm
description: Use before any feature, design, or non-trivial change — explores intent, constraints, and design before implementation
---

# Brainstorm

Turn ideas into designs through collaborative dialogue. Understand context, ask questions, propose approaches, get approval, write the spec.

Do NOT write code, scaffold, or invoke implementation skills until the user approves the design.

## Process

1. **Explore context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, prefer multiple choice
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — section by section, get approval incrementally
5. **Write spec** — save to `docs/specs/YYYY-MM-DD-<topic>-design.md`, commit
6. **Spec review** — dispatch spec-reviewer subagent (see spec-reviewer-prompt.md), fix issues, repeat until approved (max 5 iterations)
7. **User review gate** — ask user to review the written spec before proceeding
8. **Transition** — invoke `dodi-dev:write-plan`

## Design Principles

- **One question per message** — don't overwhelm
- **YAGNI ruthlessly** — cut unnecessary features
- **Design for clear boundaries** — each unit has one purpose, a well-defined interface, and can be understood independently
- **Follow existing patterns** — explore the codebase before proposing changes
- **Scale detail to complexity** — a few sentences for simple sections, more for nuanced ones

## Scope Check

If the request spans multiple independent subsystems, decompose into sub-projects first. Each gets its own spec → plan → implementation cycle.
