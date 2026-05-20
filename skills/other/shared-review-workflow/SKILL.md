---
name: shared-review-workflow
description: Severity definitions, approval gate protocol, and fix constraints shared across all review and test skills.
---

## Purpose

Define the common review workflow shared by code-review, design-review, and unit-test skills across all platforms.

## Severity definitions

| Severity     | Meaning                                                         |
| ------------ | --------------------------------------------------------------- |
| must-fix     | Security vulnerability, broken functionality, blocks deployment or App Store submission |
| should-fix   | Standards violation, maintainability concern, tech debt         |
| nice-to-have | Style preference, minor improvement, optional optimization      |

## Approval gate

If issues are found and `--no-fix` is not set:

> "Found X issues (Y must-fix). Approve fixes? (yes/no)"

Do not modify code before approval.

## Fix and confirm (if approved)

- Apply fixes
- Re-run automated gates (lint, format, typecheck)
- Run unit tests to confirm no regressions
- Report final status

## Fix constraints

- Don't add dependencies unless required
- Don't weaken assertions to make tests pass
- Prefer targeted fixes over broad refactors
- Don't disable or skip tests to make them pass
