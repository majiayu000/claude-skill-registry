---
name: progress
description: Show detailed progress for active increments with task/AC completion, priority, and type
argument-hint: "[incrementId]"
---

# Increment Progress

Shows detailed progress information for active increments including:
- **Task completion** with progress bars
- **Acceptance Criteria (AC)** completion percentages
- **Priority** indicators (P0/P1/P2)
- **Type** badges (feature/bug/hotfix/refactor)
- **Status** grouping (ready for review → active → paused)

## Hook Execution (Default)

This command is intercepted by the **UserPromptSubmit hook** for instant execution (<10ms). The hook reads from `.specweave/state/dashboard.json` cache.

**No action needed** - the hook output appears automatically in `<system-reminder>` tags.

## CLI Fallback

If hook output isn't displayed (rare), execute:

```bash
specweave status --verbose
```

Note: The CLI command is `specweave status` (with `progress` as an alias).

## Arguments

- `/sw:progress` - Show all active increments
- `/sw:progress 0042` - Show specific increment details (partial ID match supported)

## Data Shown

| Field | Description |
|-------|-------------|
| Tasks | `X/Y (Z%)` with progress bar |
| ACs | `A/B (C%)` acceptance criteria completion |
| Priority | P0 (critical), P1 (high), P2 (normal) |
| Type | feature, bug, hotfix, refactor, experiment |
| Status | ready_for_review, active, planning, paused |

## Related Commands

- `/sw:status` - Macro view (all increments grouped by status)
- `/sw:done <id>` - Close increment after review
