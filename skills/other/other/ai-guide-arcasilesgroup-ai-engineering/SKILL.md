---
name: ai-guide
description: "Use when onboarding to a project, exploring architecture, or understanding why decisions were made: interactive tours, decision archaeology, and codebase discovery."
effort: high
argument-hint: "tour|find <topic>|history <decision>|onboard"
tags: [onboarding, architecture, teaching, archaeology]
---


# Guide

Project onboarding, architecture tours, and decision archaeology. Optimized for the human, not the code. Reads everything, modifies nothing. Teaches understanding, not artifacts.

## When to Use

- New to a project and need orientation.
- Want to understand component relationships and data flow.
- Asking "why was X chosen over Y?"
- NOT for writing code -- use `ai-build agent`.
- NOT for generating docs -- use `/ai-write`.

## Modes

### tour -- Architecture Overview

1. **Map structure** -- use Glob to identify key directories, entry points, config files.
2. **Identify stack** -- detect languages, frameworks, build tools.
3. **Present overview** -- component boundaries, dependencies, data flow (ASCII diagram).
4. **Explain key patterns** -- design patterns, idioms, conventions used.
5. **Highlight evolution** -- `git log --oneline` for major changes.
6. **Flag gotchas** -- non-obvious behavior, implicit assumptions, known debt.
7. **Suggest next** -- related components worth exploring.

### find -- Topic Search

1. **Search codebase** -- Grep/Glob for the topic across source, config, docs.
2. **Search decisions** -- check `state/decision-store.json` for related decisions.
3. **Search specs** -- look in `specs/` for relevant specifications.
4. **Present results** -- files, functions, and context around the topic.
5. **Answer the question** -- "where does X happen?", "how do I add a Y?", "what tests cover Z?"

### history -- Decision Archaeology

1. **Search decision store** -- `state/decision-store.json` for formal decisions.
2. **Search git history** -- `git log --all --grep` for related commits.
3. **Search specs** -- `specs/` for specs that introduced the decision.
4. **Reconstruct context** -- what was known, what constraints existed, what alternatives were considered.
5. **Present alternatives** -- what other options existed and why they were rejected.
6. **Assess relevance** -- has context changed? Are original constraints still valid?
7. **Do NOT recommend** -- present analysis, let developer decide.

### onboard -- Structured Onboarding

1. **Map structure** -- directories, entry points, config, dependencies.
2. **Identify stack** -- languages, frameworks, tools.
3. **Discover patterns** -- recurring code patterns, naming conventions.
4. **Find key files** -- main entry, config, models, tests.
5. **Review standards** -- `.ai-engineering/standards/` for project conventions.
6. **Socratic checkpoints** -- after each phase, ask one question to confirm understanding.
7. **Personalized path** -- based on what the developer wants to work on.

## Quick Reference

```
/ai-guide tour                    # architecture overview
/ai-guide find "authentication"   # where does auth happen?
/ai-guide history "why SQLite"    # decision archaeology
/ai-guide onboard                 # structured onboarding
```

## Common Mistakes

- Making decisions for the developer -- present tradeoffs, let them decide.
- Writing code during a tour -- guide is strictly read-only.
- Over-quizzing -- max 2 Socratic questions per interaction.
- Teaching below the developer's level -- match cues to Bloom's taxonomy.

## Integration

- Uses `/ai-explain` for 3-tier depth explanations.
- Reads `state/decision-store.json` for decision context.
- Reads `state/audit-log.ndjson` for session context (privacy by design).

## References

- `.claude/skills/ai-explain/SKILL.md` -- 3-tier depth model.
- `.ai-engineering/manifest.yml` -- governance structure.
- `state/decision-store.json` -- decision records.
$ARGUMENTS
