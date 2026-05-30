---
name: phx:boundaries
description: Analyze Phoenix context boundaries and module coupling via mix xref. Use when checking cross-context calls, validating dependencies, before splitting modules, or reviewing architecture.
effort: medium
argument-hint: [--assess|--fix]
allowed-tools: Read, Grep, Glob, Bash
---

# Phoenix Context Boundary Validation

Analyze module dependencies to ensure clean context separation and proper architectural boundaries.

## Usage

```
/phx:boundaries              # Check for violations
/phx:boundaries --assess     # Score context health (0-100)
/phx:boundaries --fix        # Suggest fixes for violations
```

## `--assess` Mode: Context Health Score

Evaluate overall boundary health with a quantified score.

### Metrics Calculated

| Metric | Healthy Range | Red Flag | Weight |
|--------|---------------|----------|--------|
| Modules per context | 3-15 | >20 or <2 | 20% |
| Public API surface | 5-30 funcs | >40 funcs | 15% |
| Fan-out (contexts called) | 1-4 | >6 | 20% |
| Fan-in (called by contexts) | 1-6 | >10 | 15% |
| Circular dependencies | 0 | >0 | 15% |
| Boundary violations | 0 | >0 | 15% |

### Commands for Assessment

Use Glob to count `.ex` files per context directory under `lib/my_app/*/`.
Use Grep to count public function definitions per context file under `lib/my_app/*.ex`.
Run `mix xref graph --format stats` for dependency analysis.
Run `mix xref graph --format cycles --label compile` for compile-time circular dependencies.

### Output Format

```markdown
## Context Health Assessment

### Overall Score: 82/100 (Good)

| Context | Modules | API | Fan-Out | Fan-In | Score |
|---------|---------|-----|---------|--------|-------|
| Accounts | 5 | 12 | 2 | 4 | 95 |
| Orders | 18 | 45 | 8 | 3 | 62 |
| Shared | 2 | 8 | 0 | 12 | 78 |

### Issues Found

1. **Orders** - Too large (18 modules, 45 funcs)
   - Consider: Extract Fulfillment, Invoicing sub-contexts

2. **Orders** - High fan-out (8 contexts)
   - Consider: Review if all dependencies necessary

### Recommendations

- Split Orders into Orders + Fulfillment
- Review Accounts ← Billing dependency
```

## Iron Laws - Never Violate These

1. **Controllers call only contexts** - No direct Repo access from web layer
2. **Schemas are pure data** - No side effects, no Repo calls in schema modules
3. **Contexts own their schemas** - Don't import schemas from other contexts
4. **Explicit dependencies only** - Cross-context calls must be intentional
5. **DO NOT refactor context boundaries without running `mix xref` first** — Refactoring without dependency data creates new violations; always map the dependency graph before moving modules

## Dependency Rules

| Layer | Can Call | Cannot Call |
|-------|----------|-------------|
| Controllers | Contexts, Plug, Conn | Repo, Schemas directly |
| LiveViews | Contexts, Components, PubSub | Repo, Schemas directly |
| Contexts | Own schemas, Repo, other contexts | Web layer modules |
| Schemas | Ecto types, validations | Contexts, Repo |

## Analysis Commands

### Check Compile Dependencies

Run `mix xref graph --label compile-connected`.

### Find What Depends on a Context

Run `mix xref graph --sink MyApp.Accounts --label compile`.

### Find What a Module Calls

Run `mix xref callers MyApp.Accounts.get_user!/1`.

### Check for Circular Dependencies

Run `mix xref graph --format cycles --label compile`.

## Red Flags to Detect

| Issue | Detection Command | Fix |
|-------|------------------|-----|
| Repo in web layer | `grep -r "Repo\." lib/my_app_web/` | Move to context |
| Schema with queries | `grep -r "import Ecto.Query" lib/my_app/**/schemas/` | Move queries to context |
| Cross-context schema import | `grep -r "alias MyApp.Other.Schema" lib/my_app/ctx/` | Call context API |
| Business logic in LiveView | `grep -r "Repo\.\|Ecto\.Multi" lib/my_app_web/live/` | Extract to context |

## Boundary Verification Process

1. Run `mix xref graph --label compile-connected` for overview
2. Check for context cross-contamination
3. Verify no direct Repo calls from web layer
4. Ensure schemas have no side effects
5. Validate explicit cross-context dependencies

## Next Steps

Always end with actionable follow-up — findings without a plan
get lost:

```
- `/phx:plan` — Create a plan to fix violations (recommended for 3+ issues)
- `/phx:quick` — Fix a single boundary violation directly
- `/phx:review` — Review specific modules for deeper issues
```

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/context-design.md` - Context design principles
- `${CLAUDE_SKILL_DIR}/references/refactoring-boundaries.md` - Fixing boundary violations
