---
name: sdd-workflow
description: |
  Manage SDD state, handoffs, and versioning for web-playground.
  Use when: tracking progress, handing off between sessions/agents, propagating changes.
  Triggers: "sdd workflow", "sdd status", "propagate changes", "handoff"
---

# Web Playground SDD Workflow

Track state and enable multi-agent/session continuity for SDD work.

## State File

Location: `.sdd/state.yaml`

```yaml
version: 1
updated: 2025-01-15T10:00:00Z
current_phase: requirements  # foundation | requirements | design

documents:
  foundation: { status: verified, version: 1.0.0, owner: human }
  requirements: { status: partial, version: 1.1.0, owner: claude }
  design: { status: draft, version: 0.1.0, owner: unassigned }

packages:
  react-sample: { foundation: verified, requirements: draft }

gaps: []
escalations: []
```

## Status Values

| Status | Meaning |
|--------|---------|
| `draft` | Created, not verified |
| `verified` | Passed verification |
| `blocked` | Waiting on escalation resolution |
| `partial` | Some items verified, some draft |

## Owner Values

| Owner | Meaning |
|-------|---------|
| `claude` | Current Claude session owns this |
| `human` | Human is responsible |
| `unassigned` | Available for next agent |

## Instructions

### 1. Initialize

```bash
mkdir -p .sdd
```

Create `.sdd/state.yaml` with `current_phase: foundation`.

### 2. Claim Ownership

Before modifying a document, update owner:
```yaml
documents:
  requirements: { status: draft, owner: claude }
```

### 3. Track Progress

Update state after completing work:
```yaml
documents:
  foundation: { status: verified, version: 1.0.0, owner: human }
```

### 4. Escalate When Blocked

When needing human decision:
```yaml
escalations:
  - id: ESC-001
    type: scope_decision
    description: "Should QUALITY-MINIMAL allow lodash?"
    items_affected: [REQ-003]
    status: pending  # pending | resolved
```

Set affected items to `blocked` status.

### 5. Propagate Changes

```
Foundation change -> Re-verify Requirements (@aligns-to links)
Requirements change -> Re-verify Design (@derives links)
```

### 6. Session Handoff

At session end, write `.sdd/handoff.md`:

```markdown
# SDD Handoff - 2025-01-15

**From:** claude
**To:** human (or next claude session)

## Ownership Transfer
- requirements: claude -> unassigned

## Completed
- Foundation verified with SCOPE-MONOREPO, QUALITY-TYPESCRIPT anchors

## In Progress
- REQ-002: 50% complete, needs verification criteria

## Blocked
- REQ-003: waiting on ESC-001 (scope decision)

## Next Steps
1. Resolve ESC-001 (human decision needed)
2. Complete REQ-002 verification criteria
3. Run alignment check
```

## Versioning

| Change | Bump |
|--------|------|
| Anchor/REQ deleted or modified meaning | MAJOR |
| New anchor/REQ, clarification | MINOR |
| Typo, formatting | PATCH |

## Multi-Level

Package specs in `packages/{pkg}/spec/`. Reference root with `root::` prefix:
- `root::SCOPE-MONOREPO`
- `root::REQ-001`

## Verification

- [ ] State file reflects actual document status
- [ ] Ownership assigned before modifications
- [ ] Escalations documented when blocked
- [ ] Handoff enables next agent to continue without questions

## Reference

For full details: `.claude/skills/sdd-guidelines/reference/guidelines-v4.4.md` sections 4, 5, 8, 10
