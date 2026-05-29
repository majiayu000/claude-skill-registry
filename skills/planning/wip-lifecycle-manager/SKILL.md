---
name: "wip-lifecycle-manager"
description: "Manage WIP document lifecycle: create, track, review, and archive work-in-progress documentation; use when starting features, reviewing active WIPs, or archiving completed work (project)"
version: "2.0.0"
---

# WIP Lifecycle Manager

Manage work-in-progress documentation for multi-step tasks, features, and investigations.

## Quick Commands

```bash
# List all active WIPs with status
./scripts/wip-list.sh

# Review WIPs and identify completable ones
./scripts/wip-review.sh

# Archive completed WIPs
./scripts/wip-archive.sh "WIP_feature_name_2025_12_24.md"

# Create new WIP from template
./scripts/wip-create.sh "implementing_new_feature"
```

## When to Use WIPs

**DO create a WIP for:**
- Multi-step features (3+ implementation steps)
- Database migrations with service/UI changes
- Bug investigations requiring research
- Architecture decisions
- Mobile + Web parallel implementations

**DON'T create a WIP for:**
- Single-file changes
- Trivial bug fixes
- Quick refactors
- Documentation updates

## Directory Structure

```
docs/wip/
├── active/           # Currently being worked on
├── archive/
│   └── 2025-12/      # Organized by month
└── README.md         # Index of active WIPs
```

## Naming Convention

**Format**: `WIP_{gerund_description}_{YYYY_MM_DD}.md`

**Examples**:
- `WIP_implementing_feedback_system_2025_12_19.md`
- `WIP_fixing_rls_policy_issues_2025_12_18.md`
- `WIP_building_mobile_app_2025_12_21.md`

**Rules**:
- Use gerund form (ending in -ing)
- Underscores between words
- Date is creation date (never changes)
- NEVER use version suffixes (-v2, -new, -improved)

## WIP Template

```markdown
# WIP: {Feature Name in Title Case}

**Created**: {YYYY-MM-DD}
**Last Updated**: {YYYY-MM-DD}
**Status**: In Progress | On Hold | Complete
**Priority**: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
**Target Completion**: {YYYY-MM-DD} (optional)

## Objective

One paragraph describing what we're building and why.

## Progress Tracker

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1: Database | Complete | Migrations and RLS |
| Phase 2: Service | In Progress | Business logic |
| Phase 3: UI | Pending | Components and forms |
| Phase 4: Testing | Pending | E2E tests |

## Implementation Details

### Phase 1: Database (Complete)

- [x] Create migration `20251224_add_feature.sql`
- [x] Add RLS policies
- [x] Regenerate types

### Phase 2: Service (In Progress)

- [x] Create `feature.service.ts`
- [ ] Implement core methods
- [ ] Add error handling

### Phase 3: UI (Pending)

- [ ] Create form component
- [ ] Add to page
- [ ] Wire up actions

## Files Modified

| File | Change |
|------|--------|
| `supabase/migrations/...` | Added feature table |
| `services/feature.service.ts` | New service |

## Decisions & Notes

- Decision 1: Why we chose approach X over Y
- Note: Important gotcha discovered

## Completion Criteria

- [ ] All phases complete
- [ ] Tests passing
- [ ] Types regenerated
- [ ] Verified in staging
```

## Lifecycle Workflow

### 1. Create

```bash
# Option A: Use script
./scripts/wip-create.sh "implementing_user_auth"

# Option B: Manual
touch docs/wip/active/WIP_implementing_user_auth_2025_12_24.md
```

### 2. Track Progress

Update the WIP as you work:
- Mark tasks complete with `[x]`
- Update phase statuses
- Add notes and decisions
- Update "Last Updated" date

### 3. Review

```bash
# Check all WIPs for completeness
./scripts/wip-review.sh
```

Indicators a WIP is complete:
- All `[ ]` boxes checked
- All phases marked "Complete"
- Status says "Complete"
- Target completion date passed

### 4. Archive

```bash
# Archive a single WIP
./scripts/wip-archive.sh "WIP_feature_2025_12_20.md"

# Archive multiple
./scripts/wip-archive.sh "WIP_a.md" "WIP_b.md" "WIP_c.md"
```

This moves files to `docs/wip/archive/YYYY-MM/`.

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **In Progress** | Actively being worked on | Continue work |
| **On Hold** | Paused intentionally | Document why, resume later |
| **Blocked** | Cannot proceed | Document blocker, escalate |
| **Complete** | All work done | Archive within 1 week |

## Best Practices

### DO

- Update WIP before ending work session
- Mark tasks complete immediately (not in batches)
- Document decisions and gotchas
- Link to related issues/PRs
- Archive promptly when complete

### DON'T

- Create WIP for trivial work
- Let completed WIPs sit in active/
- Create multiple WIPs for same feature
- Use version suffixes in names
- Leave WIPs without status updates for weeks

## Monthly Maintenance

Run on the 1st of each month:

```bash
# 1. Review all active WIPs
./scripts/wip-review.sh

# 2. Archive any completed ones
./scripts/wip-archive.sh <files...>

# 3. Update docs/wip/README.md if needed
```

## Integration with Claude

When starting multi-step work, Claude should:

1. Check for existing WIP: `ls docs/wip/active/`
2. Create WIP if none exists for the task
3. Update WIP as phases complete
4. Suggest archiving when all criteria met

## Related Skills

- `database-migration-manager` - For database phases
- `service-patterns` - For service layer phases
- `ui-patterns` - For UI phases
- `test-patterns` - For testing phases
