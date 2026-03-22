---
name: code-simplifier
version: 2.0.0
description: '[Code Quality] Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise.'
allowed-tools: Read, Edit, Glob, Grep, Task
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `.claude/skills/shared/design-patterns-quality-checklist.md` — Design pattern opportunities, anti-pattern detection, DRY/abstraction enforcement
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

## Quick Summary

**Goal:** Simplify and refine code for clarity, consistency, and maintainability while preserving all functionality.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `docs/project-reference/code-review-rules.md` — anti-patterns, review checklists, quality standards **(READ FIRST)**
> - `project-structure-reference.md` — project patterns and structure
>
> If files not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Identify Targets** — Recent git changes or specified files (skip generated/vendor)
2. **Analyze** — Find complexity hotspots (nesting >3, methods >20 lines), duplicates, naming issues
3. **Apply Simplifications** — One refactoring type at a time following KISS/DRY/YAGNI
4. **Verify** — Run related tests, confirm no behavior changes

**Key Rules:**

- Preserve all existing functionality; no behavior changes
- Follow platform patterns (Entity expressions, fluent helpers, project store base (search for: store base class), BEM)
- Keep tests passing after every change

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

# Code Simplifier Skill

Simplify and refine code for clarity, consistency, and maintainability.

## Usage

```
/code-simplifier                    # Simplify recently modified files
/code-simplifier path/to/file.ts    # Simplify specific file
/code-simplifier --scope=function   # Focus on function-level simplification
```

## Simplification Mindset

**Be skeptical. Verify before simplifying. Every change needs proof it preserves behavior.**

- Do NOT assume code is redundant — verify by tracing call paths and reading implementations
- Before removing/replacing code, grep for all usages to confirm nothing depends on the current form
- Before flagging a convention violation, grep for 3+ existing examples — codebase convention wins
- Every simplification must include `file:line` evidence of what was verified
- If unsure whether simplification preserves behavior, do NOT apply it

## What It Does

1. **Analyzes** code for unnecessary complexity
2. **Identifies** opportunities to simplify without changing behavior
3. **Applies** KISS, DRY, and YAGNI principles
4. **Preserves** all existing functionality
5. **Follows convention** — grep for 3+ existing patterns before applying simplifications

## Readability Checklist (MUST evaluate)

Before finishing, verify the code is **easy to read, easy to maintain, easy to understand**:

- **Schema visibility** — If a function computes a data structure (object, map, config), add a comment showing the output shape so readers don't have to trace the code
- **Non-obvious data flows** — If data transforms through multiple steps (A → B → C), add a brief comment explaining the pipeline
- **Self-documenting signatures** — Function params should explain their role; remove unused params
- **Magic values** — Replace unexplained numbers/strings with named constants or add inline rationale
- **Naming clarity** — Variables/functions should reveal intent without reading the implementation

## Simplification Targets

- Redundant code paths
- Over-engineered abstractions
- Unnecessary comments (self-documenting code preferred)
- Complex conditionals that can be flattened
- Verbose patterns that have simpler alternatives

## Execution

Use the `code-simplifier:code-simplifier` subagent:

```
Task(subagent_type="code-simplifier:code-simplifier", prompt="Review and simplify [target files]")
```

## Examples

**Before:**

```typescript
function getData() {
    const result = fetchData();
    if (result !== null && result !== undefined) {
        return result;
    } else {
        return null;
    }
}
```

**After:**

```typescript
function getData() {
    return fetchData() ?? null;
}
```

## Workflow

1. **Identify targets**
    - If no arguments: `git diff --name-only HEAD~1` for recent changes
    - If arguments provided: use specified files/patterns
    - Skip: generated code, migrations, vendor files

2. **Analyze each file**
    - Identify complexity hotspots (nesting > 3, methods > 20 lines)
    - Find duplicated code patterns
    - Check naming clarity

3. **Design Pattern Assessment** (per `design-patterns-quality-checklist.md`)
    - **DRY/Abstraction:** Flag duplicate patterns extractable to base class, generic, or helper
    - **Right Responsibility:** Verify logic is in lowest appropriate layer (Entity > Service > Component)
    - **Pattern Opportunities:** Check for creational/structural/behavioral pattern opportunities (switch→Strategy, scattered new→Factory, etc.)
    - **Anti-Patterns:** Flag God Objects, Copy-Paste, Circular Dependencies, Singleton overuse
    - **Guard against over-engineering:** Only recommend patterns with evidence of 3+ occurrences of the problem

4. **Apply simplifications**
    - One refactoring type at a time
    - Preserve all functionality
    - Follow platform patterns

5. **Verify**
    - Run related tests if available
    - Confirm no behavior changes

## Project Patterns

### Backend

- Extract to entity static expressions (search for: entity expression pattern)
- Use fluent helpers (search for: fluent helper pattern in docs/project-reference/backend-patterns-reference.md)
- Move mapping to DTO mapping methods (search for: DTO mapping pattern)
- Use project validation fluent API (see docs/project-reference/backend-patterns-reference.md)
- Check entity expressions have database indexes
- Verify document database index methods exist for collections

> **[IMPORTANT] Database Performance Protocol (MANDATORY):**
>
> 1. **Paging Required** — ALL list/collection queries MUST use pagination. NEVER load all records into memory. Verify: no unbounded `GetAll()`, `ToList()`, or `Find()` without `Skip/Take` or cursor-based paging.
> 2. **Index Required** — ALL query filter fields, foreign keys, and sort columns MUST have database indexes configured. Verify: entity expressions match index field order, database collections have index management methods, migrations include indexes for WHERE/JOIN/ORDER BY columns.

### Frontend

- Use `project store base (search for: store base class)` for state management
- Apply subscription cleanup pattern (search for: subscription cleanup pattern) to all subscriptions
- Ensure BEM class naming on all template elements
- Use platform base classes (`project base component (search for: base component class)`, `project store component base (search for: store component base class)`)

## Constraints

- **Preserve functionality** — No behavior changes
- **Keep tests passing** — Verify after changes
- **Follow patterns** — Use platform conventions
- **Document intent** — Add comments only where non-obvious
- **Doc staleness** — After simplifications, cross-reference changed files against related docs (feature docs, test specs, READMEs); flag any that need updating

## Related

- `code-review`
- `refactoring`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `quality-audit` workflow** (Recommended) — code-simplifier → review-changes → code-review
> 2. **Execute `/code-simplifier` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/review-changes (Recommended)"** — Review all changes before commit
- **"/code-review"** — Full code review
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
