---
name: audit-documentation
description: Run a single-session documentation audit on the codebase
---

# Single-Session Documentation Audit

## Pre-Audit Validation

**Step 1: Check Thresholds**

Run `npm run review:check` and report results.

- If no thresholds triggered: "⚠️ No review thresholds triggered. Proceed
  anyway?"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# Documentation lint
npm run docs:check 2>&1 | tail -30

# Document sync check
npm run docs:sync-check 2>&1 | head -30

# Count documentation files
find docs -name "*.md" 2>/dev/null | wc -l

# Check for broken links
grep -rn "\[.*\](.*\.md)" docs/ --include="*.md" 2>/dev/null | head -20

# Recent doc changes
git log --oneline --since="7 days ago" -- "*.md" | head -10
```

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `documentation`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_DOCUMENTATION_AUDIT_TEMPLATE.md` and verify:

- [ ] Document inventory is current
- [ ] Template-instance relationships are tracked
- [ ] Tier structure is accurate

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (7 Categories):**

1. Broken Links (internal cross-references that 404)
2. Stale Content (outdated versions, deprecated info)
3. Coverage Gaps (undocumented features, missing guides)
4. Tier Compliance (docs in correct folders per tier)
5. Frontmatter Consistency (required fields present)
6. Template-Instance Sync (templates match instances)
7. Content Quality (coherence, bloat, contradictions, flow)

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific issues with file:line references
3. Classify severity: S0 (Critical - blocks work) | S1 (Major - causes
   confusion) | S2 (Minor) | S3 (Trivial)
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
5. **Assign confidence level** (see Evidence Requirements below)

**Documentation Checks:**

- All `[text](path.md)` links resolve
- Version numbers in docs match package.json
- Dates in "Last Updated" are reasonable
- Required sections present (Purpose, Usage, etc.)
- No placeholder content ([TODO], [PLACEHOLDER], [X])
- Archive docs properly excluded from lint

**Content Quality Checks (Category 7):**

- No circular documentation (A→B→C→A reference loops that confuse readers)
- No redundant/duplicate content across documents
- No contradictory information (conflicting guidance for same task)
- Documentation narrative is cohesive and flows logically
- Document relationships are navigable (clear paths to related content)
- No bloated content (overly verbose, could be condensed)
- Consistent terminology across documents
- No orphaned docs (no incoming links, unclear purpose)

**Scope:**

- Include: `docs/`, `README.md`, `ROADMAP.md`, `ARCHITECTURE.md`,
  `DEVELOPMENT.md`
- Exclude: `node_modules/`, `.next/`

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g., `docs/guides/auth.md:45`)
2. **Content Snippet** - The actual problematic content (broken link, stale
   text)
3. **Verification Method** - How you confirmed this is an issue (link check,
   grep, file stat)
4. **Impact Description** - Who is affected and how (users, developers,
   onboarding)

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by tool (docs:check, link checker), verified file
  exists, issue reproducible
- **MEDIUM (70-89%)**: Found via pattern search, file verified, but no tool
  confirmation
- **LOW (<70%)**: Pattern match only, needs manual verification

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the content after initial finding)
- Cross-reference with docs:check or docs:sync-check output

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **docs:check output** - Mark findings as "TOOL_VALIDATED" if linter flagged
   same issue
2. **docs:sync-check output** - Mark sync findings as "TOOL_VALIDATED" if sync
   checker flagged
3. **git log** - Mark stale findings as "TOOL_VALIDATED" if last modified date
   confirms staleness
4. **Prior audits** - Check `docs/audits/single-session/documentation/` for
   duplicate findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (blocks work) and S1 (causes confusion) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual content in context
   - Verify the documentation issue is real
   - Check if content was recently updated
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Documentation Audit - [DATE]

### Baselines

- Total docs: X files
- docs:check errors: X
- docs:sync-check issues: X
- Docs changed (7 days): X

### Findings Summary

| Severity | Count | Category | Confidence  |
| -------- | ----- | -------- | ----------- |
| S0       | X     | ...      | HIGH/MEDIUM |
| S1       | X     | ...      | HIGH/MEDIUM |
| S2       | X     | ...      | ...         |
| S3       | X     | ...      | ...         |

### Broken Links

1. [source.md:line] -> [target.md] (missing) - TOOL_VALIDATED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Stale Documents

1. [file.md] - Last updated X days ago, references deprecated feature
2. ...

### Coverage Gaps

- Feature X has no documentation
- ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/documentation/audit-[YYYY-MM-DD].jsonl`

Each line (UPDATED SCHEMA with confidence and verification):

```json
{
  "id": "DOC-001",
  "category": "Links|Stale|Coverage|Tier|Frontmatter|Sync|Quality",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": "HIGH|MEDIUM|LOW",
  "verified": "DUAL_PASS_CONFIRMED|TOOL_VALIDATED|MANUAL_ONLY",
  "file": "docs/path/to/file.md",
  "line": 123,
  "title": "Short description",
  "description": "Detailed issue",
  "recommendation": "How to fix",
  "evidence": ["broken link text", "grep output", "git log output"],
  "cross_ref": "docs_check|docs_sync|git_log|MANUAL_ONLY"
}
```

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/documentation/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and fix plan.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/documentation/audit-[YYYY-MM-DD].jsonl
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
2. Confirm files saved to `docs/audits/single-session/documentation/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Documentation Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last documentation audit
   - Files Covered: Number of documentation files analyzed
   - Findings: Total count (e.g., "2 S1, 4 S2, 3 S3")
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
7. Ask: "Would you like me to fix any of these documentation issues now?"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the documentation category threshold** in
`docs/AUDIT_TRACKER.md` (single-session audits reset their own category;
multi-AI audits reset all thresholds). Reset means the commit counter for this
category starts counting from zero after this audit.

**Documentation audit triggers (check AUDIT_TRACKER.md):**

- 20+ doc files changed since last documentation audit, OR
- 30+ commits since last documentation audit

### Multi-AI Escalation

After 3 single-session documentation audits, a full multi-AI Documentation Audit
is recommended. Track this in AUDIT_TRACKER.md "Single audits completed"
counter.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "documentation" \
  --reason "Explanation of why this is not a documentation issue" \
  --source "AI_REVIEW_LEARNINGS_LOG.md#review-XXX"
```

---

## ⚠️ Update Dependencies

When updating this command (categories, checklist items), also update:

| Document                                                  | What to Update                     | Why                            |
| --------------------------------------------------------- | ---------------------------------- | ------------------------------ |
| `docs/templates/MULTI_AI_DOCUMENTATION_AUDIT_TEMPLATE.md` | Category list, checklist structure | Multi-AI version of this audit |
| `docs/SLASH_COMMANDS_REFERENCE.md`                        | `/audit-documentation` section     | Documentation of this command  |

**Why this matters:** This is the single-session version of the documentation
audit. Category changes should stay synchronized with the multi-AI template.
