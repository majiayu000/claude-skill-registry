---
name: product-planning
description: Use when transforming meeting transcripts into roadmap PRDs - synthesizes signals, clusters themes, validates PRDs, and generates PRD proposals with evidence
---

# Product Planning

## Purpose

Transform meeting signals into actionable PRDs:
- Synthesize product signals from meeting transcripts
- Cluster semantically into PRD themes
- Validate PRD quality (6-point rubric)
- Generate PRD proposals and update roadmap

## When to Use

Activate when:
- User invokes `/project:meetings-to-backlog`
- Automated processing via scheduled runs
- Regular PRD intake cycles

## Workflow Steps

### 1. Determine Time Window

**Invoke:** (internal logic, not separate skill)

**Inputs:**
- `days`: Explicit lookback (e.g., 7, 14, 30)
- `last_run`: From `datasets/product/.meetings-to-backlog-state.json`
- Default: 3 days

**Calculate cutoff_date:**
```
If days provided: cutoff_date = current_date - days
Else if last_run exists: cutoff_date = last_run timestamp
Else: cutoff_date = current_date - 3 days
```

### 2. Synthesize Meeting Signals

**Invoke:** `meeting-synthesis` skill

**Inputs:**
- Time window (cutoff_date)
- include_customers (optional filter)
- include_internal_functions (optional filter)
- min_mentions, min_sources (thresholds)
- exclude_types (default: "bugs,housekeeping")

**Outputs:**
- Clustered signals (themes with evidence)
- Signal metrics (mentions, accounts, recency, diversity)
- Verbatim quotes for PRD proposals

### 3. Filter to PRD-Level Candidates

**Apply PRD scope rubric** (see `prd-validation` skill):

**Keep candidates that:**
- Are outcome-oriented (clear customer problem and desired outcome)
- Are quarterly-scoped (roughly one quarter of work)
- Have clear boundaries (in/out scope)
- Are measurable (success criteria definable)
- Are evidence-backed (customer signals)

**Drop candidates that:**
- Are too small (single ticket level)
- Are too large (initiative spanning multiple quarters)
- Lack evidence (no customer mentions)

### 4. Draft PRD Proposals

**Use template:** `datasets/product/templates/prd-template.md`

**For each qualified cluster:**

Fill in what's known from signals:
- Project name from cluster theme
- Description from signal summary
- Background from meeting context
- Objectives from customer quotes
- Use cases from feature requests
- Initial requirements from signals

**Mark unknown sections as TBD** - don't fabricate information.

**Set initial status:** 🚧 Drafting

### 5. Validate Each PRD

**Invoke:** `prd-validation` skill

**For each PRD proposal:**
- Apply 6-point rubric
- Drafting PRDs may have warnings (missing DACE, timeline, etc.)
- Note required additions for Actionable status
- If fundamentally incomplete: flag for interactive completion

### 6. Deduplicate Against Existing Backlog

**Check datasets/product/backlog.md:**
- Fuzzy match PRD titles
- If similar PRD exists:
  - Option A: Merge (update existing with new evidence)
  - Option B: Supersede (mark old PRD "superseded by" new)

### 7. Output PRD Proposals

**Write to datasets/product/backlog.md (prepend):**
```markdown
# PRD Intake — YYYY-MM-DD

## PRD 1: {Title}
**Status:** 🚧 Drafting
{PRD proposal summary}

---

## PRD 2: {Title}
**Status:** 🚧 Drafting
{PRD proposal summary}

---

{Previous backlog content...}
```

**Write individual PRD files:**
`datasets/product/prds/{YYYY}/PRD_{slug}.md`

Slug generation: lowercase, hyphens, remove special chars

### 8. Update State Tracking

**Write to datasets/product/.meetings-to-backlog-state.json:**
```json
{
  "last_run": "2025-10-21T14:30:00Z",
  "version": "1.0"
}
```

## Success Criteria

Product planning complete when:
- All meetings in time window synthesized
- Signals clustered into PRD themes
- PRD validation applied (flags issues, doesn't fabricate)
- PRD proposals written to backlog.md
- Individual PRD files created in prds/{YYYY}/
- State file updated with current timestamp

## PRD Statuses

| Status | Meaning |
|--------|---------|
| 🚧 Drafting | Initial creation, known to be incomplete |
| 🏃 Actionable | Eng has agreed there's enough to start work |
| 🔒 Closed | Represents what was finally delivered |
| ❗ Abandoned | Project cancelled or superseded |

## No Fabrication Policy

When creating PRDs from meeting signals:
- Only include information that's evidenced in meetings
- Mark unknown sections as TBD
- Don't invent timelines, metrics, or team assignments
- Flag PRDs that need interactive completion

## Related Skills

**Invoked:**
- `meeting-synthesis`: Extract signals from transcripts
- `prd-validation`: Validate PRD quality

**Related:**
- `roadmap-updating`: Uses PRD proposals for roadmap
- `prd-creation`: Standalone PRD creation with interactive session
