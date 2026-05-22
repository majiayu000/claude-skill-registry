---
name: defense-in-depth
description: Multi-layer validation to catch bugs before they escape
version: 1.0.0
author: Ariff
when_to_use: When making changes - validate at multiple layers
---

# Defense in Depth

## Philosophy

```
MULTIPLE INDEPENDENT VALIDATION LAYERS
Each layer catches what others miss
```

One check can fail silently. Four layers rarely do.

## The Four Layers

### Layer 1: Type/Syntax
```
What: Static analysis, types, linting
Catches: Typos, syntax errors, type mismatches
Run: First, before anything else
```

### Layer 2: Unit Tests
```
What: Individual function/module tests
Catches: Logic errors, edge cases, regressions
Run: After each code change
```

### Layer 3: Integration Tests
```
What: Component interaction tests
Catches: Interface mismatches, data flow errors
Run: After unit tests pass
```

### Layer 4: End-to-End
```
What: Full system tests, user scenarios
Catches: Missing requirements, workflow bugs
Run: Before claiming complete
```

## The Pipeline

```
Code Change
    ↓
[Layer 1: Lint/Type Check]
    ↓ PASS?
[Layer 2: Unit Tests]
    ↓ PASS?
[Layer 3: Integration Tests]
    ↓ PASS?
[Layer 4: E2E / Manual Check]
    ↓ PASS?
Done
```

**Fail at any layer → FIX before proceeding**

## Why Every Layer Matters

| Without This Layer | What Escapes |
|-------------------|--------------|
| No type checks | Undefined calls crash at runtime |
| No unit tests | Logic bugs slip through |
| No integration | Components don't work together |
| No E2E | User workflows broken |

## Implementation Patterns

### For Code Changes
```
1. Make change
2. Run linter immediately
3. Run affected unit tests
4. Run integration suite
5. Test the actual feature
```

### For Bug Fixes
```
1. Write failing test first
2. Fix the bug
3. Run all tests (regression check)
4. Verify original symptom gone
```

### For New Features
```
1. Write unit tests for new logic
2. Implement feature
3. Add integration tests
4. Verify against requirements
```

## Layer-Specific Commands

Configure per project:

```yaml
layer_1:
  command: "npm run lint && npm run typecheck"
  when: "On save, before commit"
  
layer_2:
  command: "npm run test:unit"
  when: "After code changes"
  
layer_3:
  command: "npm run test:integration"
  when: "After unit tests pass"
  
layer_4:
  command: "npm run test:e2e"
  when: "Before claiming done"
```

## Recovery Procedures

### Layer 1 Fails
```
→ Syntax/type error in your code
→ Fix immediately, don't proceed
→ Never commit with lint errors
```

### Layer 2 Fails
```
→ Logic error or regression
→ Check: Did you break something?
→ Check: Is your new test wrong?
→ Fix root cause, not symptoms
```

### Layer 3 Fails
```
→ Interface/contract broken
→ Check: API changes?
→ Check: State management issues?
→ May need to update multiple files
```

### Layer 4 Fails
```
→ User-visible problem
→ Trace back through layers
→ Ask: Which layer SHOULD have caught this?
→ Add test to that layer
```

## Integration with Checker Agents

- `pre-action-verifier` → Runs before each layer
- `assumption-checker` → Validates test assumptions
- `scope-boundary-checker` → Ensures tests cover scope
- `rollback-planner` → Ready if pipeline fails
