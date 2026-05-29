---
name: task-direction-approval
description: Use when considering switching libraries/tools, changing architecture, or replacing automation with manual workarounds - explains root cause, offers 2-3 options with trade-offs, and requests explicit user choice
---

# Task Direction Approval

## Overview

This skill prevents unauthorized direction changes by forcing explicit user consent before deviating from the original requirements.

## Use when...

- Switching from the original tech/library to alternatives
- Replacing an automated approach with a manual workaround
- Changing architecture or design patterns
- Delivering different results than requested

## Symptoms / keywords

- “can’t use X”, “let’s switch to Y”, “workaround”, “manual”, “different approach”, “alternative library”, “rewrite”, “change architecture”

## Communication protocol (template)

**❌ Wrong Response:**

"GraphQL Codegen failed, so I'll define types manually instead."

**✅ Correct Response:**

"GraphQL Codegen failed due to authentication error. Options available:
1. Add authentication headers
2. Try different endpoint
3. Download schema file directly
Which approach would you prefer?"

## Minimal workflow

1. Explain the failure root cause clearly (what failed, why it failed, evidence).
2. Present 2-3 viable options with trade-offs (speed, risk, maintenance, correctness).
3. Ask for explicit user choice.
4. Only proceed after approval.

## Notes

- Use `investigation-mode` when there are repeated failures or the situation is unclear.
