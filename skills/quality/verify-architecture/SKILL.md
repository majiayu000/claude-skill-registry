---
name: verify-architecture
description: Run architecture compliance checks for BioETL (quick/full/category modes) before commit or PR.
---

# Verify Architecture

## Objective
Execute architecture validation checks and report blocking/non-blocking issues.

## Source Of Truth
- Primary instructions: `../../../.claude/skills/verify-architecture.md`

## Workflow
1. Open and follow `../../../.claude/skills/verify-architecture.md`.
2. Select mode (`quick`, `full`, `category`) based on request scope.
3. Adapt command examples to the active shell and installed toolchain.
4. Report findings with failing tests/checks and actionable next fixes.

## Notes
- The `.claude` skill file is canonical for test groupings and command sets.
