---
name: sdd-requirements
description: |
  Create Requirements documents with alignment to Foundation anchors.
  Use when: defining success criteria, writing verifiable requirements.
  Triggers: "create requirements", "write reqs", "sdd requirements"
---

# Web Playground Requirements

Create Requirements documents that define success criteria aligned to Foundation anchors.

## Prerequisites

**Foundation must be verified before writing requirements.**

Check `.sdd/state.yaml`:
```yaml
documents:
  foundation:
    status: verified  # must be verified
```

## REQ ID Formats

| Level | Format | Example |
|-------|--------|---------|
| Root | `REQ-{NNN}` | REQ-001, REQ-002 |
| Package | `REQ-{PKG}-{NNN}` | REQ-REACT-001, REQ-NEST-001 |

## Instructions

### 1. Choose Level

- **Root:** `spec/requirements.md` (cross-cutting requirements)
- **Package:** `packages/{pkg}/spec/requirements.md` (sample-specific)

### 2. Write Frontmatter

```yaml
---
title: "{Package} Requirements"
version: 1.0.0
status: draft
depends_on:
  - foundation.md@1.0.0  # or root::foundation.md@1.0.0 for packages
---
```

### 3. Write Each Requirement

```markdown
## REQ-001: {Title}

{Description of what the system must do}

`@aligns-to:` {ANCHOR-NAME}

**Status:** draft

**Verification:** {How to verify this requirement is met}
```

### 4. Add Alignment Links

Every requirement must have `@aligns-to` linking to Foundation anchors.

**Root requirements:** Link to root anchors
```markdown
`@aligns-to:` SCOPE-MONOREPO, QUALITY-TYPESCRIPT
```

**Package requirements:** Can link to root or package anchors
```markdown
`@aligns-to:` PATTERN-HOOKS, root::QUALITY-TESTED
```

### 5. Build Coverage Matrix

Track which anchors are addressed:

```markdown
## Coverage Matrix

| Anchor | Requirements |
|--------|--------------|
| SCOPE-MONOREPO | REQ-001 |
| QUALITY-TYPESCRIPT | REQ-001, REQ-003 |
| PATTERN-HOOKS | REQ-REACT-001, REQ-REACT-002 |
```

### 6. Update State

Claim ownership and update `.sdd/state.yaml`:

```yaml
documents:
  requirements: { status: draft, version: 1.0.0, owner: claude }
```

## Example: Package Requirements

```markdown
---
title: "React Sample Requirements"
version: 1.0.0
status: draft
depends_on:
  - foundation.md@1.0.0
  - root::foundation.md@1.0.0
---

# React Sample Requirements

## REQ-REACT-001: Todo CRUD Operations

User can create, read, update, and delete todo items.

`@aligns-to:` DEMO-TODO-APP, root::SCOPE-SHOWCASE

**Status:** draft

**Verification:**
- Create: new item appears in list
- Read: items persist across page reload (localStorage)
- Update: can edit item text, toggle completion
- Delete: item removed from list

---

## REQ-REACT-002: Hooks-Only State

All component state uses React hooks (useState, useReducer, useContext).

`@aligns-to:` PATTERN-HOOKS, TECH-REACT-18

**Status:** draft

**Verification:** No class components in codebase; grep for `extends Component` returns empty.

---

## Coverage Matrix

| Anchor | Requirements |
|--------|--------------|
| DEMO-TODO-APP | REQ-REACT-001 |
| PATTERN-HOOKS | REQ-REACT-002 |
| TECH-REACT-18 | REQ-REACT-002 |
| root::SCOPE-SHOWCASE | REQ-REACT-001 |
```

## Verification

After writing requirements:

- [ ] Frontmatter has depends_on pointing to verified foundation
- [ ] Every REQ has unique ID in correct format
- [ ] Every REQ has `@aligns-to` with valid anchor(s)
- [ ] Cross-level refs use `root::` prefix
- [ ] Coverage matrix shows no unaddressed anchors
- [ ] Each REQ has verification criteria

## Alignment Check

| Check | Pass | Fail |
|-------|------|------|
| Coverage | Every anchor has >= 1 REQ | Anchor unaddressed |
| Scope | REQ within Foundation scope | Outside scope |
| Non-contradiction | Consistent with constraints | Violates constraint |

## State Update

After all requirements verified:
```yaml
documents:
  requirements: { status: verified, version: 1.0.0, owner: human }
current_phase: design
```

Transfer ownership when complete. If blocked on scope decision, escalate:
```yaml
escalations:
  - id: ESC-001
    description: "REQ-003 unclear if within scope"
    status: pending
```

## Next Phase

When requirements are verified, proceed to design:
- Create design items with `@derives` links to requirements
- Document significant decisions as DEC-NNN

## Reference

For full details: `.claude/skills/sdd-guidelines/reference/guidelines-v4.4.md` sections 1.2, 2, 3.2
