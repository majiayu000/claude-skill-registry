---
name: audit-code
description: Run a single-session code review audit on the codebase
supports_parallel: true
fallback_available: true
estimated_time_parallel: 15 min
estimated_time_sequential: 50 min
---

# Single-Session Code Review Audit

## Execution Mode Selection

| Condition                                 | Mode       | Time    |
| ----------------------------------------- | ---------- | ------- |
| Task tool available + no context pressure | Parallel   | ~15 min |
| Task tool unavailable                     | Sequential | ~50 min |
| Context running low (<20% remaining)      | Sequential | ~50 min |
| User requests sequential                  | Sequential | ~50 min |

---

## Section A: Parallel Architecture (3 Agents)

**When to use:** Task tool available, sufficient context budget

### Agent 1: hygiene-and-types

**Focus Areas:**

- Code Hygiene (unused imports, dead code, console.logs)
- Types & Correctness (any types, type safety, null checks)

**Files:**

- `app/**/*.tsx`, `components/**/*.tsx`
- `lib/**/*.ts`, `hooks/**/*.ts`
- `types/**/*.ts`

### Agent 2: framework-and-testing

**Focus Areas:**

- Framework Best Practices (React patterns, Next.js conventions)
- Testing Coverage (untested functions, missing edge cases)

**Files:**

- `app/**/*.tsx` (routing, layouts)
- `components/**/*.tsx` (component patterns)
- `tests/**/*.test.ts`

### Agent 3: security-and-debugging

**Focus Areas:**

- Security Surface (input validation, auth checks)
- AI-Generated Code Failure Modes
- Debugging Ergonomics

**Files:**

- `lib/auth*.ts`, `middleware.ts`
- `functions/src/**/*.ts`
- Error handling code, logging patterns

### Parallel Execution Command

```markdown
Invoke all 3 agents in a SINGLE Task message:

Task 1: hygiene-and-types agent - audit code hygiene and TypeScript patterns
Task 2: framework-and-testing agent - audit React/Next.js patterns and test
coverage Task 3: security-and-debugging agent - audit security, AI patterns,
debugging
```

### Coordination Rules

1. Each agent writes findings to separate JSONL section
2. Hygiene findings have lowest priority in conflicts
3. Security findings have highest priority
4. Framework agent handles boundary issues

---

## Section B: Sequential Fallback (Single Agent)

**When to use:** Task tool unavailable, context limits, or user preference

**Execution Order:**

1. AICode Patterns (catches hallucinations early) - 15 min
2. Types & Correctness - 10 min
3. Testing Coverage - 10 min
4. Remaining categories - 15 min

**Total:** ~50 min (vs ~15 min parallel)

### Checkpoint Format

```json
{
  "started_at": "ISO timestamp",
  "categories_completed": ["Hygiene", "Types"],
  "current_category": "Framework",
  "findings_count": 18,
  "last_file_written": "stage-2-findings.jsonl"
}
```

---

## Pre-Audit Validation

**Step 0: Episodic Memory Search (Session #128)**

Before running code audit, search for context from past code review sessions:

```javascript
// Search for past code audit findings
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["code audit", "patterns", "quality"],
    limit: 5,
  });

// Search for AI-generated code issues addressed before
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["AICode", "hallucinated", "dead code"],
    limit: 5,
  });
```

**Why this matters:**

- Compare against previous code quality findings
- Identify recurring anti-patterns (may indicate architectural debt)
- Track which issues were resolved vs regressed
- Prevent re-flagging known patterns

---

**Step 1: Check Thresholds**

Run `npm run review:check` and report results. If no thresholds are triggered:

- Display: "⚠️ No review thresholds triggered. Proceed anyway? (This is a
  lightweight single-session audit)"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# Test count
npm test 2>&1 | grep -E "Tests:|passing|failed" | head -5

# Lint status
npm run lint 2>&1 | tail -10

# Pattern compliance
npm run patterns:check 2>&1

