---
name: describe-phase-file
description: Required sections and format for phase.md. Load when defining phase intent, scope, and acceptance criteria.
user-invocable: false
---

## phase.md

Defines what the Phase accomplishes and how success is measured.

Required sections:
- **Intent**: What this Phase accomplishes and why it exists now
- **Scope**: In scope / Out of scope
- **Constraints**: References to relevant laws and style sections
- **Acceptance criteria**: Concrete, verifiable conditions for completion
- **Risks / notes**: Known tradeoffs or intentionally deferred work

Optional metadata:
- **ticket**: Reference to the ticket ID (format: `ticket: TNNNN`) if this phase was derived from a ticket. This field should appear immediately after the phase title and before the Intent section. When Overseer completes the phase, the referenced ticket will be archived.

Acceptance criteria must be verifiable by the Overseer.