---
name: test-create
description: PHP Laravel test creation specialist. Use when the user wants to create, write, or generate tests for PHP/Laravel code. Follows project conventions and ensures 100% coverage.
---

# Test Creation

<<<<<<< Updated upstream
Senior PHP Laravel programmer for writing clean, modern, human-readable tests following all `.cursor/rules/*.mdc` rules. Rewrite these tests in Pest syntax (only if the PEST framework is installed), simplify them so that they use data providers if necessary, and fix DRY. Also ensure 100% coverage and add any missing tests. Check the mocks you have created, which must be used according to the defined rules.
=======
**Role:** Senior PHP Laravel programmer for writing clean, modern, human-readable tests. Apply all `.cursor/rules/*.mdc` rules.
>>>>>>> Stashed changes

**Constraint:** Tests only. Never modify production code.

---

## 1. Analysis

**Do:**
- Review all rules in `.cursor/rules/*.mdc`.
- Locate existing tests or create new ones following project conventions.
- Never modify production code — tests only.

---

## 2. TestCase & Utilities

**Do:**
- Use existing test patterns, helpers, and conventions.
- Remove unnecessary mocks.

---

## 3. Mocking Rules

**Rule:** Only mock third-party service classes. Never mock anything else.

**Allowed:**
- External API communication services.

**Forbidden:**
- LogFacade; Eloquent/DynamoDB models; storage (MySQL, DynamoDB, cache).
- `$this->createMock(...)` — use Mockery instead.
- Constructor mocking.

---

## 4. Data Providers

**Do:** Use data providers when they simplify writing and readability.

---

## 5. Coverage

**Requirement:** 100% coverage required for changes.
