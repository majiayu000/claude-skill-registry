---
name: refactoring
description: |
  Technical debt remediation and code restructuring workflow. Use when improving
  code structure, reducing complexity, extracting abstractions, or paying down
  accumulated technical debt.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Refactoring Skill

Structured approach to technical debt remediation. Improve code structure while maintaining behavior through incremental, safe changes.

---

## When to Use

| Trigger | Description |
|---------|-------------|
| **Guardrail Violations** | Functions >50 lines, files >300 lines |
| **Complexity Threshold** | Cyclomatic complexity >10 |
| **Code Duplication** | Same logic in 3+ places |
| **Quarterly Review** | Regular technical debt assessment |
| **Pre-Feature** | Before adding features to messy code |
| **Post-Incident** | After bugs caused by confusing code |

---

## Refactoring Principles

### Golden Rules

1. **Behavior Preservation**: Output unchanged after refactoring
2. **Small Steps**: One change at a time
3. **Test First**: Ensure tests exist before changing
4. **Incremental**: Commit after each successful change
5. **Reversible**: Easy to roll back if issues arise

### When NOT to Refactor

- During active incident response
- Without test coverage
- When deadline is imminent
- If no clear improvement goal

---

## Prerequisites

Before starting:

- [ ] Code compiles and all tests pass
- [ ] Test coverage exists for target code (>60%)
- [ ] Clear refactoring goal defined
- [ ] Time allocated (refactoring always takes longer)
- [ ] Git working directory is clean

---

## Refactoring Process

```
Phase 1: Identify Candidates
    ↓
Phase 2: Impact Analysis
    ↓
Phase 3: Plan Refactoring
    ↓
Phase 4: Add Safety Net
    ↓
Phase 5: Execute Incrementally
    ↓
Phase 6: Validate & Document
```

---

## Phase 1: Identify Candidates

### 1.1 Automated Detection

**Long Functions** (>50 lines):
```bash
# Find functions over 50 lines (varies by language)
# Example: use linter rules or IDE features
```

**Long Files** (>300 lines):
```bash
# Find files over 300 lines
find src -name "*.ts" -exec wc -l {} \; | awk '$1 > 300'
find src -name "*.py" -exec wc -l {} \; | awk '$1 > 300'
```

**High Complexity**:
```bash
# Use complexity analyzers
npx escomplex src/**/*.ts
python -m mccabe src/**/*.py
```

### 1.2 Code Smells

| Smell | Signs | Priority |
|-------|-------|----------|
| **Long Method** | >50 lines, multiple responsibilities | High |
| **Large Class** | >300 lines, low cohesion | High |
| **Feature Envy** | Method uses other class more than own | Medium |
| **Data Clumps** | Same group of variables together | Medium |
| **Primitive Obsession** | Overuse of primitives vs objects | Medium |
| **Switch Statements** | Large switch blocks | Low |
| **Speculative Generality** | Unused abstractions | Low |

### 1.3 Candidate List

Document identified candidates:

```markdown
## Refactoring Candidates

### High Priority
| File | Issue | Lines | Impact |
|------|-------|-------|--------|
| src/services/order.ts | Long method: processOrder | 120 → 50 | High |
| src/api/users.ts | Large file | 450 → 200 | High |
| src/utils/validation.ts | Duplication | N/A | Medium |

### Medium Priority
| File | Issue | Lines | Impact |
|------|-------|-------|--------|
| src/models/product.ts | Feature envy | N/A | Medium |
| src/services/email.ts | Complex conditionals | N/A | Medium |
```

---

## Phase 2: Impact Analysis

### 2.1 Dependency Mapping

For each candidate, identify:

```
Target: src/services/order.ts

Dependencies (imports from):
- src/models/order.ts
- src/services/inventory.ts
- src/services/payment.ts

Dependents (imported by):
- src/api/orders.ts
- src/workers/orderProcessor.ts
- tests/services/order.test.ts

Impact radius: 5 files
Risk level: Medium
```

### 2.2 Risk Assessment

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Test coverage | >80% | 60-80% | <60% |
| Dependents | <3 | 3-10 | >10 |
| Business criticality | Non-critical | Important | Critical path |
| Complexity | Simple rename | Extract method | Architecture change |

### 2.3 Risk Matrix

```
              Low Effort    High Effort
            ┌────────────┬────────────┐
High Value  │  DO FIRST  │  PLAN      │
            │            │  CAREFULLY │
            ├────────────┼────────────┤
Low Value   │  QUICK WIN │  AVOID     │
            │            │            │
            └────────────┴────────────┘
```

---

## Phase 3: Plan Refactoring

### 3.1 Choose Refactoring Technique

| Smell | Technique | Description |
|-------|-----------|-------------|
| Long method | Extract Method | Pull out logical chunks |
| Large class | Extract Class | Split by responsibility |
| Feature envy | Move Method | Move to appropriate class |
| Data clumps | Extract Parameter Object | Group related params |
| Duplicated code | Extract to shared function | DRY principle |
| Complex conditional | Replace with polymorphism | Strategy pattern |
| Long parameter list | Introduce Parameter Object | Create wrapper class |

### 3.2 Step-by-Step Plan

Example: Extract Method from Long Function

```markdown
## Refactoring Plan: processOrder()

### Goal
Reduce processOrder() from 120 lines to <50 lines

### Steps
1. [ ] Add characterization tests for current behavior
2. [ ] Extract validateOrder() (lines 15-35)
3. [ ] Verify tests pass
4. [ ] Commit: "refactor: extract validateOrder"
5. [ ] Extract calculateTotals() (lines 40-65)
6. [ ] Verify tests pass
7. [ ] Commit: "refactor: extract calculateTotals"
8. [ ] Extract processPayment() (lines 70-95)
9. [ ] Verify tests pass
10. [ ] Commit: "refactor: extract processPayment"
11. [ ] Extract sendConfirmation() (lines 100-115)
12. [ ] Verify tests pass
13. [ ] Commit: "refactor: extract sendConfirmation"
14. [ ] Final cleanup and documentation
15. [ ] Commit: "refactor: cleanup processOrder"

### Expected Result
- processOrder(): 120 → 25 lines
- New methods: 4
- Total lines: +10 (net increase for clarity)
```

