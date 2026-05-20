---
name: refactor-test-safety-net
description: "[Code Quality] Establishes test coverage requirements before refactoring. Use to identify missing tests, create minimal safety net tests, and define verification strategy for behavior preservation."
---

# Refactor: Test Safety Net

Ensure adequate test coverage before making changes.

## Pre-Refactoring Test Checklist

### 1. Coverage Assessment
- What's the current test coverage?
- Which paths are untested?

### 2. Test Types Needed
| Type | Purpose | When Required |
|------|---------|---------------|
| Unit | Function behavior | Always |
| Integration | Component interaction | Cross-module changes |
| Snapshot | UI/Output structure | View refactoring |
| Regression | Known bug prevention | Bug-prone areas |

### 3. Minimal Safety Net
Priority 1: Happy path test
Priority 2: Error handling test
Priority 3: Edge case test

## Rules

1. Never refactor without tests on the target code
2. Add tests BEFORE changes, not after
3. Characterization tests capture behavior, not correctness
4. Run tests after each small step