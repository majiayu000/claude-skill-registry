---
name: describe-steps-file
description: Step format and ordering rules for steps.md. Load when defining implementation steps or checking step requirements.
user-invocable: false
---

## steps.md

Lists ordered steps for implementation. Each step must include:
- **Title**: Short description
- **Intent**: Why the step exists
- **Work**: What needs to be done
- **Done when**: Observable condition that proves completion

Rules:
- Prefer 5-15 steps
- Steps must be ordered (dependencies reflected in ordering)
- Tests are first-class steps, not implied