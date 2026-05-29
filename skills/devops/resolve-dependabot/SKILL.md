---
name: resolve-dependabot
description: Resolve Dependabot dependency updates locally; use when asked to handle dependency bumps or security updates.
---

# Resolve Dependabot

## Overview

Use this skill to apply dependency updates and keep the build green.

## Inputs

- Dependency update list or PR info (optional)

## Workflow

1. Identify dependency files (`package.json`, `requirements.txt`, etc.).
2. Apply updates and regenerate lockfiles.
3. Fix breaking changes or conflicts.
4. Run relevant tests and builds.
5. Summarize updated packages and risk notes.

## Output

- Updated dependency summary and test results.
