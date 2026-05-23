---
name: work-queue
description: Maintains a queue of work items (features, bugs, tasks) across workspace-hub repositories with two-phase capture and process pipeline
version: 1.1.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - work_item_capture
  - complexity_classification
  - multi_repo_coordination
  - priority_management
  - processing_pipeline
  - queue_state_management
  - archive_audit_trail
  - reflect_integration
tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
related_skills: [claude-reflect, skill-learner, repo-sync]
scripts:
  - next-id.sh
  - queue-status.sh
  - archive-item.sh
  - queue-report.sh
---

# Work Queue Skill

> Two-phase work queue system: **Capture** rapidly logs items, **Process** triages and delegates by complexity. Inspired by bladnman/do-work, adapted for multi-repo orchestration.

## Quick Start

```bash
# Capture a work item
/work add Fix login redirect in aceengineer-website

# Process next item in queue
/work run

# List all pending items
/work list

# Check specific item
/work status WRK-001

# Queue health report
/work report
```

## Command Interface

| Command | Action | Description |
|---------|--------|-------------|
| `/work add <desc>` | Capture | Log one or more work items |
| `/work run` or `/work` | Process | Process next item in queue |
| `/work list` | Status | Show all pending/working/blocked items (regenerates INDEX.md) |
| `/work status WRK-NNN` | Detail | Show specific item details |
| `/work prioritize` | Reorder | Interactive priority adjustment |
| `/work archive WRK-NNN` | Archive | Manually archive an item |
| `/work report` | Report | Queue health summary |

Smart routing: Action verbs (run, go, start) -> Process. Descriptive content -> Capture.

## Two-Phase System

### Phase 1: Capture
- Parse input for single vs multi-request
- Check duplicates against pending/working/blocked
- Classify complexity (simple <50 words; medium 50-200 words; complex >200 words or 3+ features)
- Create file in `pending/` with proper template
- Create context document for large inputs

### Phase 2: Process
- Select next item by priority from `pending/`
- Triage: classify complexity -> Route A/B/C
- Claim: move to `working/`, update frontmatter
- Pre-check: repo-readiness on target repos
- Delegate to subagents per route
- Test, commit, archive pipeline
- Failure handling (3 attempts -> mark failed)

## Complexity Routing

```
Route A (Simple):  Triage -> Implement -> Test -> Archive
Route B (Medium):  Triage -> Explore -> Implement -> Test -> Archive
Route C (Complex): Triage -> Plan (spec) -> Explore -> Implement -> Test -> Review -> Archive
```

| Complexity | Criteria | Route |
|------------|----------|-------|
| Simple | Single config/value change, clear files, <50 words, 1 repo | A |
| Medium | Clear outcome, unknown files, 1-2 repos, 50-200 words | B |
| Complex | Architectural, 3+ repos, ambiguous scope, >200 words | C |

Route C items generate a spec in `specs/modules/` using existing plan templates.

### Compound Integration

Route C items with `compound: true` in frontmatter delegate to the compound engineering loop instead of the standard pipeline:

```
Route C (compound): /compound "<title>" → Plan → Work → Review → Compound → Archive
```

To create a compound work item:
```
/work add --compound "Add OAuth2 authentication to website"
```

This sets `compound: true` in the work item frontmatter, causing the process phase to delegate to `/compound` for the full 4-phase loop.

## Queue Directory Structure

### Master Queue (workspace-hub)
```
workspace-hub/.claude/work-queue/
  pending/          # Items awaiting processing
  working/          # Currently being processed (max 1-2)
  blocked/          # Awaiting dependencies
  archive/YYYY-MM/  # Completed items with audit trail
  assets/           # Screenshots, context files
  state.yaml        # Counters, stats, last processed
```

### Repo-Local Queue (each target repo)
```
<target-repo>/.claude/work-queue/
  pending/          # Items targeting this repo
  working/          # Currently being processed in this repo
  archive/YYYY-MM/  # Completed items
  state.yaml        # Repo-local counters
```

