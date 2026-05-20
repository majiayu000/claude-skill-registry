---
name: superspec:archive
description: |
  Use after verification passes to archive completed changes.
  Applies delta specs to main specs and moves change to archive.
---

# Archive Changes

## Overview

Archive a completed change by applying delta specs to main specs and moving documents to archive.

**Core principle:** Specs are truth. Archive preserves complete history.

**Announce at start:** "I'm using the archive skill to complete this change."

## When to Use

- After `/superspec:finish-branch` completes
- Branch is merged or PR created
- Ready to finalize the change documentation

## Prerequisites

- [ ] Verification passed: `superspec verify [id]` ✅
- [ ] All tests pass
- [ ] Code review approved
- [ ] Branch completed: `/superspec:finish-branch` ✅ (merged or PR created)

## The Archive Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Archive Flow                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   1. Verify Ready                                                 │
│      └─→ Check verification passed                               │
│      └─→ Check tests pass                                        │
│                                                                   │
│   2. Apply Deltas to Main Specs                                  │
│      └─→ ADDED → append to spec                                  │
│      └─→ MODIFIED → replace in spec                              │
│      └─→ REMOVED → delete from spec                              │
│      └─→ RENAMED → rename in spec                                │
│                                                                   │
│   3. Move to Archive                                              │
│      └─→ superspec/changes/[id]/                                 │
│      └─→ superspec/changes/archive/YYYY-MM-DD-[id]/              │
│                                                                   │
│   4. Validate Final State                                         │
│      └─→ superspec validate --strict                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Verify Ready

```bash
# Check verification status
superspec verify [change-id]

# Check tests
npm test / cargo test / pytest

# Confirm all pass
```

**If not ready:** Stop. Fix issues first.

## Step 2: Apply Deltas

### Delta Operations

**ADDED Requirements:**
```markdown
## ADDED Requirements

### Requirement: New Feature
The system SHALL [behavior]
```
→ Appends to `superspec/specs/[capability]/spec.md`

**MODIFIED Requirements:**
```markdown
## MODIFIED Requirements

### Requirement: Existing Feature
The system SHALL [updated behavior]
```
→ Replaces matching requirement in main spec (exact name match required)

**REMOVED Requirements:**
```markdown
## REMOVED Requirements

### Requirement: Deprecated Feature
**Reason**: [why removing]
**Migration**: [how to handle]
```
→ Removes from main spec, keeps reason in archive

**RENAMED Requirements:**
```markdown
## RENAMED Requirements
- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```
→ Renames in main spec

### Apply Order

1. Process RENAMED first (avoid conflicts)
2. Process REMOVED second
3. Process MODIFIED third
4. Process ADDED last

## Step 3: Move to Archive

```bash
# Create archive directory
mkdir -p superspec/changes/archive/$(date +%Y-%m-%d)-[change-id]

# Move all change documents
mv superspec/changes/[change-id]/* \
   superspec/changes/archive/$(date +%Y-%m-%d)-[change-id]/

# Remove empty directory
rmdir superspec/changes/[change-id]
```

**Archive contains:**
```
superspec/changes/archive/2024-01-15-add-2fa/
├── proposal.md       # Original proposal
├── design.md         # Technical design
├── specs/            # Delta specs (before application)
│   └── two-factor-auth/
│       └── spec.md
├── plan.md           # Implementation plan
└── tasks.md          # Task checklist (all complete)
```

## Step 4: Validate Final State

```bash
# Validate all specs
superspec validate --strict

# List specs to confirm update
superspec list --specs
```

**If validation fails:**
- Delta application had errors
- Fix and re-run

## CLI Command

```bash
# Interactive mode
superspec archive [change-id]

# Non-interactive mode
superspec archive [change-id] --yes

# Skip spec updates (tooling-only changes)
superspec archive [change-id] --skip-specs
```

## Archive Document Structure

After archiving:

```
superspec/
├── specs/                           # Updated main specs
│   ├── user-auth/
│   │   └── spec.md                  # Now includes 2FA requirements
│   └── two-factor-auth/
│       └── spec.md                  # New capability spec
│
└── changes/
    └── archive/
        └── 2024-01-15-add-2fa/      # Complete history
            ├── proposal.md
            ├── design.md
            ├── specs/
            ├── plan.md
            └── tasks.md
```

## Handling Edge Cases

### Conflict in MODIFIED

If requirement name doesn't match exactly:

```
Error: Cannot find requirement to modify
Expected: ### Requirement: User Login
Found: ### Requirement: User Authentication
```

**Action:** Fix delta spec to use exact name, or update main spec first.

### New Capability (No Existing Spec)

If delta adds a new capability:

```bash
# Create new spec file
mkdir -p superspec/specs/[new-capability]
cp superspec/changes/[id]/specs/[new-capability]/spec.md \
   superspec/specs/[new-capability]/spec.md
```

### Partial Archive

Don't partially archive. Either:
- Archive complete change
- Keep change active

## Red Flags

**Never:**
- Archive without passing verification
- Archive with failing tests
- Manually edit main specs (use delta process)
- Delete archive history

**Always:**
- Run `superspec verify` before archive
- Use `superspec archive` command (not manual)
- Keep complete archive history
- Validate after archive

## Integration

**Called by:**
- `/superspec:archive` command
- After `finish-branch` completes

**Pairs with:**
- `verify` - Must pass before finish-branch
- `finish-branch` - Must complete before archiving (handles merge/PR)
- `verification-before-completion` - Evidence before claims
