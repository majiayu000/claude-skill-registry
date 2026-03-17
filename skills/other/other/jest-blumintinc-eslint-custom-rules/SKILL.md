---
name: jest
description: "Use when implementing or expanding ESLint rule test suites."
user-invocable: false
---

Given an ESLint rule implementation (e.g., `src/rules/my-rule.ts`), implement or update a comprehensive Jest test suite in `src/tests/` (e.g., `src/tests/my-rule.test.ts`). The suite must achieve high code coverage (90% minimum, 100% preferred) and pass all checks.

## Purpose

Ensure every rule ships with a thorough, repeatable test suite that prevents false positives, catches regressions, and documents expected behavior.

## Why the System Was Built

Reliable rule tests keep 100+ custom rules stable across refactors and TypeScript upgrades by codifying expected diagnostics, auto-fixes, and edge cases.

## Definitions

- **RuleTester**: Harness that runs lint cases against a rule and asserts reported errors/fixes.
- **Valid case**: Code that must NOT trigger the rule (guards against false positives).
- **Invalid case**: Code that MUST trigger the rule with expected `messageId` (prevents false negatives and verifies fixes).
- **Coverage target**: 90% minimum, 100% preferred across rule logic and fixers.

## Core Components

- `ruleTesterTs`, `ruleTesterJsx`, `ruleTesterJson` from `src/utils/ruleTester.ts` for TS, JSX/React, and JSON rules.
- Jest with `ts-jest` for executing suites.
- Auto-fix assertions via `output` in invalid cases when the rule is fixable.

## Directory Structure

- Tests live in `src/tests/`, mirroring rule filenames (`src/rules/foo.ts` → `src/tests/foo.test.ts`).
- RuleTester utilities: `src/utils/ruleTester.ts`.
- Coverage output: `coverage/`.

## Setup and Execution

- Run all tests: `npm test`
- Run a single suite: `npx jest src/tests/<rule>.test.ts`

## Test Case Patterns

```typescript
import { ruleTesterTs, ruleTesterJsx, ruleTesterJson } from '../utils/ruleTester';
import { myRule } from '../rules/my-rule';

// TypeScript rules
ruleTesterTs.run('my-rule', myRule, { valid: [], invalid: [] });

// React/JSX rules
ruleTesterJsx.run('my-rule', myRule, { valid: [], invalid: [] });

// JSON rules
ruleTesterJson.run('my-rule', myRule, { valid: [], invalid: [] });
```

### ✅ Valid Cases (false-positive prevention)
- Good patterns that must NOT report.
- Include similar-but-correct code and ignored paths.

```typescript
valid: [
  'const x = 1;',
  { code: 'const x = 1;', filename: 'src/utils/math.ts', options: [{ allow: true }] },
]
```

### ❌ Invalid Cases (false-negative prevention)
- Violations that MUST report with the right `messageId`.
- Provide `output` when verifying auto-fix.

```typescript
invalid: [
  {
    code: 'const x = var;',
    errors: [{ messageId: 'unexpectedVar' }],
    output: 'const x = fixedVar;',
  },
]
```

## Usage Instructions

1) Analyze the rule (targets, visitors, edge cases).
2) Select the correct tester variant.
3) Draft cases: 10+ valid and 10+ invalid, covering nested and tricky syntax.
4) Run `npx jest src/tests/<rule>.test.ts`.
5) Refine until coverage ≥90% and all assertions pass.
6) Keep fixes minimal and focused on requested behavior.

## How It Makes Developers' Lives Easier

- Prevents regressions when refactoring rules or upgrading TypeScript/ESLint.
- Documents expected diagnostics and fixes for future contributors.
- Speeds debugging by localizing failures to a single rule suite.

## Critical Insights for Maintainers

- Test the intent: `messageId` should match the rule's purpose.
- Use filenames when rule behavior depends on file type/path.
- Always assert `output` for fixable rules to guard against unsafe fixes.
