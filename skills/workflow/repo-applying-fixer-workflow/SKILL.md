---
description: Complete fixer agent workflow including report discovery, validation strategy (HIGH/MEDIUM/FALSE_POSITIVE confidence), fix application, and fix report generation. Use when implementing or updating fixer agents.
---

# Applying Fixer Workflow

Common workflow pattern for all fixer agents in the maker-checker-fixer three-stage quality pipeline.

## When This Skill Loads

This Skill auto-loads for fixer agents that need standardized workflow for applying validated fixes from checker audit reports.

## Core Fixer Workflow

### 1. Report Discovery

**Auto-detect with manual override (default pattern)**:

```bash
# Auto-detect latest audit report for agent family
ls -t generated-reports/{agent-family}-*-audit.md | head -1
```

**Implementation Steps**:

1. **Auto-detect latest**: Find most recent audit report in `generated-reports/`
2. **Allow manual override**: Accept explicit report path from user
3. **Verify report exists**: Check file exists before proceeding
4. **Parse report format**: Extract UUID chain and timestamp for fix report

**Report Naming**: Uses 4-part format per Temporary Files Convention:

- Pattern: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Example: `docs__a1b2c3__2025-12-14--20-45__audit.md`

### 2. Validation Strategy

**CRITICAL PRINCIPLE**: NEVER trust checker findings blindly. ALWAYS re-validate before applying fixes.

**For EACH finding in audit report**:

```
Read finding → Re-execute validation check → Assess confidence level

HIGH_CONFIDENCE:
  - Re-validation confirms issue exists
  - Issue is objective and verifiable
  - Apply fix automatically

MEDIUM_CONFIDENCE:
  - Re-validation unclear or ambiguous
  - Issue is subjective or context-dependent
  - Skip fix, flag as "needs manual review"

FALSE_POSITIVE:
  - Re-validation disproves issue
  - Skip fix, report to user
  - Suggest checker improvement
```

**Confidence Assessment Criteria**:

**HIGH Confidence** (Apply automatically):

- Objective, verifiable errors
- Clear violation of documented standards
- Pattern-based errors with known fixes
- File-based errors (paths, syntax, format)

**MEDIUM Confidence** (Manual review):

- Subjective quality judgments
- Context-dependent issues
- Ambiguous requirements
- Risky refactoring changes

**FALSE_POSITIVE** (Skip and report):

- Re-validation disproves the issue
- Checker misunderstood context
- Checker used wrong verification source
- Finding no longer applicable

### 3. Mode Parameter Handling

Support `mode` parameter for quality-gate workflows:

**Mode Levels**:

- **lax**: Process CRITICAL findings only (skip HIGH/MEDIUM/LOW)
- **normal**: Process CRITICAL + HIGH findings only (skip MEDIUM/LOW)
- **strict**: Process CRITICAL + HIGH + MEDIUM findings (skip LOW)
- **ocd**: Process all findings (CRITICAL + HIGH + MEDIUM + LOW)

**Implementation**:

```markdown
1. Parse audit report and categorize findings by criticality
2. Apply mode filter before re-validation:
   - lax: Only process CRITICAL findings
   - normal: Process CRITICAL + HIGH findings
   - strict: Process CRITICAL + HIGH + MEDIUM findings
   - ocd: Process all findings
3. Track skipped findings for reporting
4. Document skipped findings in fix report
```

**Reporting Skipped Findings**:

```markdown
## Skipped Findings (Below Mode Threshold)

**Mode Level**: normal (fixing CRITICAL/HIGH only)

**MEDIUM findings** (X skipped - reported but not fixed):

1. [File path] - [Issue description]

**LOW findings** (X skipped - reported but not fixed):

1. [File path] - [Issue description]

**Note**: Run with `mode=strict` or `mode=ocd` to fix these findings.
```

### 4. Fix Application

**Automatic Application** (HIGH confidence only):

- Apply ALL HIGH_CONFIDENCE fixes automatically
- NO confirmation prompts (user already reviewed checker report)
- Skip MEDIUM_CONFIDENCE findings (flag for manual review)
- Skip FALSE_POSITIVE findings (report to improve checker)
- Use appropriate tools based on file location:
  - `.opencode/` folders: Use Bash tools (sed, awk, heredoc)
  - `docs/` folders: Use Edit tool
  - Other locations: Use appropriate tools per file type

**Fix Execution Pattern**:

```markdown
For each HIGH_CONFIDENCE finding:

1. Read current file state
2. Apply fix using appropriate tool
3. Verify fix applied correctly
4. Log fix in fix report (progressive writing)
5. Continue to next finding
```

### 5. Fix Report Generation

Generate fix report in `generated-reports/` using same UUID chain as audit:

**File Naming Pattern**:

- Input audit: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Output fix: `{agent-family}__{uuid-chain}__{timestamp}__fix.md`
- Preserve UUID chain and timestamp from source audit

**Report Structure**:

```markdown
# Fix Report: {Agent Name}

**Status**: In Progress / Complete
**Source Audit**: {path to audit report}
**Timestamp**: {YYYY-MM-DD--HH-MM UTC+7}
**UUID Chain**: {uuid-chain}
**Mode**: {lax/normal/strict/ocd}

---

## Fixes Applied

### Fix 1: {Title}

**Status**: ✅ APPLIED / ⏭️ SKIPPED
**Criticality**: {CRITICAL/HIGH/MEDIUM/LOW}
**Confidence**: {HIGH/MEDIUM/FALSE_POSITIVE}
**File**: {path}

**Issue**: {description}

**Changes Applied**: {before → after}

**Tool Used**: {Edit/Bash sed/etc}

---

## Skipped Findings

### {Reason for skipping}

**Count**: X findings

1. {File} - {Issue} - {Reason}

---

## Summary

**Fixes Applied**: X
**Fixes Skipped**: Y (Z MEDIUM_CONFIDENCE, W FALSE_POSITIVE)
**Skipped by Mode**: M (below mode threshold)

**Status**: Complete
**Completed**: {timestamp}
```