# Stack versions
grep -E '"(next|react|typescript)"' package.json | head -5
```

**Step 2b: Query SonarCloud (if MCP available)**

If `mcp__sonarcloud__get_issues` is available, fetch current issue counts:

- Query with `types: "CODE_SMELL,BUG"` and `severities: "CRITICAL,MAJOR"`
- Compare against baseline from previous SonarCloud sync (778 issues as of
  2026-01-05)
- Note any significant changes (>10% increase/decrease)

This provides real-time issue data to cross-reference with audit findings.

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `code`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/multi-ai-audit/templates/CODE_REVIEW_PLAN.md` and verify:

- [ ] Stack versions match package.json
- [ ] Test count baseline is accurate
- [ ] File paths in scope still exist
- [ ] Review range in AI_REVIEW_LEARNINGS_LOG.md is current

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (7 Categories):**

1. Code Hygiene (unused imports, dead code, console.logs)
2. Types & Correctness (any types, type safety, null checks)
3. Framework Best Practices (React patterns, Next.js conventions)
4. Testing Coverage (untested functions, missing edge cases)
5. Security Surface (input validation, auth checks)
6. AICode (AI-Generated Code Failure Modes):
   - "Happy-path only" logic, missing edge cases and error handling (S1)
   - Tests that exist but don't assert meaningful behavior (S1)
   - Hallucinated dependencies/APIs that don't exist (S1)
   - Copy/paste anti-patterns (similar code blocks that should be abstracted)
     (S2)
   - Inconsistent architecture patterns across files (S2)
   - Overly complex functions (deep nesting, >50 lines) (S2)
   - Session Boundary Inconsistencies: Conflicting patterns from different AI
     sessions (S2)
   - Dead Code from Iterations: Commented code, unused variables from AI
     iterations (S3)
   - AI TODO Markers: "TODO: AI should fix this", "FIXME: Claude" patterns (S3)
   - Over-Engineering: Unnecessary abstractions, premature optimization (S2)
7. Debugging (Debugging Ergonomics) (NEW - 2026-01-13):
   - Correlation IDs / request tracing (frontend to backend)
   - Structured logging with context (not just console.log)
   - Sentry/error tracking integration completeness
   - Error messages include actionable fix hints
   - Offline/network status captured in error context

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific issues with file:line references
3. Classify severity: S0 (Critical) | S1 (High) | S2 (Medium) | S3 (Low)
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
5. **Assign confidence level** (see Evidence Requirements below)

**Category Token Requirement (MANDATORY):**

- In JSONL output, `category` MUST be one of:
  `Hygiene|Types|Framework|Testing|Security|AICode|Debugging`
- Do NOT include spaces, parentheses, or descriptive suffixes (e.g., output
  `AICode`, not `AICode (AI-Generated Code Failure Modes)`)

**AI-Code Specific Checks:**

- Functions with only happy-path logic (no try/catch, no null checks)
- Test files with `expect(true).toBe(true)` or trivial assertions
- Import statements for packages not in package.json
- Multiple similar code blocks (>10 lines duplicated)
- Functions with >3 levels of nesting

**Scope:**

- Include: `app/`, `components/`, `lib/`, `hooks/`, `types/`
- Exclude: `node_modules/`, `.next/`, `docs/`
- Conditional: `tests/` excluded for code hygiene, but included when analyzing
  Testing Coverage (category 4) and AI-Generated Code (category 6)

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g., `lib/utils.ts:45`)
2. **Code Snippet** - The actual problematic code (3-5 lines of context)
3. **Verification Method** - How you confirmed this is an issue (grep output,
   lint output)
4. **Standard Reference** - ESLint rule, TypeScript error, or React best
   practice citation

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by external tool (ESLint, TypeScript, tests),
  verified file exists, code snippet matches
- **MEDIUM (70-89%)**: Found via pattern search, file verified, but no tool
  confirmation
- **LOW (<70%)**: Pattern match only, needs manual verification

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the code after initial finding)
- Cross-reference with ESLint or TypeScript output

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **ESLint output** - Mark findings as "TOOL_VALIDATED" if ESLint flagged same
   issue
2. **TypeScript errors** - Mark type findings as "TOOL_VALIDATED" if tsc flagged
   same issue
