---
name: code-simplifier
version: 2.0.0
description: '[Code Quality] Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise.'
allowed-tools: Read, Edit, Glob, Grep, Task
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

## Quick Summary

**Goal:** Simplify and refine code for clarity, consistency, and maintainability while preserving all functionality.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Identify Targets** — Recent git changes or specified files (skip generated/vendor)
2. **Analyze** — Find complexity hotspots (nesting >3, methods >20 lines), duplicates, naming issues
3. **Apply Simplifications** — One refactoring type at a time following KISS/DRY/YAGNI
4. **Verify** — Run related tests, confirm no behavior changes

**Key Rules:**

- Preserve all existing functionality; no behavior changes
- Follow platform patterns (Entity expressions, fluent helpers, project store base (search for: store base class), BEM)
- Keep tests passing after every change

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

3. **Apply simplifications**
    - One refactoring type at a time
    - Preserve all functionality
    - Follow platform patterns

4. **Verify**
    - Run related tests if available
    - Confirm no behavior changes

## Platform Patterns

### Backend (C#)

- Extract to `Entity.XxxExpr()` static expressions
- Use fluent helpers: `.With()`, `.Then()`, `.PipeIf()`
- Move mapping to DTO `MapToObject()` / `MapToEntity()`
- Use `PlatformValidationResult` fluent API
- Check entity expressions have database indexes
- Verify document database index methods exist for collections

### Frontend (TypeScript)

- Use `project store base (search for: store base class)` for state management
- Apply `untilDestroyed()` to all subscriptions
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
