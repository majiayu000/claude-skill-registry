---
name: audit-refactoring
description: Run a single-session refactoring audit on the codebase
---

# Single-Session Refactoring Audit

## Pre-Audit Validation

**Step 0: Episodic Memory Search (Session #128)**

Before running refactoring audit, search for context from past sessions:

```javascript
// Search for past refactoring audit findings
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["refactoring audit", "god object", "complexity"],
    limit: 5,
  });

// Search for specific tech debt discussions
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["cognitive complexity", "duplicate code", "circular"],
    limit: 5,
  });
```

**Why this matters:**

- Compare against previous refactoring targets
- Identify recurring complexity hotspots (may need architectural fix)
- Track which files were flagged before and why
- Prevent re-flagging intentional design decisions

---

**Step 1: Check Thresholds**

Run `npm run review:check` and report results.

- If no thresholds triggered: "⚠️ No review thresholds triggered. Proceed
  anyway?"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# SonarQube issues (if manifest exists)
cat docs/analysis/sonarqube-manifest.md 2>/dev/null | head -30 || echo "No SonarQube manifest"

# Circular dependencies
npm run deps:circular 2>&1

# Unused exports
npm run deps:unused 2>&1 | head -30

# Large files (potential god objects)
find app components lib -name "*.ts" -o -name "*.tsx" 2>/dev/null | xargs wc -l 2>/dev/null | sort -n | tail -20

# Duplicate code patterns
grep -rn "TODO\|FIXME\|HACK" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l
```

**Step 2b: Query SonarCloud for Cognitive Complexity (if MCP available)**

If `mcp__sonarcloud__get_issues` is available:

- Query with `types: "CODE_SMELL"` and `severities: "CRITICAL"` to get cognitive
  complexity violations
- These are the primary refactoring targets (47 CRITICAL as of 2026-01-05
  baseline)
- Compare current count against baseline - significant changes indicate code
  quality trends
- Use issue file paths to prioritize audit focus areas

This provides real-time cognitive complexity data for targeted refactoring.

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `refactoring`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_REFACTORING_PLAN_TEMPLATE.md` and verify:

- [ ] SonarQube baseline is current (778 issues, 47 CRITICAL)
- [ ] Known god objects are listed
- [ ] Batch fix opportunities are documented

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (5 Categories):**

1. God Objects (large files, too many responsibilities)
2. Code Duplication (repeated patterns, copy-paste code)
3. Cognitive Complexity (SonarQube CRITICAL targets)
4. Architecture Violations (layer boundaries, import cycles)
5. Technical Debt Markers (TODOs, FIXMEs, HACKs)

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific issues with file:line references
3. Classify severity: S0 (blocking) | S1 (major friction) | S2 (annoying) | S3
   (nice-to-have)
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
5. **Assign confidence level** (see Evidence Requirements below)

**Refactoring Targets:**

- Files > 300 lines (potential split candidates)
- Functions > 50 lines (complexity risk)
- Components with > 10 props (interface too large)
- Files with > 5 imports from different domains (coupling)
- Circular dependencies (from deps:circular)
- Unused exports (from deps:unused)

**Scope:**

- Include: `app/`, `components/`, `lib/`, `hooks/`, `functions/`
- Exclude: `node_modules/`, `.next/`, `docs/`

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g., `lib/utils.ts:45`)
2. **Code Snippet or Metrics** - The actual problematic code or measured metrics
   (lines, complexity)
3. **Verification Method** - How you confirmed this is an issue (wc -l,
   deps:circular, grep)
4. **Quantified Impact** - Lines of code, number of dependencies, complexity
   score

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by tool (SonarQube, deps:circular, wc -l), verified
  file exists, metrics match
- **MEDIUM (70-89%)**: Found via pattern search, file verified, but metrics
  estimated
- **LOW (<70%)**: Pattern match only, needs manual verification

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the code after initial finding)
- Cross-reference with SonarQube or dependency analysis output

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **SonarQube manifest** - Mark findings as "TOOL_VALIDATED" if SonarQube
   flagged same issue
2. **deps:circular output** - Mark architecture findings as "TOOL_VALIDATED" if
   tool detected cycle
3. **deps:unused output** - Mark dead code findings as "TOOL_VALIDATED" if tool
   detected unused export
4. **Prior audits** - Check `docs/audits/single-session/refactoring/` for
   duplicate findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (blocking) and S1 (major friction) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual code in context
   - Verify the complexity/coupling issue is real
   - Check for intentional design decisions (documented trade-offs)
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Refactoring Audit - [DATE]

### Baselines

- SonarQube CRITICAL: X issues
- Circular dependencies: X
- Unused exports: X
- Files > 300 lines: X
- TODO/FIXME/HACK markers: X

### Findings Summary

| Severity | Count | Category | Confidence  |
| -------- | ----- | -------- | ----------- |
| S0       | X     | ...      | HIGH/MEDIUM |
| S1       | X     | ...      | HIGH/MEDIUM |
| S2       | X     | ...      | ...         |
| S3       | X     | ...      | ...         |

