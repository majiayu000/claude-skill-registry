---
name: optimus-prime
argument-hint: additional-context
description: "Configure Claude for specific projects. Use this skill when setting up claude-prime in a new project, detecting project conventions and stack, deciding what skills to create, or generating CLAUDE.md entry points. Analyzes codebase and creates project-specific rules."
disable-model-invocation: true
---

Ultrathink.

## Role

You are a project configurator. Analyze the codebase and configure Claude to work effectively with it.

## Context Assessment

Before starting, check:
- `.claude/rules/` has path-scoped files **besides `_apply-all.md`**? → Ask if user wants to reconfigure (`_apply-all.md` is a boilerplate default and should not be touched)
- `.claude/project/` exists? → Ask if user wants to reconfigure
- `./CLAUDE.md` exists? → Ask if user wants to regenerate

Wait for user confirmation before proceeding.

## Quick Start

1. Analyze project codebase (patterns, stack, conventions)
2. Copy matching starter skills from `.claude/starter-skills/` to `.claude/skills/`, adapt generic parts
3. Create skills for uncovered stacks via `/touch-skill`
4. Create `.claude/project/` with on-demand references
5. Identify `.claude/rules/` path-scoped guardrails (if any — rules are optional)
6. Generate `./CLAUDE.md` entry point
7. Delete `.claude/starter-skills/` (starters have been processed)

## Core Philosophy

1. **Three-layer system** — Skills (framework knowledge) + Rules (guardrails, auto-attach) + Project references (on-demand context)
2. **Context-aware placement** — Auto-attach only what prevents wrong code; everything else is on-demand
3. **LLM-driven analysis** — Claude explores codebase, not scripts
4. **Leverage existing tools** — Use `/touch-skill` + `docs-seeker` for skill generation

## Decision Matrix

| Detected | Where | Rule Test |
|----------|-------|-----------|
| General framework/library | Skill via `/touch-skill` | — |
| Project-specific constraint (wrong code even with skill) | `.claude/rules/` with `paths:` | "With the relevant skill activated, will code still be wrong without this?" → Yes |
| Architecture, structure, domain context | `.claude/project/` | — |

**Rules are optional.** "Important" ≠ "must auto-attach." Only create rules for things skills can't cover.

Red flags that something is NOT a rule:
- Applies to all files (`**/*.swift`, `**/*.ts`) → probably general knowledge, belongs in skill
- A skill already teaches this pattern → redundant, don't duplicate
- It's a language/framework feature, not a project decision → skill

## Output Structure

```
./CLAUDE.md                       # Entry point
.claude/rules/
└── <name>.md                     # Path-scoped guardrails (auto-attached)
.claude/project/
└── *.md                          # On-demand references (architecture, structure)
```

## Constraints

- Rule files must be concise — guardrails only, not documentation
- Rules auto-attach: do NOT reference them in CLAUDE.md
- Project references go to `.claude/project/` and ARE referenced in CLAUDE.md
- Show what will be created before creating
- Ask for confirmation at gates

## References

| Reference | Content |
|-----------|---------|
| [analysis-checklist.md](./references/analysis-checklist.md) | What to look for in projects |
| [claude-md-template.md](./references/claude-md-template.md) | CLAUDE.md format guide |

## Workflows

- [Full Setup](./workflows/setup-project.md) — Complete project setup flow (default workflow)

## Templates

- `templates/CLAUDE.template.md` — CLAUDE.md starter

## Additional Context (Optional)

<user-context>$ARGUMENTS</user-context>
