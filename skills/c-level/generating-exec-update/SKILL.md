---
name: generating-exec-update
description: Use before stakeholder meetings - generates 1-page executive summary from latest PM outputs.
---

# Generating Exec Update

## Overview

Generates a concise 1-page executive update from latest PM outputs (charters, VOC, KTLO, decisions). Perfect for stakeholder meetings and leadership reviews.

## When to Use

- Before leadership meetings
- Weekly exec check-ins
- Monthly updates to stakeholders
- Quick status snapshots

## Core Pattern

**Step 1: Read Latest Outputs**

Read the most recent files from:
- `outputs/roadmap/` (latest charter)
- `outputs/insights/` (latest VOC synthesis)
- `outputs/ktlo/` (latest KTLO triage)
- `outputs/decisions/` (recent decisions)

If files missing, note what's unavailable.

**Step 2: Extract Key Information**

From each source, extract:
- **Problems:** What are we solving? (from charters/VOC)
- **Metrics:** Current vs target KPIs (from charters)
- **Risks:** Top risks and mitigations (from charters/KTLO)
- **Timeline:** Current week + quarter milestones (from charters)

**Step 3: Generate 1-Page Summary**

Write to `outputs/exec_updates/exec-update-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: generating-exec-update
sources:
  - outputs/roadmap/Q1-2026-charters.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-2026-01.md (modified: YYYY-MM-DD)
  - outputs/ktlo/ktlo-triage-2026-01-14.md (modified: YYYY-MM-DD)
downstream:
  - (sent to stakeholders)
---

# Executive Update: [Date]

## Top 3 Problems We're Solving

1. **[Problem 1]** - [Why it matters in 1 sentence]
   - **Evidence:** [Source: file:line]

2. **[Problem 2]** - [Why it matters in 1 sentence]
   - **Evidence:** [Source: file:line]

3. **[Problem 3]** - [Why it matters in 1 sentence]
   - **Evidence:** [Source: file:line]

## Key Metrics

| Metric | Current | Target | Status | Trend |
|--------|---------|--------|--------|-------|
| [KPI 1] | [Value] | [Goal] | 🟢/🟡/🔴 | ↗/→/↘ |
| [KPI 2] | [Value] | [Goal] | 🟢/🟡/🔴 | ↗/→/↘ |
| [KPI 3] | [Value] | [Goal] | 🟢/🟡/🔴 | ↗/→/↘ |

**Status Legend:** 🟢 On track | 🟡 At risk | 🔴 Blocked

## Top 3 Risks

| Risk | Impact | Mitigation | Owner | Status |
|------|--------|------------|-------|--------|
| [Risk 1] | High/Med/Low | [Mitigation plan] | [Name or TBD] | 🟢/🟡/🔴 |
| [Risk 2] | High/Med/Low | [Mitigation plan] | [Name or TBD] | 🟢/🟡/🔴 |
| [Risk 3] | High/Med/Low | [Mitigation plan] | [Name or TBD] | 🟢/🟡/🔴 |

## Timeline

### This Week
- [Key milestone 1]
- [Key milestone 2]
- [Key milestone 3]

### This Quarter
- [Major initiative 1]
- [Major initiative 2]
- [Major initiative 3]

## Recent Decisions
- **[Decision]:** [Outcome] - [Impact]
- **[Decision]:** [Outcome] - [Impact]

## Sources Used
- [file path]
- [file path]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Problem is top priority] | Evidence | [charter:line] |
| [Metric target] | Evidence | [charter:line] |
| [Risk impact] | Evidence/Assumption | [file:line or "Assessed by PM"] |
```

**Step 4: Copy to History**

- Copy to `history/generating-exec-update/exec-update-YYYY-MM-DD.md`

## Quick Reference

**One-page means:**
- 3 problems max
- 3 metrics max
- 3 risks max
- 3 bullets per timeline section
- No paragraphs, only tables and bullets

## Common Mistakes

- **Too detailed:** This isn't the full charter, it's highlights only
- **Missing evidence:** Every claim needs a source
- **Stale sources:** Use most recent outputs, not old versions
- **No unknowns:** If data missing, say "Unknown - need [X]"
- **Vague timeline:** "Soon" → specific week/quarter

## Verification Checklist

- [ ] Read latest charter, VOC, KTLO
- [ ] Extracted top 3 problems
- [ ] Metrics table complete with status
- [ ] Risks table includes mitigation
- [ ] Timeline has current week + quarter
- [ ] All claims have sources
- [ ] Metadata header complete
- [ ] Copied to history

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Top problem] | Evidence | [charter:line or voc:line] |
| [Metric target] | Evidence | [charter:line] |
| [Risk assessment] | Evidence/Assumption | [charter/ktlo:line or "PM judgment"] |
