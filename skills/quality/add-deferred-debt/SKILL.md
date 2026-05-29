---
name: add-deferred-debt
description: Add deferred technical debt items identified during PR review
---

# Add Deferred PR Debt

**Purpose:** Track technical debt items identified during PR review that were
deferred (not fixed in the current PR).

**When to Use:** During or after PR review when you identify issues that should
be tracked but won't be fixed immediately.

---

## Overview

This skill creates a tracked debt item from PR review findings. Items are tagged
with the PR number for traceability.

**Output Location:** `docs/technical-debt/MASTER_DEBT.jsonl`

---

## When to Use This Skill

Use during PR review when:

1. You find an issue but fixing it is out of scope for the current PR
2. The fix would significantly increase PR complexity
3. The issue existed before this PR (pre-existing tech debt)
4. The issue is low severity and can wait

**Do NOT defer if:**

- The issue is S0 (Critical) - must be fixed now
- The issue was introduced by this PR - fix it in this PR
- The issue is a security vulnerability - escalate immediately

---

## Execution Steps

### Step 1: Gather PR Context

Collect from the user or current context:

| Field       | Required | Description                       | Example                     |
| ----------- | -------- | --------------------------------- | --------------------------- |
| `pr_number` | Yes      | PR number                         | `325`                       |
| `file`      | Yes      | File path                         | `components/auth/login.tsx` |
| `line`      | Yes      | Line number                       | `145`                       |
| `title`     | Yes      | Short description                 | `Missing input validation`  |
| `severity`  | Yes      | S1, S2, or S3 (NOT S0)            | `S2`                        |
| `category`  | Yes      | security, performance, etc.       | `security`                  |
| `reason`    | Yes      | Why deferred (out of scope, etc.) | `Pre-existing issue`        |

### Step 2: Validate Severity

```
⚠️ S0 items cannot be deferred!

If this is truly critical, it must be fixed before PR merges.
Options:
   [1] Downgrade to S1 and defer
   [2] Block PR until fixed
   [3] Cancel deferral
```

### Step 3: Preview Item

```
📋 Deferred Debt Item Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PR:          #325
ID:          DEBT-XXXX (auto-assigned)
Source:      PR-325-001
File:        components/auth/login.tsx:145
Severity:    S2 (Medium)
Category:    security
Title:       Missing input validation
Reason:      Pre-existing issue, out of scope for this PR

Confirm? [Y/n]
```

### Step 4: Run Intake Script

```bash
node scripts/debt/intake-pr-deferred.js \
  --pr 325 \
  --file "components/auth/login.tsx" \
  --line 145 \
  --title "Missing input validation" \
  --severity S2 \
  --category security \
  --reason "Pre-existing issue, out of scope for this PR"
```

**Script behavior:**

1. Validates all inputs (rejects S0)
2. Generates source_id as `PR-{number}-{sequence}`
3. Assigns next available DEBT-XXXX ID
4. Appends to MASTER_DEBT.jsonl
5. Logs to intake-log.jsonl with PR context

### Step 5: Regenerate Views

```bash
node scripts/debt/generate-views.js
```

### Step 6: Confirm Success

```
✅ Deferred Debt Item Added

   ID:       DEBT-0892
   PR:       #325
   File:     components/auth/login.tsx:145
   Severity: S2
   Status:   NEW (from PR review)

📄 Updated files:
   - docs/technical-debt/MASTER_DEBT.jsonl
   - docs/technical-debt/views/verification-queue.md

💡 Reminder:
   - Add to PR description: "Defers: DEBT-0892"
   - Item will appear in next verification batch
```

---

## Batch Deferral

For multiple items in one PR:

```bash
# Run for each item
node scripts/debt/intake-pr-deferred.js --pr 325 --file "file1.tsx" ...
node scripts/debt/intake-pr-deferred.js --pr 325 --file "file2.tsx" ...

# Or use batch mode (future enhancement)
node scripts/debt/intake-pr-deferred.js --pr 325 --batch items.json
```

---

## PR Description Update

After adding deferred items, update the PR description:

```markdown
## Technical Debt

Defers: DEBT-0892, DEBT-0893

**Reason:** Pre-existing issues identified during review, out of scope for this
PR. Tracked for future cleanup.
```

---

## Integration with pr-review Skill

The `pr-review` skill includes a mandatory section for deferred items:

```markdown
## Deferred Items (Mandatory Section)

If ANY items are deferred during review:

1. List each with: file, line, severity, description
2. Run `add-deferred-debt` skill for each item
3. Verify items appear in MASTER_DEBT.jsonl

**No PR review is complete until deferred items are tracked.**
```

---

## Related

- `sync-sonarcloud-debt` - Import from SonarCloud
- `add-manual-debt` - Add items manually
- `verify-technical-debt` - Verify items in queue
- `pr-review` - Full PR review workflow
