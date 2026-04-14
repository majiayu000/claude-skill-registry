---
name: optimus-prime
argument-hint: additional-context
description: "Bootstraps Claude Code configuration for a project. Trigger on 'prime this project', 'set up claude', 'configure claude for this repo', 'bootstrap', 'prime', 'optimus-prime'. Detects stack, copies starter skills, generates CLAUDE.md and project-specific rules."
---

Ultrathink.

## Context Assessment

Before starting, check:
- `.claude/rules/` has path-scoped files **besides `_apply-all.md`**? → Ask if user wants to reconfigure (`_apply-all.md` is a boilerplate default and should not be touched)
- `./CLAUDE.md` exists? → Ask if user wants to regenerate

Wait for user confirmation before proceeding.

## Quick Start

1. Analyze project codebase
2. Copy matching starter skills, create skills for uncovered stacks via `/skill-creator`
3. Identify `.claude/rules/` guardrails (optional — zero rules is valid)
4. Generate `./CLAUDE.md` — only guide what Claude doesn't do by default
5. Offer `CLAUDE.local.md` setup (gitignored personal preferences)
6. Clean up and verify

## Core Philosophy

1. **Lean knowledge system** — CLAUDE.md (always-on context) + Skills (domain knowledge) + Rules (guardrails, auto-attach). On-demand refs point to wherever docs already live.
2. **Guide, don't template** — Claude generates good CLAUDE.md natively. Augment with reference pointers and project-specific context it wouldn't discover on its own.
3. **LLM-driven analysis** — Claude explores codebase, not scripts
4. **Leverage existing tools** — Use `/skill-creator` to autonomously create and optimize skills (with eval-driven iteration), and `docs-seeker` for documentation research

## Decision Matrix

| Detected | Where | Rule Test |
|----------|-------|-----------|
| General framework/library | Skill via `/skill-creator` | — |
| Project-specific constraint (wrong code even with skill) | `.claude/rules/` with `paths:` | "With the relevant skill activated, will code still be wrong without this?" → Yes |
| Always-on project context (identity, commands, stack) | `CLAUDE.md` | — |
| Detailed architecture/domain docs (human) | `docs/`, READMEs — referenced from CLAUDE.md | — |
| Agent-optimized references (optional) | `.claude/project/` — only when human docs are too verbose for agents | — |

**Rules are optional.** "Important" ≠ "must auto-attach." Only create rules for things skills can't cover.

## Output Structure

```
./CLAUDE.md                       # Always-on project context
./CLAUDE.local.md                 # Personal preferences (gitignored, optional)
.claude/rules/
└── <name>.md                     # Path-scoped guardrails (auto-attached, optional)
```

## Gotchas

- **Over-ruling existing conventions**: Don't overwrite project rules the team already has in place.
- **Copying starters verbatim**: Starter skills need project-specific customization. Generic starters are unhelpful.
- **Forgetting to delete starters**: After processing, starter-skills/ directory must be removed from the target.
- **Modifying _apply-all.md in target**: These are universal rules from prime. Don't change them during priming.

## Constraints

- Rules auto-attach: do NOT reference them in CLAUDE.md
- On-demand references point to wherever docs already live (`docs/`, READMEs, etc.) — no prescribed directory

## References

| Reference | Content |
|-----------|---------|
| [analysis-checklist.md](./references/analysis-checklist.md) | What to look for in projects |

## Workflows

- [Full Setup](./workflows/setup-project.md) — Complete project setup flow (default workflow)

## Additional Context (Optional)

<user-context>$ARGUMENTS</user-context>
