---
name: refactor
description: Safe refactoring with test guard — improve code quality without changing behavior
triggers: [refactor, cleanup, restructure, simplify, extract function, improve code quality]
context_cost: low
---

# Refactor Skill

## Goal
Improve code structure, readability, or maintainability while guaranteeing that all existing behavior is preserved. Tests are the safety net — if they fail after refactoring, the refactor was incorrect.

## Steps

1. **Establish the safety net**
   - Run the full test suite: `[test command from AGENTS.md]`
   - If tests fail before you start: STOP — fix the failing tests first (they're not a safe net)
   - Record baseline: number of passing tests, coverage %

2. **Identify the refactoring target**
   - What specific code smell is being addressed?
   - Common targets:
     - Function too long (> 30 lines) → Extract Function
     - Class too large (> 500 lines) → Extract Class / Split by Responsibility
     - Duplicated logic (> 3 occurrences) → Extract Method/Module
     - Magic numbers/strings → Extract Constants
     - Deep nesting (> 3 levels) → Early Returns / Extract Method
     - God class → Decompose to smaller, focused classes
     - Long parameter list → Introduce Parameter Object

3. **Apply ONE refactoring at a time**
   - Make the smallest possible change
   - Run tests immediately after each change
   - If tests fail: REVERT the change (don't try to fix tests and refactor simultaneously)

4. **Common refactoring patterns**

   **Extract Function:**
   ```typescript
   // Before: complex inline logic
   function processOrder(order) {
     // 40 lines of validation + calculation + notification
   }

   // After: extracted with clear names
   function processOrder(order) {
     validateOrder(order);
     const total = calculateTotal(order);
     notifyUser(order, total);
   }
   ```

   **Early Returns (reduce nesting):**
   ```typescript
   // Before: deeply nested
   function getDiscount(user) {
     if (user) {
       if (user.isPremium) {
         if (user.yearsActive > 5) {
           return 0.3;
         }
       }
     }
     return 0;
   }

   // After: early returns
   function getDiscount(user) {
     if (!user) return 0;
     if (!user.isPremium) return 0;
     if (user.yearsActive <= 5) return 0;
     return 0.3;
   }
   ```

   **Extract Constants:**
   ```typescript
   // Before: magic numbers
   if (attempts > 3) lockAccount(15 * 60 * 1000);

   // After: named constants
   const MAX_LOGIN_ATTEMPTS = 3;
   const LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutes
   if (attempts > MAX_LOGIN_ATTEMPTS) lockAccount(LOCKOUT_DURATION_MS);
   ```

5. **After each refactoring step**
   - Run: `[test command]` → must pass
   - Run: `[typecheck command]` → must pass
   - Run: `[lint command]` → must pass
   - Check: complexity still < 10? Length still < 30 lines?

6. **Check architecture boundaries** (agentic-linter)
   - After significant structural changes: run agentic-linter skill
   - Ensure no new circular dependencies introduced

7. **Final verification**
   - Baseline tests passing count matches post-refactor count
   - Coverage has not decreased
   - No new lint errors or type errors

## Constraints
- NEVER change behavior during refactoring (only structure)
- NEVER refactor without a passing test suite as safety net
- NEVER combine refactoring with feature addition in the same commit
- If a refactor requires fixing tests: stop, analyze whether the tests or the logic is wrong

## Output Format
Report: "Refactored [target]. All [N] tests still passing. Coverage: [X]%. Complexity reduced from [A] to [B]."
