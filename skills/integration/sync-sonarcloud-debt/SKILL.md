---
name: sync-sonarcloud-debt
description:
  Sync technical debt items from SonarCloud API into MASTER_DEBT.jsonl
---

# SonarCloud Debt Sync

**Purpose:** Synchronize SonarCloud issues with the canonical technical debt
tracker.

**When to Use:** On-demand when you want to import/update issues from
SonarCloud.

---

## Overview

This skill fetches current issues from SonarCloud, normalizes them to the
canonical TDMS schema, diffs against existing items, and reports what's new,
resolved, or unchanged.

**Output Location:** `docs/technical-debt/MASTER_DEBT.jsonl`

---

## Prerequisites

1. **SonarCloud Project Key:** Must be configured in `sonar-project.properties`
2. **API Token (optional):** For private projects, set `SONAR_TOKEN` env var
3. **Existing MASTER_DEBT.jsonl:** Script diffs against existing items

---

## Execution Steps

### Step 1: Verify Configuration

```bash
# Check sonar-project.properties exists
cat sonar-project.properties | grep "sonar.projectKey"
```

If missing, ask user for the SonarCloud project key.

### Step 2: Run Sync Script

```bash
node scripts/debt/sync-sonarcloud.js
```

**Script behavior:**

1. Fetches issues from SonarCloud public API
2. Normalizes each issue to canonical schema:
   - `source_id`: `sonarcloud:{issueKey}`
   - `category`: Mapped from SonarCloud type/rule
   - `severity`: Mapped (BLOCKER→S0, CRITICAL→S1, MAJOR→S2, MINOR/INFO→S3)
3. Diffs against existing items by `source_id`
4. Outputs report to console

### Step 3: Review Sync Report

The script outputs a report like:

```
SonarCloud Sync Report
━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
   Total in SonarCloud: 847
   Already tracked: 812
   NEW items: 23
   Resolved (not in SonarCloud): 12

📋 NEW Items Preview:
   1. DEBT-0868: Cognitive complexity too high (S2) - components/admin/users-tab.tsx:145
   2. DEBT-0869: Duplicate string literal (S3) - lib/utils.ts:23
   ... (showing 5 of 23)

🗑️ Resolved Items:
   1. DEBT-0234: sonarcloud:AZQ123 - no longer in SonarCloud
   ... (showing 5 of 12)

Actions:
   [A] Add all 23 new items
   [R] Mark 12 items as resolved
   [B] Both (add new + resolve old)
   [N] Do nothing (dry run only)
```

### Step 4: Confirm Actions

Ask user which action to take:

- **A** - Add new items to MASTER_DEBT.jsonl
- **R** - Mark resolved items as RESOLVED
- **B** - Both
- **N** - Cancel (no changes)

```bash
# If user chooses A or B:
node scripts/debt/sync-sonarcloud.js --apply-new

# If user chooses R or B:
node scripts/debt/sync-sonarcloud.js --apply-resolved

# Or both:
node scripts/debt/sync-sonarcloud.js --apply-all
```

### Step 5: Regenerate Views

```bash
node scripts/debt/generate-views.js
```

### Step 6: Verify Changes

```bash
# Check new items added
wc -l docs/technical-debt/MASTER_DEBT.jsonl

# Validate schema
node scripts/debt/validate-schema.js
```

---

## Output

After successful sync:

```
✅ SonarCloud Sync Complete

   Added: 23 new items (DEBT-0868 through DEBT-0890)
   Resolved: 12 items marked RESOLVED
   Views regenerated: 5 files updated

📄 Updated files:
   - docs/technical-debt/MASTER_DEBT.jsonl
   - docs/technical-debt/views/by-severity.md
   - docs/technical-debt/views/by-category.md
   - docs/technical-debt/views/by-status.md
   - docs/technical-debt/views/verification-queue.md
```

---

## Error Handling

**API Rate Limit:**

```
⚠️ SonarCloud API rate limit reached
   Try again in: 15 minutes
   Or use SONAR_TOKEN for higher limits
```

**No Project Key:**

```
❌ No SonarCloud project key found
   Add to sonar-project.properties:
   sonar.projectKey=your-project-key
```

**Network Error:**

```
❌ Failed to connect to SonarCloud API
   Check internet connection and try again
```

---

## Related

- `add-manual-debt` - Add items manually
- `add-deferred-debt` - Add items from PR reviews
- `verify-technical-debt` - Verify items in queue
