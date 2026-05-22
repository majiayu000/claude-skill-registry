---
name: security-quick-scan
description: Scan code or configuration for common security issues. Use when a mid-level developer needs a quick security pass.
---

# Security Quick Scan

## Purpose
Scan code or configuration for common security issues.

## Inputs to request
- Code or config diff.
- Auth and data handling flow.
- Threat model or risk level.

## Workflow
1. Check auth, input validation, and secret handling.
2. Identify risky dependencies or outdated crypto.
3. Recommend immediate fixes and follow-ups.

## Output
- Security findings with severity tags.

## Quality bar
- Prioritize issues by impact and likelihood.
- Separate quick wins from larger remediations.