### Repo-Local Specs (Route C only)
```
<target-repo>/specs/modules/<module>/
  plan.md           # Full plan synced from workspace-hub
```

**Source of truth**: workspace-hub is the master. Repo-local copies are synced mirrors for local visibility.

## Work Item Format

```yaml
---
id: WRK-001
title: Brief descriptive title
status: pending
priority: medium  # high | medium | low
complexity: simple  # simple | medium | complex
compound: false     # true = route via /compound instead of standard pipeline
created_at: 2026-01-28T10:00:00Z
target_repos:
  - aceengineer-website
commit:
spec_ref:
related: []
blocked_by: []
synced_to: []  # repos where this item has been mirrored
---

# Title

## What
[1-3 sentence description]

## Why
[Rationale]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

---
*Source: [verbatim original request]*
```

## Multi-Repo Handling

- Each item has `target_repos` field listing affected repositories
- Pre-check via repo-readiness on each target repo before processing
- If repo has dirty state or failing tests -> item moves to `blocked/` with reason
- Route C items get cross-repo implementation sequence from Plan agent
- Commits per-repo with work item ID: `feat(work-queue): WRK-NNN - description`
- Workspace-hub submodule refs updated after all repos committed

## Repo-Local Sync

Work items and specs are **synced to target repos** for local visibility:

### On Capture
- Work item created in workspace-hub `pending/` (master)
- Copy synced to each `<target-repo>/.claude/work-queue/pending/`
- Work item `synced_to` field updated with repo list
- Repo-local `state.yaml` updated

### On Process (Route C — Plan Creation)
- Spec created in workspace-hub `specs/modules/<module>/plan.md`
- Spec also copied to `<target-repo>/specs/modules/<module>/plan.md`
- Both copies have `source_work_item: WRK-NNN` and cross-reference each other

### On Archive
- Workspace-hub master item archived to `archive/YYYY-MM/`
- Repo-local copy also moved to `<target-repo>/.claude/work-queue/archive/YYYY-MM/`

### On Status Change
- Any status change (pending → working → blocked → done) updates both master and repo-local copies

### Sync Direction
```
workspace-hub (master) ──sync──> target-repo (mirror)
       ↑                              │
       └──── status/commits ───────────┘
```

Workspace-hub is always the source of truth. If conflicts arise, master wins.

## Integration Points

| System | Integration |
|--------|-------------|
| claude-reflect | Checklist item: queue counts, stale item alerts (>7 days blocked) |
| skill-learner | Post-archive feedback: triage accuracy tracking |
| repo-readiness | Pre-check before processing each work item |
| specs/modules | Route C items generate plan files with bidirectional linking |

## Scripts

| Script | Purpose |
|--------|---------|
| `next-id.sh` | Scan queue dirs for max WRK-NNN, return next |
| `queue-status.sh` | Report counts per state |
| `archive-item.sh` | Move to `archive/YYYY-MM/` with metadata |
| `queue-report.sh` | Generate summary for reflect integration |
| `generate-index.py` | Generate `INDEX.md` with multi-view lookup tables |

## Error Handling

### Item Processing Failures
- 3 attempts before marking as failed
- Failed items stay in `working/` with `status: failed`
- Failure reason logged in frontmatter `failure_reason` field

### Blocked Items
- Auto-detect: dirty repo, failing tests, pending PR
- Moved to `blocked/` with `blocked_by` field
- Daily reflect checks for stale blocked items (>7 days)

### State Recovery
- `state.yaml` tracks counters and last processed
- Scripts are idempotent - safe to re-run
- Archive includes full audit trail

## Version History

- **1.1.0** (2026-01-29): Repo-local sync
  - Work items synced to target repo `.claude/work-queue/`
  - Route C specs synced to target repo `specs/modules/`
  - Bidirectional status tracking (master → mirror)
  - `synced_to` frontmatter field added
- **1.0.0** (2026-01-28): Initial release
  - Two-phase capture/process system
  - Complexity routing (A/B/C)
  - Multi-repo coordination
  - Queue state management
  - Reflect integration