3. **Test failures** - Mark testing findings as "TOOL_VALIDATED" if test suite
   flagged same area
4. **Prior audits** - Check `docs/audits/single-session/code/` for duplicate
   findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (Critical) and S1 (High) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual code in context
   - Verify the issue is real and not a false positive
   - Check for existing handling or intentional patterns
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Code Review Audit - [DATE]

### Baselines

- Tests: X passing, Y failing
- Lint: X errors, Y warnings
- Patterns: X violations

### Findings Summary

| Severity | Count | Top Issues | Confidence  |
| -------- | ----- | ---------- | ----------- |
| S0       | X     | ...        | HIGH/MEDIUM |
| S1       | X     | ...        | HIGH/MEDIUM |
| S2       | X     | ...        | ...         |
| S3       | X     | ...        | ...         |

### Top 5 Issues

1. [file:line] - Description (S1/E1) - DUAL_PASS_CONFIRMED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Quick Wins (E0-E1)

- ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/code/audit-[YYYY-MM-DD].jsonl`

**CRITICAL - Use JSONL_SCHEMA_STANDARD.md format:**

```json
{
  "category": "code-quality",
  "title": "Short specific title",
  "fingerprint": "code-quality::path/to/file.ts::identifier",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": 90,
  "files": ["path/to/file.ts:123"],
  "why_it_matters": "1-3 sentences explaining impact",
  "suggested_fix": "Concrete remediation direction",
  "acceptance_tests": ["Array of verification steps"],
  "evidence": ["code snippet", "grep output", "lint output"]
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
      "tool": "eslint|typescript|sonarcloud|patterns_check|NONE",
      "reference": "Tool output or NONE justification"
    }
  }
}
```

**⚠️ REQUIRED FIELDS (per JSONL_SCHEMA_STANDARD.md):**

- `category` - MUST be `code-quality` (normalized from
  Hygiene/Types/Framework/etc.)
- `fingerprint` - Format: `<category>::<primary_file>::<identifier>`
- `files` - Array with file paths (include line as `file.ts:123`)
- `confidence` - Number 0-100 (not string)
- `acceptance_tests` - Non-empty array of verification steps

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/code/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and recommendations.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/code/audit-[YYYY-MM-DD].jsonl
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
2. Confirm files saved to `docs/audits/single-session/code/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Code Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last code audit
   - Files Covered: Number of files analyzed
   - Findings: Total count (e.g., "3 S1, 5 S2, 2 S3")
   - Reset Threshold: YES (single-session audits reset that category's
     threshold)
   - Run:
     `node scripts/reset-audit-triggers.js --type=single --category=code --apply`
6. **TDMS Integration (MANDATORY)** - Ingest findings to canonical debt store:
   ```bash
   node scripts/debt/intake-audit.js docs/audits/single-session/code/audit-[YYYY-MM-DD].jsonl --source "audit-code-[DATE]"
   ```
   This assigns DEBT-XXXX IDs and adds to
   `docs/technical-debt/MASTER_DEBT.jsonl`. See
   `docs/technical-debt/PROCEDURE.md` for the full TDMS workflow.
7. Ask: "Would you like me to fix any of these issues now?"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the code category threshold** in `docs/AUDIT_TRACKER.md`
(single-session audits reset their own category; multi-AI audits reset all
thresholds). Reset means the commit counter for this category starts counting
from zero after this audit.

**Code audit triggers (check AUDIT_TRACKER.md):**

- 25+ commits since last code audit, OR
- 15+ code files modified since last code audit

### Multi-AI Escalation

Multi-AI audits are triggered by total commits or time elapsed (not single audit
counts). Check `npm run review:check` for current multi-AI trigger status.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "code" \
  --reason "Explanation of why this is not an issue" \
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
  `node scripts/debt/intake-audit.js <output.jsonl> --source "audit-code-<date>"`

### Documentation Standards (Required)

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Output
  format requirements and TDMS field mapping
- [DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md) - 5-tier doc
  hierarchy
- [CODE_PATTERNS.md](docs/agent_docs/CODE_PATTERNS.md) - Anti-patterns to check
