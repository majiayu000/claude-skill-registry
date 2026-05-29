---
name: triaging-ktlo
description: Use when you have a Jira backlog export and need to turn KTLO tickets into a product-view with prioritized buckets.
---

# Triaging KTLO

## Overview

Transforms a chaotic KTLO (Keep The Lights On) backlog into a structured product view. Categorizes issues into 5 buckets, surfaces the top 20, and recommends stop/fix/defer actions.

## When to Use

- Inherited a messy Jira backlog
- Support team keeps escalating issues
- Need to present KTLO to leadership
- Want to find patterns in operational burden

## Core Pattern

**Step 1: Load Jira Export**

Read files in `inputs/jira/` (CSV preferred, but accept HTML/PDF/MD).

Required columns (or equivalents):
- Issue key, Summary, Status, Priority
- Component/Product area
- Created date, Updated date
- Labels, Customer impact (if present)
- Escalation flag, Linked tickets

If columns are missing, note what's unknown.

**Step 2: Categorize into 5 Buckets**

| Bucket | Definition | Signals |
|--------|------------|---------|
| **1. Revenue/Renewal Risk** | Could cause churn or block deals | "customer threatening to leave", "blocker for renewal", escalation tags |
| **2. Customer Trust & Data Integrity** | Errors, data corruption, incorrect outputs | "data mismatch", "wrong values", "sync failed" |
| **3. Operational Burden** | High support volume, field escalations | Multiple linked tickets, repeat issues, "workaround" in comments |
| **4. Paper Cuts (UX Friction)** | Annoyances that don't break things | "confusing", "should be easier", "unexpected behavior" |
| **5. Tech Debt Blocking Roadmap** | Can't build new things until fixed | Dependencies mentioned, "refactor needed", "legacy" |

**Step 3: Score and Rank**

For each issue, note:
- Which bucket(s) it belongs to
- Severity (Critical/High/Medium/Low)
- Recency (last updated)
- Volume (linked tickets, duplicates)

**Step 4: Generate Output**

Write to `outputs/ktlo/ktlo-triage-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: triaging-ktlo
sources:
  - inputs/jira/export.csv (modified: YYYY-MM-DD)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# KTLO Triage: [Date]

## Executive Summary
[3 sentences: What's the state of KTLO? What's most urgent?]

## Bucket Overview

| Bucket | Count | Critical | High | Med | Low |
|--------|-------|----------|------|-----|-----|
| 1. Revenue Risk | N | N | N | N | N |
| 2. Trust/Data | N | N | N | N | N |
| 3. Ops Burden | N | N | N | N | N |
| 4. Paper Cuts | N | N | N | N | N |
| 5. Tech Debt | N | N | N | N | N |
| **Total** | N | N | N | N | N |

## Top 20 Issues

| Rank | Key | Summary | Bucket | Severity | Why It Matters | Who Feels Pain | Next Step |
|------|-----|---------|--------|----------|----------------|----------------|-----------|
| 1 | ABC-123 | [summary] | 1 | Critical | [reason] | [persona] | [action] |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Patterns Observed
1. **[Pattern]:** [Description] — Affected issues: [list keys]
2. ...

## Recommendations

### STOP (Deprioritize/Close)
| Key | Reason |
|-----|--------|
| ... | [why this can be closed or deprioritized] |

### FIX (Address Soon)
| Key | Reason | Suggested Sprint |
|-----|--------|------------------|
| ... | [why urgent] | [Q1/Q2/etc] |

### DEFER (Later / Needs More Info)
| Key | Reason |
|-----|--------|
| ... | [why this can wait] |

## Unknowns / Missing Data
- [What columns were missing?]
- [What context would help?]

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Issue affects X customers] | Evidence/Unknown | [from ticket or "Not stated"] |
```

**Step 5: Copy to History & Update Tracker**

- Copy to `history/triaging-ktlo/ktlo-triage-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Bucket | Key Signal |
|--------|------------|
| 1. Revenue Risk | "churn", "renewal", escalation |
| 2. Trust/Data | "incorrect", "mismatch", "corruption" |
| 3. Ops Burden | Multiple tickets, workarounds |
| 4. Paper Cuts | "confusing", "annoying" |
| 5. Tech Debt | "refactor", "legacy", "blocker" |

## Common Mistakes

- **Missing buckets:** Only listing revenue risk → Check all 5 buckets
- **No severity:** "These are all important" → Rank by Critical/High/Med/Low
- **Guessing impact:** "This affects many customers" → Only state if in ticket
- **Ignoring patterns:** Treating each ticket independently → Group related issues
- **No next steps:** Just listing issues → Every issue needs suggested action

## Verification Checklist

- [ ] All Jira files read
- [ ] Issues categorized into 5 buckets
- [ ] Counts are accurate
- [ ] Top 20 ranked with reasons
- [ ] Stop/Fix/Defer recommendations provided
- [ ] Patterns identified and documented
- [ ] Unknown/missing data noted
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Issue is Critical] | Evidence | [ticket priority field] |
| [Affects enterprise customers] | Evidence/Unknown | [stated in ticket or "Unknown"] |
| [Pattern affects N tickets] | Evidence | [list of ticket keys] |
