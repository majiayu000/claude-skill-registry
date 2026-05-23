---
name: session-log-fixer
description: Fix session protocol validation failures in GitHub Actions. Use when
  a PR fails with "Session protocol validation failed", "MUST requirement(s) not met",
  "NON_COMPLIANT" verdict, or "Aggregate Results" job failure in the Session Protocol
  Validation workflow. With deterministic validation, failures show exact missing
  requirements directly in Job Summary - no artifact downloads needed.
version: 3.0.0
license: MIT
model: claude-sonnet-4-5
metadata:
  domains:
  - ci
  - session-protocol
  - compliance
  - github-actions
  type: diagnostic-fixer
  inputs:
  - run-id
  - pr-number
  outputs:
  - fixed-session-file
  - commit
---
# Session Log Fixer

Fix session protocol validation failures using deterministic validation feedback from Job Summary.

---

## Quick Start

Just tell me what failed:

```text
session-log-fixer: fix run 20548622722
```

or

```text
my PR failed session validation, please fix it
```

The skill will read the Job Summary from the failed run, identify the non-compliant session file, and apply the necessary fixes.

---

## Triggers

- `session-log-fixer: {run-id}` - Fix specific workflow run
- `fix session validation for {PR/run}` - Natural language activation
- `session protocol failed` - When user reports a failure
- `NON_COMPLIANT session` - Direct from CI output
- `MUST requirement not met` - Direct from validation error

| Input | Output | Quality Gate |
|-------|--------|--------------|
| Run ID or PR number | Fixed session file with commit | CI re-run passes |

---

## Process Overview

```text
GitHub Actions Failure
        │
        ▼
┌───────────────────────────────────────────────────┐
│ Phase 1: READ JOB SUMMARY                         │
│ • Extract run ID from URL or PR                   │
│ • Read Job Summary from GitHub Actions            │
│ • Identify NON_COMPLIANT session files            │
│ • Parse specific missing requirements             │
│ • View detailed validation results                │
├───────────────────────────────────────────────────┤
│ Phase 2: ANALYZE                                  │
│ • Read failing session file                       │
│ • Read SESSION-PROTOCOL.md template               │
│ • Diff current vs required structure              │
│ • Identify specific missing elements              │
├───────────────────────────────────────────────────┤
│ Phase 3: FIX                                      │
│ • Apply fixes based on Job Summary details        │
│ • Copy template sections exactly                  │
│ • Add evidence to verification steps              │
│ • Validate fix locally with Validate-SessionJson.ps1 │
├───────────────────────────────────────────────────┤
│ Phase 4: VERIFY                                   │
│ • Commit and push changes                         │
│ • Monitor re-run status                           │
│ • Confirm COMPLIANT verdict in new Job Summary    │
└───────────────────────────────────────────────────┘
        │
        ▼
   Passing CI
```

---

## Workflow

### Step 1: Read Job Summary

#### Option A: Use the script (recommended)

```powershell
# By run ID
$errors = & .claude/skills/session-log-fixer/scripts/Get-ValidationErrors.ps1 -RunId 20548622722

# By PR number
$errors = & .claude/skills/session-log-fixer/scripts/Get-ValidationErrors.ps1 -PullRequest 799

# View errors
$errors | ConvertFrom-Json
```

#### Option B: Manual (web UI)

Navigate to the failed GitHub Actions run and click the **Summary** tab. The Session Protocol Compliance Report shows:

1. **Overall Verdict** - PASS or CRITICAL_FAIL
2. **Compliance Summary** - Table with each session file, verdict, and MUST failure count
3. **Detailed Validation Results** - Expandable sections showing exact failures

Example Job Summary output:

```markdown
## Session Protocol Compliance Report

> [!CAUTION]
> ❌ **Overall Verdict: CRITICAL_FAIL**
>
> 1 MUST requirement(s) not met. These must be addressed before merge.

### Compliance Summary

| Session File | Verdict | MUST Failures |
|:-------------|:--------|:-------------:|
| `2025-12-29-session-11.md` | ❌ NON_COMPLIANT | 1 |

### Detailed Validation Results

Click each session to see the complete validation report with specific requirement failures.

<details>
<summary>📄 2025-12-29-session-11</summary>

| Check | Level | Status | Issues |
|-------|-------|--------|--------|
| SessionLogExists | MUST | PASS | - |
| ProtocolComplianceSection | MUST | FAIL | Missing 'Protocol Compliance' section |
| MustRequirements | MUST | PASS | - |
| HandoffUpdated | MUST | PASS | - |
...
</details>
```

