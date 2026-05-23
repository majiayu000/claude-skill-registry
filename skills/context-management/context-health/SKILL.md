---
name: context-health
description: Use when validating or diagnosing the cortex environment (consistency, duplicates, redundancy, optimization) - provides a diagnostic workflow and reporting structure for context health checks.
---

# Context Health

## Overview
Provide a consistent diagnostic workflow for cortex environments: verify config integrity, detect duplicates, surface redundancies, and report actionable issues.

## When to Use
- Checking system health after changes to agents, modes, or rules
- Troubleshooting unexpected cortex behavior
- Performing periodic maintenance checks

Avoid when:
- The task is unrelated to cortex configuration or context

## Quick Reference

| Task | Load reference |
| --- | --- |
| Environment diagnostics | `skills/context-health/references/doctor.md` |

## Workflow
1. Confirm target scope and environment.
2. Load the diagnostics reference.
3. Run checks and gather findings.
4. Summarize issues by severity.
5. Recommend fixes and next steps.

## Output
- Diagnostic report with severity levels
- Recommended fixes or follow-up actions

## Common Mistakes
- Running fixes without reviewing findings
- Skipping context scope verification
