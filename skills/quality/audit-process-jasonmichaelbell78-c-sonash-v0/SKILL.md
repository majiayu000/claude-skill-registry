---
name: audit-process
description: Run a single-session process and automation audit on the codebase
---

# Single-Session Process/Automation Audit

## Pre-Audit Validation

**Step 1: Check Thresholds**

Run `npm run review:check` and report results.

- If no thresholds triggered: "⚠️ No review thresholds triggered. Proceed
  anyway?"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# CI workflow status
ls -la .github/workflows/ 2>/dev/null || echo "No .github/workflows/ directory"

# Hook inventory
ls -la .claude/hooks/ 2>/dev/null || echo "No .claude/hooks/ directory"
ls -la .husky/ 2>/dev/null || echo "No .husky/ directory"

# Script inventory
ls -la scripts/*.js scripts/*.sh 2>/dev/null || echo "No scripts found"

# Slash command inventory
ls -la .claude/commands/ 2>/dev/null || echo "No .claude/commands/ directory"

# npm scripts
grep -A 50 '"scripts"' package.json | head -60
```

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `process`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_PROCESS_AUDIT_TEMPLATE.md` and verify:

- [ ] CI/CD workflow list is current
- [ ] Hook inventory is complete
- [ ] Script coverage is documented

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (8 Categories):**

1. CI/CD Pipeline (workflow coverage, reliability, speed)
2. Git Hooks (pre-commit, pre-push effectiveness)
3. Claude Hooks (session hooks, tool hooks)
4. Script Health (test coverage, error handling, documentation)
5. **Script Trigger Coverage** (automatic triggers, npm commands, orphan
   scripts)
6. Trigger Thresholds (appropriateness, coverage)
7. Process Documentation (accuracy, completeness)
8. Golden Path & Developer Experience (NEW - 2026-01-17):
   - Setup friction (one command to bootstrap environment)
   - Dev workflow (one command to start development)
   - Test workflow (one command to run full test suite)
   - Deploy workflow (one command to deploy)
   - Rollback workflow (one command to rollback)
   - Common task discoverability (npm scripts documented, README actionable)
   - Environment validation (`scripts/doctor.js` or equivalent)

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific issues with file:line references
3. Classify severity: S0 (breaks CI) | S1 (reduces effectiveness) | S2
   (inconvenient) | S3 (polish)
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
5. **Assign confidence level** (see Evidence Requirements below)

**Process Checks:**

- All CI workflows pass on current branch
- Hooks exit with correct codes
- Scripts have error handling
- Triggers are documented in TRIGGERS.md
- Slash commands have descriptions
- npm scripts are documented in DEVELOPMENT.md

**Scope:**

- Include: `.github/`, `.claude/`, `.husky/`, `scripts/`, `package.json`
- Exclude: `node_modules/`

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g.,
   `.github/workflows/ci.yml:45`)
2. **Code/Config Snippet** - The actual problematic configuration (3-5 lines of
   context)
3. **Verification Method** - How you confirmed this is an issue (workflow run,
   script test, grep)
4. **Impact Description** - What breaks or degrades if not fixed

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by CI run, script execution, or hook test; verified
  file exists, issue reproducible
- **MEDIUM (70-89%)**: Found via pattern search, file verified, but no execution
  test
- **LOW (<70%)**: Pattern match only, needs manual testing to confirm

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the config/script after initial finding)
- Cross-reference with CI logs or script output

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **CI workflow logs** - Mark findings as "TOOL_VALIDATED" if CI logs show
   failure
2. **Script execution** - Mark findings as "TOOL_VALIDATED" if script test
   confirms issue
3. **Hook test runs** - Mark findings as "TOOL_VALIDATED" if hook execution
   reveals problem
4. **Prior audits** - Check `docs/audits/single-session/process/` for duplicate
   findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (breaks CI) and S1 (reduces effectiveness) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual config/script in context
   - Verify the process issue is real
   - Check for intentional configurations or workarounds
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Process/Automation Audit - [DATE]

### Baselines

- CI workflows: X files
- Git hooks: X hooks
- Claude hooks: X hooks
- Scripts: X files
- Slash commands: X commands
- npm scripts: X scripts

### Findings Summary

| Severity | Count | Category | Confidence  |
| -------- | ----- | -------- | ----------- |
| S0       | X     | ...      | HIGH/MEDIUM |
| S1       | X     | ...      | HIGH/MEDIUM |
| S2       | X     | ...      | ...         |
| S3       | X     | ...      | ...         |

### CI/CD Issues

1. [workflow.yml:line] - Description - DUAL_PASS_CONFIRMED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Hook Issues

1. [hook.sh:line] - Description
2. ...

### Script Issues

1. [script.js:line] - Description
2. ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/process/audit-[YYYY-MM-DD].jsonl`

Each line (UPDATED SCHEMA with confidence and verification):

```json
{
  "id": "PROC-001",
  "category": "CI|GitHooks|ClaudeHooks|Scripts|Triggers|ProcessDocs|GoldenPath",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": "HIGH|MEDIUM|LOW",
  "verified": "DUAL_PASS_CONFIRMED|TOOL_VALIDATED|MANUAL_ONLY",
  "file": "path/to/file",
  "line": 123,
  "title": "Short description",
  "description": "Detailed issue",
  "recommendation": "How to fix",
  "evidence": ["config snippet", "CI log output", "script output"],
  "cross_ref": "ci_logs|script_test|hook_test|MANUAL_ONLY"
}
```

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/process/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and improvement plan.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/process/audit-[YYYY-MM-DD].jsonl
   ```

2. **Validation Checks:**
   - All findings have required fields
   - No matches in FALSE_POSITIVES.jsonl (or documented override)
   - No duplicate findings
   - All S0/S1 have HIGH or MEDIUM confidence
   - All S0/S1 have DUAL_PASS_CONFIRMED or TOOL_VALIDATED

3. **If validation fails:**
   - Review flagged findings
   - Fix or document exceptions
   - Re-run validation

---

## Post-Audit

1. Display summary to user
2. Confirm files saved to `docs/audits/single-session/process/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Process Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last process audit
   - Files Covered: Number of CI/hook/script files analyzed
   - Findings: Total count (e.g., "1 S1, 2 S2, 4 S3")
   - Confidence: Overall confidence (HIGH if majority HIGH, else MEDIUM)
   - Validation: PASSED or PASSED_WITH_EXCEPTIONS
   - Reset Threshold: YES (single-session audits reset that category's
     threshold)
6. **Update Technical Debt Backlog** - Re-aggregate all findings:
   ```bash
   npm run aggregate:audit-findings
   ```
   This updates `docs/aggregation/MASTER_ISSUE_LIST.md` and the Technical Debt
   Backlog section in `ROADMAP.md`. Review the updated counts and ensure new
   findings are properly categorized.
7. Ask: "Would you like me to fix any of these process issues now?"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the process category threshold** in `docs/AUDIT_TRACKER.md`
(single-session audits reset their own category; multi-AI audits reset all
thresholds). Reset means the commit counter for this category starts counting
from zero after this audit.

**Process audit triggers (check AUDIT_TRACKER.md):**

- ANY CI/hook file changed since last process audit, OR
- 30+ commits since last process audit

### Multi-AI Escalation

After 3 single-session process audits, a full multi-AI Process Audit is
recommended. Track this in AUDIT_TRACKER.md "Single audits completed" counter.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "process" \
  --reason "Explanation of why this is not a process issue" \
  --source "AI_REVIEW_LEARNINGS_LOG.md#review-XXX"
```
