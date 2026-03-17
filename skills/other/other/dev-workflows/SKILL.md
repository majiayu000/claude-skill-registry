---
name: dev-workflows
description: Use when running builds, executing tests, or improving developer experience workflows - provides structured guidance for build/test execution and DX improvement.
---

# Dev Workflows

## Overview
Unify build, test, and DX improvement workflows so they are repeatable and reliable. Focus on safe execution, clear diagnostics, and actionable follow-ups.

## When to Use
- Running builds or resolving build failures
- Executing tests or analyzing test failures
- Improving onboarding, tooling, or developer workflows

Avoid when:
- The task is pure code implementation
- A full release process is required (use release-prep)

## Quick Reference

| Task | Load reference |
| --- | --- |
| Build workflows | `skills/dev-workflows/references/build.md` |
| Test workflows | `skills/dev-workflows/references/test.md` |
| DX improvements | `skills/dev-workflows/references/dx.md` |

## Workflow
1. Select the workflow type: build, test, or DX.
2. Load the matching reference file.
3. Execute with monitoring and capture diagnostics.
4. Apply fixes or improvements as needed.
5. Verify outcomes and document next steps.

## Output
- Execution summary (status, errors, next steps)
- Suggested follow-ups or improvements

## Common Mistakes
- Skipping baseline environment checks
- Running tests without capturing failing output
- Changing DX workflows without documenting impact