---

## Phase 4: Add Safety Net

### 4.1 Characterization Tests

Before refactoring, add tests that capture current behavior:

```typescript
describe('processOrder - characterization tests', () => {
  it('should match current behavior for valid order', () => {
    const order = createValidOrder();
    const result = processOrder(order);

    // Capture current output exactly
    expect(result).toMatchSnapshot();
  });

  it('should match current behavior for edge cases', () => {
    const edgeCases = [
      createEmptyOrder(),
      createMaxItemOrder(),
      createDiscountedOrder(),
    ];

    edgeCases.forEach(order => {
      expect(processOrder(order)).toMatchSnapshot();
    });
  });
});
```

### 4.2 Coverage Check

Ensure adequate coverage before proceeding:

```bash
# Check coverage for target file
npm test -- --coverage --collectCoverageFrom="src/services/order.ts"
```

**Minimum Coverage**: 60% before refactoring (prefer >80%)

### 4.3 Checkpoint Commit

Create a checkpoint before starting:

```bash
git add .
git commit -m "chore: checkpoint before refactoring processOrder"
```

---

## Phase 5: Execute Incrementally

### 5.1 One Change at a Time

**Bad**: Multiple changes in one commit
```bash
# Too much at once - hard to debug if tests fail
git commit -m "refactor: refactor entire order module"
```

**Good**: Atomic changes
```bash
git commit -m "refactor(order): extract validateOrder method"
git commit -m "refactor(order): extract calculateTotals method"
git commit -m "refactor(order): extract processPayment method"
```

### 5.2 Red-Green-Refactor

For each change:

```
1. Run tests → PASS (green)
2. Make one refactoring change
3. Run tests → Should still PASS (green)
4. If FAIL (red) → Revert and try smaller change
5. If PASS → Commit
6. Repeat
```

### 5.3 Common Refactoring Patterns

See `references/process.md` for detailed code examples including:
- Extract Method pattern
- Extract Class pattern
- Replace Conditional with Polymorphism pattern

---

## Phase 6: Validate & Document

### 6.1 Final Validation

- [ ] All tests pass
- [ ] Coverage maintained or improved
- [ ] No new linter warnings
- [ ] Performance unchanged (or improved)
- [ ] Behavior identical (check snapshots)

### 6.2 Document Changes

**Update patterns.md** (if new pattern emerged):
```markdown
## Order Processing Pattern

Orders are processed through composable steps:
1. validateOrder() - Input validation
2. calculateTotals() - Price calculations
3. processPayment() - Payment handling
4. sendConfirmation() - Notifications
```

**Create memory entry** (if significant):
```markdown
# Refactoring: Order Processing

**Date**: 2025-01-15
**Files**: src/services/order.ts

## Before
- Single 120-line function
- Difficult to test
- Hard to modify

## After
- 5 focused functions (<30 lines each)
- Easier to test
- Clear responsibilities

## Lessons
- Extract Method is low-risk, high-reward
- Characterization tests prevented regressions
```

### 6.3 Final Commit

```bash
git add .
git commit -m "refactor(order): complete processOrder decomposition

- Extract validateOrder (20 lines)
- Extract calculateTotals (25 lines)
- Extract processPayment (30 lines)
- Extract sendConfirmation (20 lines)
- Main function now 25 lines (was 120)

No behavior changes. All tests passing."
```

---

## Refactoring Catalog

### Quick Reference

| Refactoring | When | Effort | Risk |
|-------------|------|--------|------|
| Rename | Unclear naming | Low | Low |
| Extract Method | Long function | Low | Low |
| Extract Variable | Complex expression | Low | Low |
| Inline | Over-abstraction | Low | Low |
| Extract Class | Large class | Medium | Medium |
| Move Method | Feature envy | Medium | Medium |
| Extract Parameter Object | Long param list | Medium | Low |
| Replace Conditional with Polymorphism | Complex switch | High | Medium |
| Replace Inheritance with Composition | Rigid hierarchy | High | High |

### IDE Support

Most refactorings have IDE shortcuts:

| Action | VS Code | JetBrains |
|--------|---------|-----------|
| Rename | F2 | Shift+F6 |
| Extract Method | Ctrl+Shift+R | Ctrl+Alt+M |
| Extract Variable | Ctrl+Shift+R | Ctrl+Alt+V |
| Move | Drag or F2 | F6 |
| Inline | N/A | Ctrl+Alt+N |

---

## Checklist

### Before Refactoring
- [ ] Clear goal defined
- [ ] Tests exist (>60% coverage)
- [ ] Impact analysis complete
- [ ] Step-by-step plan created
- [ ] Checkpoint committed

### During Refactoring
- [ ] One change at a time
- [ ] Tests run after each change
- [ ] Commit after each successful change
- [ ] No behavior changes introduced

### After Refactoring
- [ ] All tests pass
- [ ] Coverage maintained
- [ ] Code cleaner (measurable)
- [ ] Documentation updated
- [ ] Patterns documented (if applicable)

---

## Related Resources

- **Workflows**: code-review.md, testing-strategy.md, troubleshooting.md
- **Detailed Examples**: See `references/process.md` for code patterns
- **Refactoring Book**: Martin Fowler's "Refactoring: Improving the Design of Existing Code"