**Progressive Writing**: Write findings as they're processed, not buffered to end.

### 6. Trust Model: Checker Verifies, Fixer Applies

**Key Principle**: Fixer trusts checker's verification work (separation of concerns).

**Why Fixers Don't Have Web Tools**:

1. **Separation of Concerns**: Checker does expensive web verification once
2. **Performance**: Avoid duplicate web requests
3. **Clear Responsibility**: Checker = research/verification, Fixer = application
4. **Audit Trail**: Checker documents all sources in audit report
5. **Trust Model**: Fixer trusts checker's documented verification

**How Fixer Re-validates Without Web Access**:

- Read audit report and extract checker's documented sources
- Analyze checker's cited URLs, registry data, API docs
- Apply pattern matching for known error types
- Perform file-based checks (syntax, format, consistency)
- Conservative approach: When in doubt → MEDIUM confidence

**When Fixer Doubts a Finding**:

- Classify as MEDIUM or FALSE_POSITIVE (don't apply)
- Document reasoning in fix report
- Provide actionable feedback for checker improvement
- Flag for manual review

## Integration with Other Skills

**Required Skills** (should be in fixer's `skills:` frontmatter):

- `wow-applying-maker-checker-fixer` - Three-stage workflow context
- `wow-assessing-criticality-confidence` - Criticality and confidence levels
- `wow-generating-validation-reports` - Report format and progressive writing

**Related Documentation**:

- [Fixer Confidence Levels Convention](../../../../governance/development/quality/fixer-confidence-levels.md)
- [Maker-Checker-Fixer Pattern](../../../../governance/development/pattern/maker-checker-fixer.md)
- [Temporary Files Convention](../../../../governance/development/infra/temporary-files.md)

## Tool Requirements

Fixers typically need:

- **Read**: Read audit reports and files to fix
- **Edit**: Apply fixes to docs/ files
- **Bash**: Apply fixes to .opencode/ files (sed, awk, heredoc)
- **Write**: Generate fix reports
- **Glob/Grep**: Optional - for pattern matching and validation

**NO Web Tools**: Fixers intentionally lack WebFetch/WebSearch (trust checker's verification).

## Common Patterns

### Pattern 1: Simple File-Based Fix

```markdown
Finding: Broken internal link in docs/file.md
Re-validation: Check if target file exists
Confidence: HIGH (objective - file either exists or doesn't)
Fix: Update link path using Edit tool
```

### Pattern 2: Subjective Quality Fix

```markdown
Finding: Paragraph too long (10 lines)
Re-validation: Count lines - yes, 10 lines
Confidence: MEDIUM (subjective - maybe intentional for readability)
Action: Skip, flag for manual review
```

### Pattern 3: False Positive

```markdown
Finding: Command syntax incorrect
Re-validation: Check command against checker's cited source
Result: Command is actually correct, checker misread docs
Confidence: FALSE_POSITIVE
Action: Skip fix, report to improve checker
```

### Pattern 4: Mode-Filtered Finding

```markdown
Finding: LOW criticality typo
Mode: normal (CRITICAL/HIGH only)
Action: Skip due to mode filter, document in report
```

## Best Practices

1. **Always Re-validate**: Never apply fixes blindly from audit
2. **Conservative Confidence**: When uncertain → MEDIUM (manual review)
3. **Progressive Writing**: Write fix results immediately, don't buffer
4. **Tool Selection**: Bash for .opencode/, Edit for docs/, appropriate for others
5. **Preserve Context**: Maintain UUID chain from audit to fix report
6. **Document Reasoning**: Explain why fixes were skipped
7. **Mode Awareness**: Respect mode parameter thresholds
8. **Trust Checker**: Don't try to independently verify web-based findings

## Example Workflow Execution

```markdown
1. Auto-detect latest audit: docs**a1b2c3**2025-12-14--20-45\_\_audit.md
2. Parse 10 findings: 3 CRITICAL, 4 HIGH, 2 MEDIUM, 1 LOW
3. Apply mode filter (normal): Process 7 findings (skip 2 MEDIUM, 1 LOW)
4. For each of 7 findings:
   - Read finding details
   - Re-execute validation check
   - Assess confidence:
     - Finding 1: HIGH → Apply fix
     - Finding 2: MEDIUM → Skip, flag for manual review
     - Finding 3: FALSE_POSITIVE → Skip, report to checker
     - Finding 4-7: HIGH → Apply fixes
5. Generate fix report: docs**a1b2c3**2025-12-14--20-45\_\_fix.md
6. Summary: 5 applied, 1 manual review, 1 false positive, 3 skipped by mode
```

## Key Takeaways

- **Fixers are careful**: Always re-validate before applying changes
- **Fixers are conservative**: When uncertain → skip for manual review
- **Fixers are trusting**: Trust checker's documented verification work
- **Fixers are mode-aware**: Respect quality threshold from mode parameter
- **Fixers are transparent**: Generate detailed fix reports with reasoning
- **Fixers are autonomous**: Apply HIGH confidence fixes without prompts

This workflow ensures consistent, safe, and auditable fix application across all fixer agents.
