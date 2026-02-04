---
name: manager
description: manager skill documentation.
---

# Manager Skill

## Purpose
Maintain scope control and documentation discipline for teams-meetinglens.

## Scope and responsibilities
- Manage status transitions across milestones, epics, features, and tasks
- Ensure documentation reflects current decisions and scope

## Inputs
- `README.md`
- `AGENTS.md`
- Risk register updates

## Outputs
- Scope and priority notes in documentation
- Documentation consistency checks

## Constraints
- No production code
- Status taxonomy must remain consistent

## Error-handling expectations
- Flag ambiguous ownership or missing statuses
- Require mitigations for new risks
- Ensure status snapshot stays accurate

## Testing strategy (unit-focused)
- Verify that all modular components have unit-test requirements listed
- Validate that test scope excludes Teams UI end-to-end tests

## Quality bar / validation checklist
- Every Epic, Feature, and Task has a status
- Risk register is current with mitigations

## Related documentation
- `../../README.md`
- `../../AGENTS.md`
