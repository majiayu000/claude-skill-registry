---
name: agent-changelog
description: Compile an agent-optimized changelog by cross-referencing git history with plans and documentation. Use when asked to "update changelog", "compile history", "document project evolution", or proactively after major milestones, architectural changes, or when stale/deprecated information is detected that could confuse coding agents.
---

# Agent Changelog

Compile a chronological record of key decisions, architectural changes, and project evolution optimized for coding agent context-building.

## Output

Write to `AGENT_CHANGELOG.md` in the project root. This file helps agents:
- Understand key decisions and their rationale
- Identify deprecated patterns/approaches to avoid
- Grasp the trajectory from past to present to likely future
- Detect stale documentation that contradicts current reality

## Workflow

### 1. Gather Sources

Collect information from these sources in parallel:

**Git history:**
```bash
git log --oneline --since="6 months ago" | head -100
git log --all --oneline --grep="BREAKING" --grep="deprecate" --grep="remove" --grep="migrate" -i
git tag -l --sort=-creatordate | head -20
```

**Documentation:**
- `.claude/plans/` - implementation plans and decisions
- `CLAUDE.md` - project instructions
- `README.md` - project overview
- `docs/` or similar documentation directories
- `CHANGELOG.md` if exists (traditional changelog)

**Code signals:**
- `@deprecated` annotations
- `TODO`, `FIXME`, `HACK` comments with dates
- Migration files, upgrade scripts

### 2. Identify Key Events

Extract events that matter for agent understanding:

**Always include:**
- Architectural decisions (new patterns, removed patterns)
- Breaking changes and migrations
- Deprecated features/approaches
- Major dependency changes
- Directory structure changes
- API changes (internal or external)

**Include if significant:**
- New features that change how agents should work
- Bug fixes that reveal incorrect assumptions
- Performance changes that affect approach recommendations

**Skip:**
- Minor bug fixes
- Cosmetic changes
- Routine dependency updates
- Individual feature additions (unless architectural)

### 3. Cross-Reference for Contradictions

For each significant event, check if existing documentation contradicts it:

```
Event: "Migrated from Redux to Zustand" (commit abc123, 2024-03)

Check: Does any documentation still reference Redux patterns?
- README.md mentions Redux? → Flag as STALE
- CLAUDE.md suggests Redux approach? → Flag as STALE
- Old tutorials in docs/? → Flag as STALE
```

Track contradictions in a "Stale Information Detected" section.

### 4. Write the Changelog

Structure the output file:

```markdown
# Agent Changelog

> This file helps coding agents understand project evolution, key decisions,
> and deprecated patterns. Updated: [DATE]

## Current State Summary

[2-3 sentences on where the project is NOW - the authoritative current architecture]

## Stale Information Detected

[List any documentation that contradicts current reality - agents should ignore these until fixed]

| Location | States | Reality | Since |
|----------|--------|---------|-------|
| docs/auth.md | "Uses JWT tokens" | Migrated to sessions | 2024-06 |

## Timeline

### [YEAR-MONTH] - [Brief Title]

**What changed:** [Factual description]

**Why:** [Decision rationale if known from plans/commits]

**Agent impact:** [How this affects how agents should work in the codebase]

**Deprecated:** [What approaches/patterns should agents avoid]

---

[Repeat for each significant event, reverse chronological]

## Deprecated Patterns

[Consolidated list of things agents should NOT do, with what to do instead]

| Don't | Do Instead | Deprecated Since |
|-------|------------|------------------|
| Use `OldService` | Use `NewService` | 2024-08 |

## Trajectory

[Brief note on where the project appears to be heading based on recent changes and plans]
```

### 5. Validate and Update

After writing:
- Read existing `AGENT_CHANGELOG.md` if present and merge, don't duplicate
- Verify dates against git history
- Ensure "Stale Information Detected" section is actionable

## When to Proactively Run

Suggest running this skill when:
- A major refactor or migration just completed
- Plans in `.claude/plans/` were recently executed
- Multiple architectural decisions happened in quick succession
- Detected documentation that seems to contradict code reality
- Starting work on a codebase after a long gap
- Onboarding to an unfamiliar codebase

## Guidelines

- Prioritize accuracy over completeness—wrong history is worse than incomplete
- Include rationale when available (commit messages, plan docs)
- Be specific about what agents should avoid, not just what changed
- Keep entries concise—this is reference material, not storytelling
- Date everything to help agents judge relevance
