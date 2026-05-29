---
name: add-manual-debt
description: Manually add a technical debt item to MASTER_DEBT.jsonl
---

# Add Manual Technical Debt

**Purpose:** Add ad-hoc technical debt items discovered outside formal audits.

**When to Use:** When you discover tech debt during development that should be
tracked but wasn't found by automated tools.

---

## Overview

This skill guides you through adding a single technical debt item to the
canonical tracker with proper validation and ID assignment.

**Output Location:** `docs/technical-debt/MASTER_DEBT.jsonl`

---

## Execution Steps

### Step 1: Gather Required Information

Collect the following from the user (or context):

| Field         | Required | Description                                     | Example                     |
| ------------- | -------- | ----------------------------------------------- | --------------------------- |
| `file`        | Yes      | File path (relative to repo root)               | `components/auth/login.tsx` |
| `line`        | Yes      | Line number                                     | `145`                       |
| `title`       | Yes      | Short description (< 80 chars)                  | `Missing error boundary`    |
| `severity`    | Yes      | S0 (Critical), S1 (High), S2 (Medium), S3 (Low) | `S2`                        |
| `category`    | Yes      | security, performance, code-quality, docs, etc. | `code-quality`              |
| `effort`      | No       | E0 (<30m), E1 (<2h), E2 (<8h), E3 (>8h)         | `E1`                        |
| `description` | No       | Detailed description                            | `Component lacks error...`  |

### Step 2: Validate File Exists

```bash
# Verify the file exists
ls -la {file}
```

If file doesn't exist, ask user to correct the path.

### Step 3: Validate Line Number

```bash
# Check if line number is valid
wc -l {file}
```

If line exceeds file length, warn user.

### Step 4: Preview Item

Show user what will be added:

```
📋 Technical Debt Item Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID:          DEBT-XXXX (auto-assigned)
Source:      manual
File:        components/auth/login.tsx:145
Severity:    S2 (Medium)
Category:    code-quality
Effort:      E1 (<2h)
Title:       Missing error boundary
Description: Component lacks error boundary, crashes propagate to parent

Confirm? [Y/n]
```

### Step 5: Run Intake Script

```bash
node scripts/debt/intake-manual.js \
  --file "components/auth/login.tsx" \
  --line 145 \
  --title "Missing error boundary" \
  --severity S2 \
  --category code-quality \
  --effort E1 \
  --description "Component lacks error boundary, crashes propagate to parent"
```

**Script behavior:**

1. Validates all inputs
2. Checks for duplicates (same file:line)
3. Assigns next available DEBT-XXXX ID
4. Appends to MASTER_DEBT.jsonl
5. Logs to intake-log.jsonl

### Step 6: Regenerate Views

```bash
node scripts/debt/generate-views.js
```

### Step 7: Confirm Success

```
✅ Technical Debt Item Added

   ID:       DEBT-0891
   File:     components/auth/login.tsx:145
   Severity: S2
   Status:   NEW (pending verification)

📄 Updated files:
   - docs/technical-debt/MASTER_DEBT.jsonl
   - docs/technical-debt/views/verification-queue.md

💡 Next steps:
   - Item is in verification queue (status: NEW)
   - Run 'verify-technical-debt' to verify this item
   - Or manually update status to VERIFIED after confirming issue exists
```

---

## Duplicate Detection

If a similar item already exists:

```
⚠️ Potential Duplicate Detected

Existing item:
   ID:    DEBT-0234
   File:  components/auth/login.tsx:142
   Title: Missing error handling in login

Your item:
   File:  components/auth/login.tsx:145
   Title: Missing error boundary

Options:
   [A] Add anyway (different issue)
   [M] Merge with existing (update DEBT-0234)
   [C] Cancel
```

---

## Severity Guidelines

| Severity | Criteria                                         |
| -------- | ------------------------------------------------ |
| **S0**   | Security vulnerability, data loss risk, crash    |
| **S1**   | Major functionality broken, significant perf hit |
| **S2**   | Code smell, minor bug, moderate tech debt        |
| **S3**   | Style issue, documentation, nice-to-have cleanup |

---

## Category Options

- `security` - Auth, input validation, OWASP
- `performance` - Load times, queries, caching
- `code-quality` - Types, patterns, hygiene
- `documentation` - README, API docs, comments
- `refactoring` - Tech debt, complexity, DRY
- `process` - CI/CD, testing, workflows

---

## Related

- `sync-sonarcloud-debt` - Import from SonarCloud
- `add-deferred-debt` - Add from PR reviews
- `verify-technical-debt` - Verify items in queue
