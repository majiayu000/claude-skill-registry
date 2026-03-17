---
name: plans-report-status
description: Report on the status of incomplete plans — how many tasks remain in each. Optionally fact-check plans before reporting.
---

# Plans Report Status

Scan `docs/plans/` for plans that are not yet complete, and report on the status of each: how many tasks are done vs remaining.

## Operating Mode

**READ-ONLY ANALYSIS + REPORT**

**Allowed:**
- Read plan documents in `docs/plans/` (not `docs/plans/archive/`)
- Parse frontmatter Status field and task summary tables
- Count task completion status per plan
- Invoke `/fact-check` on individual plans (only when user opts in)

**Not allowed:**
- Modifying plan documents (unless fact-check mode is enabled)
- Creating new files
- Changing task statuses

## Inputs

**Required:** None (scans all non-archived plans automatically).

**Optional:**
- `filter`: Glob or keyword to narrow which plans to report on (e.g., `brikette`, `email`)

## Step 1: Ask User About Fact-Check

Before scanning, ask the user:

> Would you like to run `/fact-check` on each incomplete plan before reporting status? This updates plans to reflect the actual repo state but takes longer.

Options:
1. **Yes — fact-check first** — Run `/fact-check <plan-path>` on each incomplete plan before collecting status. This ensures task statuses reflect reality.
2. **No — report as-is** — Report based on what the plan documents currently say. Faster, but statuses may be stale.

Wait for the user's answer before proceeding.

## Step 2: Identify Incomplete Plans

Scan `docs/plans/*.md` (exclude `docs/plans/archive/`). For each plan:

1. Parse YAML frontmatter for `Status` and `Type` fields.
2. **Include** plans where:
   - `Type: Plan` (skip fact-finds, references, decision memos, briefings)
   - `Status` is one of: `Active`, `Draft`, `Accepted`, `Proposed` (i.e., not completed/done)
3. **Exclude** plans where:
   - `Status` is `Historical`, `Superseded`, `Reference`, `Complete`, or `Archived`
   - File is in `docs/plans/archive/`

## Step 3: Fact-Check (If Opted In)

If the user chose fact-check mode:

For each incomplete plan identified in Step 2, invoke `/fact-check <plan-path>` with `scope: focused` (task statuses and file references only). This corrects any stale task-completion claims before reporting.

Use parallel subagents (up to 3 concurrent) to speed this up.

## Step 4: Extract Task Status Per Plan

For each incomplete plan, extract the task summary table. Plans use one of these formats:

### Format A: Summary table with Status column
```markdown
| Task ID | Type | Description | Confidence | Effort | Status | Depends on | Blocks |
|---|---|---|---:|---:|---|---|---|
| TASK-01 | IMPLEMENT | Wire voice examples | 87% | S | Complete (2026-02-10) | - | TASK-02 |
| TASK-02 | IMPLEMENT | Upgrade knowledge | 85% | S | Pending | TASK-01 | TASK-07 |
```

### Format B: Per-task sections with inline Status
```markdown
### ADMIN-01: Configure Turbo Remote Cache
- **Status**: COMPLETE
...
### ADMIN-02: Provision Cloudflare Resources
- **Status**: (partially complete)
```

### Format C: Checkbox lists
```markdown
- [x] Task description (done)
- [ ] Task description (pending)
```

Parse whichever format the plan uses. Classify each task as:
- **Complete**: Status contains `Complete`, `COMPLETE`, `Done`, or checkbox `[x]`
- **In Progress**: Status contains `In progress`, `in-progress`, `partially complete`
- **Pending**: Everything else (including `Pending`, unchecked `[ ]`, no explicit status)

## Step 5: Generate Report

Output a summary table sorted by completion percentage (least complete first):

```
Plans Status Report
====================
Date: YYYY-MM-DD
Mode: [fact-checked | as-reported]
Plans scanned: N (M excluded as complete/archived/non-plan)

| Plan | Status | Total | Done | In Progress | Remaining | % Complete |
|------|--------|------:|-----:|------------:|----------:|-----------:|
| administrative-debt-plan | Active | 12 | 8 | 0 | 4 | 67% |
| business-os-phase-2-plan | Draft | 15 | 3 | 1 | 11 | 20% |
| ... | ... | ... | ... | ... | ... | ... |

Overall: X tasks done / Y total across Z active plans (N% complete)
```

After the table, list each plan with its remaining tasks:

```
---
### administrative-debt-plan (4 remaining)
- ADMIN-02: Provision Cloudflare Resources (partially complete)
- ADMIN-07: Deploy Firebase security rules
- ADMIN-08: Rotate secrets
- ADMIN-09: Product-pipeline API key

### business-os-phase-2-plan (11 remaining)
- BOS-P2-03: Mobile responsive layout
- ...
```

## Step 6: Highlight Key Observations

After the detailed breakdown, add a brief observations section:

- **Ready to archive (100% done):** Plans where all tasks are complete — recommend archival (`Status: Archived`, move to `docs/plans/archive/`)
- Plans closest to completion (>80% done)
- Plans with no progress (0% done)
- Plans with tasks in progress (active work)
- Any plans where fact-check revealed stale statuses (if fact-check mode was used)

## Error Handling

- **No task table found:** Report plan as "No structured tasks found — manual review needed"
- **Ambiguous status:** Default to Pending and note the ambiguity
- **Very large plans (>50 tasks):** Still count all tasks, but abbreviate the remaining-tasks list to top 10

## Integration with Other Skills

| After report... | Consider... |
|-----------------|-------------|
| Plan 100% complete | Set `Status: Archived` and move to `docs/plans/archive/` |
| Plan near completion | `/build-feature` to finish remaining tasks |
| Plan stale (0% progress, old dates) | Archive or `/re-plan` |
| Many stale statuses found by fact-check | Review and commit fact-check fixes |
| Plan has no tasks | `/plan-feature` to add structured tasks |
