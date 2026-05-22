---
name: tdd-plan-review
description: Review and reorder existing implementation plans to follow TDD methodology. Use when user has a plan that puts implementation before tests, or when validating plan structure for TDD compliance. Reorganizes steps to ensure test-first approach.
---

# TDD Plan Review

既存の実装計画をレビューし、TDD順序に並べ替えます。

## Review Process

1. **Analyze current plan structure**
   - Identify where test files are mentioned
   - Identify where implementation files are mentioned

2. **Check TDD compliance**
   - Are tests listed before implementation? ✅ or ❌
   - Is Step 1 about writing tests? ✅ or ❌
   - Are phases (Red/Green/Refactor) labeled? ✅ or ❌

3. **Reorder if needed**
   - Move test-related steps to the beginning
   - Add phase labels (Red/Green/Refactor)
   - Ensure verification comes last

## Before/After Example

### Before (Non-TDD)
```
Step 1: Interface Layer      ← implementation first
Step 2: Implementation Layer ← more implementation
Step 3: Use Case Layer       ← still implementation
Step 4: Test Files           ← tests last (WRONG)
```

### After (TDD)
```
Step 1: Test Files (Red Phase)     ← tests FIRST
Step 2: Implementation (Green Phase)
Step 3: Verification (Refactor Phase)
```

## Output Format

After review, provide:
1. TDD Compliance: ✅ or ❌
2. Issues found (if any)
3. Reordered plan (if needed)
