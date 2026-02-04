---
name: class-refactoring
description: PHP/Laravel code simplification and refactoring specialist. Use when the user wants to refactor, simplify, or improve PHP/Laravel code clarity, maintainability, or consistency.
---

# Class Refactoring

**Role:** PHP/Laravel code simplification specialist. Enhance clarity, consistency, and maintainability while preserving exact functionality.

**Constraint:** Change how, not what. Preserve functionality.

---

## 1. Process

**Do (in order):**
1. Review all `.cursor/rules/*.mdc` rules.
2. Analyze the class and complete the TODO list tasks.
3. Verify code coverage after refactoring.
4. Preserve functionality — change how, not what.
5. Focus on recently modified code unless instructed otherwise.

---

## 2. Anti-patterns to Avoid

**Do not:**
- Over-simplify in a way that reduces clarity.
- Use overly clever or dense solutions.
- Combine too many concerns.
- Remove helpful abstractions.
- Prioritize fewer lines over readability.
- Use nested ternaries — prefer `match`, `switch`, or `if`/`else`.

---

## 3. Code Quality

**Apply:**
- Clean, modern, optimized code.
- Stateless PHP classes.
- Collections over `foreach` where appropriate.
- PHPDoc for PHPStan analysis.
- English comments only.
- Spatie DTOs instead of arrays (except Job constructors).
- Laravel helpers over native PHP when appropriate.

---

## 4. Architecture

**Apply:**
- DRY principle — eliminate duplicates.
- Remove obvious comments; keep PHPStan-relevant docs.
- Single Responsibility Principle.
- Extract private methods if body exceeds ~30 lines.
- No single-use variables.

---

## 5. Tests & PHPStan

**Do:**
- Match test variable names to actual use cases.
- Improve iterable shapes for PHPStan.
- New tests must cover relevant code.
- Remove coverage files after verification.

**Do not:** Modify existing tests (unless refactoring requires it for consistency).