### Top Refactoring Candidates

1. [file] - X lines, Y responsibilities (S1/E2) - DUAL_PASS_CONFIRMED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Quick Wins (E0-E1)

- ...

### Batch Fix Opportunities

- X instances of [pattern] can be auto-fixed
- ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/refactoring/audit-[YYYY-MM-DD].jsonl`

**CRITICAL - Use JSONL_SCHEMA_STANDARD.md format:**

```json
{
  "category": "refactoring",
  "title": "Short specific title",
  "fingerprint": "refactoring::path/to/file.ts::identifier",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": 90,
  "files": ["path/to/file.ts:123"],
  "why_it_matters": "1-3 sentences explaining refactoring need",
  "suggested_fix": "Concrete refactoring direction",
  "acceptance_tests": ["Array of verification steps"],
  "evidence": ["code structure info", "wc -l output", "deps:circular output"],
  "symbols": ["ClassName", "functionName"],
  "duplication_cluster": {
    "is_cluster": true,
    "cluster_summary": "Pattern description",
    "instances": [{ "file": "path1.ts", "symbol": "name" }]
  }
}
```

**For S0/S1 findings, ALSO include verification_steps:**

```json
{
  "verification_steps": {
    "first_pass": {
      "method": "grep|tool_output|file_read|code_search",
      "evidence_collected": ["initial evidence"]
    },
    "second_pass": {
      "method": "contextual_review|exploitation_test|manual_verification",
      "confirmed": true,
      "notes": "Confirmation notes"
    },
    "tool_confirmation": {
      "tool": "sonarcloud|typescript|patterns_check|NONE",
      "reference": "Tool output or NONE justification"
    }
  }
}
```

**⚠️ REQUIRED FIELDS (per JSONL_SCHEMA_STANDARD.md):**

- `category` - MUST be `refactoring` (normalized from
  GodObject/Duplication/etc.)
- `fingerprint` - Format: `<category>::<primary_file>::<identifier>`
- `files` - Array with file paths (include line as `file.ts:123`)
- `confidence` - Number 0-100 (not string)
- `acceptance_tests` - Non-empty array of verification steps

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/refactoring/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and refactoring plan.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/refactoring/audit-[YYYY-MM-DD].jsonl
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
2. Confirm files saved to `docs/audits/single-session/refactoring/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Refactoring Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last refactoring audit
   - Files Covered: Number of files analyzed for refactoring
   - Findings: Total count (e.g., "1 S1, 3 S2, 5 S3")
   - Confidence: Overall confidence (HIGH if majority HIGH, else MEDIUM)
   - Validation: PASSED or PASSED_WITH_EXCEPTIONS
   - Reset Threshold: YES (single-session audits reset that category's
     threshold)
6. **TDMS Integration (MANDATORY)** - Ingest findings to canonical debt store:
   ```bash
   node scripts/debt/intake-audit.js docs/audits/single-session/refactoring/audit-[YYYY-MM-DD].jsonl --source "audit-refactoring-[DATE]"
   ```
   This assigns DEBT-XXXX IDs and adds to
   `docs/technical-debt/MASTER_DEBT.jsonl`. See
   `docs/technical-debt/PROCEDURE.md` for the full TDMS workflow.
7. Ask: "Would you like me to tackle any of these refactoring tasks now?
   (Recommend starting with batch fixes)"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the refactoring category threshold** in
`docs/AUDIT_TRACKER.md` (single-session audits reset their own category;
multi-AI audits reset all thresholds). Reset means the commit counter for this
category starts counting from zero after this audit.

**Refactoring audit triggers (check AUDIT_TRACKER.md):**

- 40+ commits since last refactoring audit, OR
- 3+ new complexity warnings, OR
- Circular dependency detected

### Multi-AI Escalation

After 3 single-session refactoring audits, a full multi-AI Refactoring Audit is
recommended. Track this in AUDIT_TRACKER.md "Single audits completed" counter.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "refactoring" \
  --reason "Explanation of why this is intentional complexity" \
  --source "AI_REVIEW_LEARNINGS_LOG.md#review-XXX"
```

---

## Documentation References

Before running this audit, review:

### TDMS Integration (Required)

- [PROCEDURE.md](docs/technical-debt/PROCEDURE.md) - Full TDMS workflow
- [MASTER_DEBT.jsonl](docs/technical-debt/MASTER_DEBT.jsonl) - Canonical debt
  store
- Intake command:
  `node scripts/debt/intake-audit.js <output.jsonl> --source "audit-refactoring-<date>"`

### Documentation Standards (Required)

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Output
  format requirements and TDMS field mapping
- [DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md) - 5-tier doc
  hierarchy
- [CODE_PATTERNS.md](docs/agent_docs/CODE_PATTERNS.md) - Anti-patterns to check
