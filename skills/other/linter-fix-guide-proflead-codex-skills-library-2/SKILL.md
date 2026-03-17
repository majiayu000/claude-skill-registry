---
name: linter-fix-guide
description: Explain lint errors and propose fixes. Use when a junior developer needs help resolving common lint or format warnings.
---

# Linter Fix Guide

## Purpose
Explain lint errors and propose fixes.

## Inputs to request
- Lint rule name and full message.
- Relevant code snippet and file path.
- Project lint config if nonstandard.

## Workflow
1. Summarize the lint error in plain language.
2. Point to the line or pattern and the expected style.
3. Provide a corrected snippet or refactor suggestion.

## Output
- Plain-language explanation.
- Suggested code change.

## Quality bar
- Match the repository style guide.
- Keep changes minimal and localized.
