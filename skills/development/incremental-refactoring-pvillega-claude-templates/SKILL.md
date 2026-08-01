---
name: incremental-refactoring
description: 'Use when IMPLEMENTING refactoring changes. Enforces metrics-driven protocol
  with before/after measurements. Triggers: "implement refactor", "apply refactoring
  pattern", "clean up code smell", "extract'
---

---
name: incremental-refactoring
description: Use when IMPLEMENTING refactoring changes. Enforces metrics-driven protocol with before/after measurements. Triggers: "implement refactor", "apply refactoring pattern", "clean up code smell", "extract method", "move method". No exceptions for "simple" refactorings - use this. NOTE: If you need to FIND duplicates first, use duplicate-code-detector, then return here for implementation.
---

# Incremental Refactoring

## Workflow Clarification: Detection vs Implementation

This skill is for **IMPLEMENTATION** (applying refactoring patterns). If you don't yet know what to refactor:
- Use `duplicate-code-detector` first to identify duplication targets
- Then return here to implement the changes

**Sequential workflow:**
1. `duplicate-code-detector` → Find and prioritize targets (if needed)
2. `incremental-refactoring` → Implement changes with metrics (this skill)

## MANDATORY FIRST STEP

**TodoWrite:** Create 10+ items (2 per step)
1. Baseline metrics (complexity, duplication, coverage)
2. Select ONE refactoring pattern
3. Apply transformation atomically
4. Validate preservation (tests, linter, metrics)
5. Document + commit

**This skill is MANDATORY for any refactoring work.**

---

## 5-Step Process

### 1. Baseline Metrics (BEFORE changes)
- Cyclomatic complexity: ___
- Maintainability index: ___
- Duplication %: ___
- Test coverage: ___%

### 2. Select ONE Pattern
Pick ONE per iteration (Extract Method, Move Method, Replace Conditional with Polymorphism, Introduce Parameter Object, etc.)

### 3. Apply Transformation
- ONE small change
- Preserve existing behavior exactly
- **No new features during refactoring**

### 4. Validate Preservation (MANDATORY)
- [ ] ALL tests pass (zero changes)
- [ ] Tests fail → **Revert immediately** (no debugging during refactoring)
- [ ] Re-measure complexity → improvement %
- [ ] Linter/type checker pass

### 5. Document Change
- Pattern applied + rationale
- Before/after metrics
- Commit with descriptive message

---

## Response Templates

**"Big rewrite is faster"**
> 80% of big rewrites fail or get abandoned. Incremental refactoring delivers value continuously, reduces risk, and keeps tests green. Which specific smell are we addressing first?

---

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll refactor multiple patterns at once" | Can't isolate what breaks |
| "Tests are slow, I'll skip for now" | 60% chance you break behavior |
| "Mix refactor + new feature" | Can't revert cleanly when it fails |
