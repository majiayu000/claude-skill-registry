---
name: verify-technical-debt
description: Verify technical debt items in the verification queue
---

# Verify Technical Debt

**Purpose:** Verify items in the NEW status queue to confirm they are real
issues, false positives, duplicates, or already resolved.

**When to Use:**

- Session-start alert shows >25 NEW items
- More than 3 days since last verification
- After bulk import from SonarCloud or audits
- Manual verification of specific items

---

## Overview

This skill walks through items in the verification queue, checking if each issue
still exists in the codebase and classifying them appropriately.

**Input:** `docs/technical-debt/views/verification-queue.md` **Output:** Updated
`docs/technical-debt/MASTER_DEBT.jsonl`

---

## Verification Triggers

The session-start hook checks for:

```
IF verification-queue.md has >25 NEW items:
  Alert: "Verification backlog at {count} items"

IF >3 days since last verification:
  Alert: "Verification overdue ({days} days)"
```

---

## Execution Steps

### Step 1: Load Verification Queue

```bash
# Check queue size
node scripts/debt/generate-views.js --queue-only
cat docs/technical-debt/views/verification-queue.md | head -50
```

**Output:**

```
Verification Queue: 47 items (NEW status)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Batch by Severity:
  S0 (Critical): 2 items - VERIFY FIRST
  S1 (High): 12 items
  S2 (Medium): 24 items
  S3 (Low): 9 items

Recommended: Start with S0/S1 items (14 total)
```

### Step 2: Select Batch

Ask user which batch to verify:

```
Select verification batch:
   [1] S0 Critical only (2 items) - RECOMMENDED
   [2] S0 + S1 High (14 items)
   [3] All items (47 items)
   [4] Specific IDs (enter DEBT-XXXX,DEBT-YYYY)
```

### Step 3: Verify Each Item

For each item in the batch:

#### 3a. Display Item

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verifying: DEBT-0042 (1/14)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID:       DEBT-0042
Source:   sonarcloud:AZQ123
File:     components/admin/users-tab.tsx:145
Severity: S1 (High)
Category: code-quality
Title:    Cognitive complexity of 42 exceeds threshold of 15

Created:  2026-01-30
Status:   NEW
```

#### 3b. Read Referenced Code

```bash
# Show code context
sed -n '140,150p' components/admin/users-tab.tsx
```

#### 3c. Determine Classification

```
Does this issue exist?

   [V] VERIFIED - Issue exists and should be fixed
   [F] FALSE_POSITIVE - Not actually an issue (explain why)
   [D] DUPLICATE - Same as existing item (enter DEBT-XXXX)
   [R] RESOLVED - Issue was already fixed
   [S] SKIP - Verify later
```

#### 3d. Record Classification

```bash
# For VERIFIED:
node scripts/debt/resolve-item.js DEBT-0042 --status VERIFIED

# For FALSE_POSITIVE:
node scripts/debt/resolve-item.js DEBT-0042 --status FALSE_POSITIVE \
  --reason "Function complexity is acceptable for this orchestration logic"

# For DUPLICATE:
node scripts/debt/resolve-item.js DEBT-0042 --status DUPLICATE \
  --duplicate-of DEBT-0023

# For RESOLVED:
node scripts/debt/resolve-item.js DEBT-0042 --status RESOLVED \
  --resolution "Fixed in commit abc123"
```

### Step 4: Progress Summary

After each item:

```
Progress: 5/14 verified
━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFIED: 3
❌ FALSE_POSITIVE: 1
🔗 DUPLICATE: 0
✓ RESOLVED: 1
⏭️ SKIPPED: 0

Continue? [Y/n]
```

### Step 5: Final Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verification Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Batch: S0 + S1 (14 items)

Results:
   ✅ VERIFIED: 9 items
   ❌ FALSE_POSITIVE: 3 items (moved to FALSE_POSITIVES.jsonl)
   🔗 DUPLICATE: 1 item (merged with DEBT-0023)
   ✓ RESOLVED: 1 item

Remaining in queue: 33 items (was 47)

📄 Updated files:
   - docs/technical-debt/MASTER_DEBT.jsonl
   - docs/technical-debt/FALSE_POSITIVES.jsonl
   - docs/technical-debt/logs/verification-log.jsonl
   - docs/technical-debt/views/*.md (regenerated)
```

### Step 6: Regenerate Views

```bash
node scripts/debt/generate-views.js
```

---

## Verification Guidelines

### VERIFIED

Mark as VERIFIED when:

- The issue clearly exists in the code
- It matches the description
- It's a real problem that should be fixed

### FALSE_POSITIVE

Mark as FALSE_POSITIVE when:

- The code pattern is intentional
- The tool misunderstood the context
- The issue doesn't apply (e.g., test file)

**Always provide a reason!**

### DUPLICATE

Mark as DUPLICATE when:

- Same file:line as existing item
- Same underlying issue, different wording
- Subset of a larger tracked issue

**Merge into the existing item with lower ID.**

### RESOLVED

Mark as RESOLVED when:

- The code was already fixed
- The file no longer exists
- The issue is no longer applicable

**Include resolution details if known.**

---

## Batch Verification Tips

1. **Start with S0/S1** - Highest priority items first
2. **Group by file** - Verify all items in one file together
3. **Use code search** - If unsure, search for similar patterns
4. **Don't over-verify** - If clearly valid, mark VERIFIED quickly
5. **Document false positives** - Future audits may flag the same thing

---

## Related

- `sync-sonarcloud-debt` - Import from SonarCloud
- `add-manual-debt` - Add items manually
- `add-deferred-debt` - Add from PR reviews
