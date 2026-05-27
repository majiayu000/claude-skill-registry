---
name: describe-required-inputs
description: Mandatory files agents must read before acting. Load when starting agent work to ensure prerequisites are met.
user-invocable: false
---

## Required Inputs

Before any agent acts, it must read:
- `.ushabti/laws.md` (if it exists)
- `.ushabti/style.md` (if it exists)

If laws or style don't exist when needed, stop and instruct the user to run the appropriate agent first.