The detailed results tell you **exactly** which MUST requirements failed.

### Step 2: Local Validation (Optional)

Validate locally before pushing:

```powershell
pwsh scripts/Validate-SessionJson.ps1 -SessionPath ".agents/sessions/<session-file>.json" 
```

This uses the **same script** as CI, so results match exactly.

### Step 3: Read Failing Session

Session files are at `.agents/sessions/YYYY-MM-DD-session-NN-*.md`

Identify what's missing by comparing against the Protocol Compliance section structure.

### Step 4: Read Protocol Template

Read `.agents/SESSION-PROTOCOL.md` to get the canonical checklist templates for:

- Session Start (COMPLETE ALL before work)
- Session End (COMPLETE ALL before closing)

**CRITICAL**: Copy the exact table structure. Do not recreate from memory.

### Step 5: Apply Fixes

Common fixes by failure type:

| Failure | Fix |
|---------|-----|
| Missing Session Start table | Copy template from SESSION-PROTOCOL.md |
| Missing Session End table | Copy template from SESSION-PROTOCOL.md |
| "Pending commit" | Replace with actual commit SHA from `gh pr view` |
| Empty evidence column | Add evidence text: "Tool output present", "Content in context", or "Commit SHA: abc1234" |
| Unchecked MUST | Mark `[x]` with evidence, or mark `[N/A]` with justification if truly not applicable |

**For SHOULD requirements**: Use `[N/A]` when not applicable. Use `[x]` with evidence when completed.

**For MUST requirements**: Never leave unchecked without explanation.

### Step 6: Commit

```powershell
git add ".agents/sessions/<session-file>.md"
git commit -m "docs: fix session protocol compliance for <session-name>

Add missing <what was missing> to satisfy session protocol validation."
git push
```

### Step 7: Verify

```powershell
gh run list --branch (git branch --show-current) --limit 3
gh run view <new-run-id> --json conclusion
```

Check the Job Summary tab again. If validation still fails, the detailed results show what's still missing.

---

## Verification Checklist

After applying fixes:

- [ ] Session file has Session Start Protocol table
- [ ] Session file has Session End Protocol table
- [ ] All MUST requirements are marked `[x]` with evidence
- [ ] No "pending" or placeholder text in evidence column
- [ ] Commit SHA is real (not "pending commit")
- [ ] Push succeeded without conflicts
- [ ] New workflow run triggered
- [ ] Job Summary shows COMPLIANT verdict

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Recreating tables from memory | Will miss exact structure | Copy from SESSION-PROTOCOL.md |
| Marking MUST as N/A without justification | Validation will fail | Provide specific justification |
| Using placeholder evidence | Validators detect these | Use real evidence text |
| Fixing without checking Job Summary | May miss actual failure | Always check Job Summary first |
| Ignoring SHOULD requirements | Creates future tech debt | Mark appropriately |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gh run view` fails | Verify run ID is correct, check authentication |
| Can't find Job Summary | Click "Summary" tab at top of workflow run page |
| Job Summary unclear | Expand detailed validation results for specifics |
| Fix didn't work | Check new Job Summary for remaining issues |
| Wrong session file | Verify branch matches PR, check for multiple session files |
| Local validation differs from CI | Ensure you're using latest SESSION-PROTOCOL.md |

---

## Scripts

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| [Get-ValidationErrors.ps1](scripts/Get-ValidationErrors.ps1) | Extract validation errors from GitHub Actions Job Summary | 0=success, 1=run not found, 2=no errors found |

### Example Usage

```powershell
# Get errors by run ID
$result = & .claude/skills/session-log-fixer/scripts/Get-ValidationErrors.ps1 -RunId 20548622722
$errors = $result | ConvertFrom-Json

# View non-compliant sessions
$errors.NonCompliantSessions

# View detailed errors for specific session
$errors.DetailedErrors.'2025-12-29-session-11'

# Get errors by PR number
$result = & .claude/skills/session-log-fixer/scripts/Get-ValidationErrors.ps1 -PullRequest 799
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [session-init](../session-init/) | Prevents need for this skill by correct initialization |
| analyze | Deep investigation when fixes aren't obvious |

---

## References

- [Common Fixes](references/common-fixes.md) - Fix patterns for common failures
- [Template Sections](references/template-sections.md) - Copy-paste ready templates
- [CI Debugging Patterns](references/ci-debugging-patterns.md) - Advanced job-level diagnostics
- [`Validate-SessionJson.ps1`](../../../scripts/Validate-SessionJson.ps1) - Deterministic validation script
