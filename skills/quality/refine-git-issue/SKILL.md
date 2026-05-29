---
name: refine-git-issue
description: Refine an existing GitHub issue for clarity and completeness; use when asked to improve an issue draft.
---

# Refine Git Issue

## Overview

Use this skill to polish an issue and fill missing details.

## Inputs

- Issue text or link
- Optional additional context

## Workflow

1. Identify gaps (repro steps, expected/actual, scope, affected files).
2. Verify relevant code paths with `rg` when possible.
3. Rewrite the issue for clarity and actionability.
4. Add questions or assumptions if information is missing.

## Output

- Improved issue text and a list of remaining unknowns.
