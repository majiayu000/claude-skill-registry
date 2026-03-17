---
name: fix-report
description: Fix report format and conventions for diagnosing validation failures and producing a fix plan. Use when creating or reviewing a fix report within the agentic spec-driven development workflow.
---

# Fix Report — Skill

## Purpose

Defines the structure, conventions, and quality standards for diagnosing validation failures and producing a `FIX_REPORT.md` within the agentic spec-driven development workflow.

## When to Use

Load this skill whenever an agent needs to **diagnose validation failures** and **produce** a fix plan or fix report. Primary user: Phase 5 (Fix). Secondary user: any agent reviewing fix outcomes.

---

## Conventions

### Diagnosis Standards

1. **Read all failures before fixing any.** Multiple scenario failures may share one root cause. Fixing in isolation risks duplicate effort or conflicting patches.
2. **Trace to origin.** Every failure must be traced: failed scenario → violated requirement → responsible component → specific function/line. If you can't point to a line, you haven't diagnosed it.
3. **Classify every failure.** Use exactly these root cause categories:
   - **code-bug**: Logic error, wrong algorithm, incorrect data transformation
   - **data-issue**: Wrong test data, missing sample files, incorrect fixture setup
   - **setup-issue**: Missing dependency, wrong version, broken install step
   - **spec-ambiguity**: Spec language allows multiple interpretations
   - **design-gap**: Design didn't account for this case or scenario
   - **validation-error**: The test script itself has a bug (wrong expected value, wrong comparison method)
4. **Group by root cause.** One root cause may manifest as multiple scenario failures. The fix plan addresses root causes, not individual scenarios.

### Fix Plan Standards

5. **Plan before executing.** The fix plan is a separate deliverable presented to the user before any code changes are made.
6. **Each fix item includes:**
   - Root cause ID (RC-001, RC-002, ...)
   - Classification (from the categories above)
   - Affected scenarios (which ones fail because of this)
   - Affected requirements (which REQs are impacted)
   - Diagnosis (what's wrong and why)
   - Proposed fix (what specific change to make, in which file, in which function)
   - Files modified (exact list)
   - Blast radius (which passing scenarios could be affected by this change)
   - Fixable: Yes / No (with rationale if No)
7. **Order by independence.** Fix items that don't affect each other come first. Fixes to shared code come last.
8. **Separate fixable from unfixable.** Unfixable items (spec-ambiguity, design-gap, validation-error) are documented but not actioned. They become recommendations for upstream revision.

### Fix Execution Standards

9. **Minimal diff.** Change the fewest lines possible. No refactoring, no improvements, no style changes.
10. **Verify after each fix.** After addressing one root cause, re-run the affected scenarios. Record pass/fail.
11. **Do not modify validation scripts.** `validate.sh` and `demo.sh` are QA artifacts. If they contain errors, flag them as `validation-error` — do not edit them.
12. **Do not modify upstream documents.** SPEC.md, DESIGN.md, RESEARCH.md are upstream contracts. If they need changes, document the recommendation.

### Git Standards

13. **Single branch.** All fixes go on `fix/validation-fixes` branched from develop.
14. **One commit per root cause.** Commit message format: `fix(component): description — fixes Scenario 6.X, 6.Y`
15. **Merge with --no-ff.** Back into develop when all fixable items are addressed.
16. **Do not merge to main.** The re-validation phase decides if main gets updated.

---

## Output Templates

### Fix Plan (presented to user BEFORE executing)

```markdown
# Fix Plan — [Project Name]

## Summary

| Metric | Count |
|--------|-------|
| Total Failures | [N] |
| Unique Root Causes | [N] |
| Fixable | [N] |
| Unfixable (upstream) | [N] |

## Fixable Items

### RC-001: [Short description]

- **Classification**: [code-bug / data-issue / setup-issue]
- **Affected Scenarios**: 6.X, 6.Y, 6.Z
- **Affected Requirements**: REQ-XX-001, REQ-XX-002
- **Diagnosis**: [What's wrong. Specific file, function, line if possible. Why it produces wrong output.]
- **Proposed Fix**: [Exact change. "In `file.py`, function `parse_query()`, change the comparison from `>` to `>=` on line 47."]
- **Files Modified**: [`src/file.py`]
- **Blast Radius**: [Which passing scenarios touch this code path. "Scenarios 6.1 and 6.4 also use `parse_query()` — will re-verify after fix."]

### RC-002: [Short description]
[Same structure]

## Unfixable Items (Require Upstream Changes)

### RC-003: [Short description]

- **Classification**: [spec-ambiguity / design-gap / validation-error]
- **Affected Scenarios**: 6.X
- **Affected Requirements**: REQ-XX-003
- **Diagnosis**: [What's wrong and why it can't be fixed at the code level.]
- **Recommendation**: [What upstream document needs to change and how. E.g., "SPEC.md §4.2 should clarify whether results are sorted by relevance or alphabetically."]

## Execution Order

1. RC-001 — isolated, no blast radius
2. RC-002 — touches shared utility, verify Scenarios 6.1, 6.4 after
```

### FIX_REPORT.md (produced AFTER executing fixes)

```markdown
# FIX_REPORT.md — [Project Name]

## 1. Diagnosis Summary

### 1.1 Input

- **Validation Report**: VALIDATION_REPORT.md dated [date]
- **Total Scenario Failures**: [N] of [M] scenarios
- **Failing Scenarios**: 6.X, 6.Y, 6.Z, ...

### 1.2 Root Cause Analysis

| Root Cause ID | Classification | Affected Scenarios | Fixable |
|--------------|---------------|-------------------|---------|
| RC-001 | [category] | 6.X, 6.Y | ✅ Yes |
| RC-002 | [category] | 6.Z | ✅ Yes |
| RC-003 | [category] | 6.W | ❌ No — [reason] |

## 2. Fixes Applied

### 2.1 RC-001: [Short description]

- **Classification**: [category]
- **Scenarios Fixed**: 6.X, 6.Y
- **Change**: [Exact description of what was changed]
- **Files Modified**: [`src/file.py` lines 45-48]
- **Commit**: `[hash] fix(component): description`
- **Verification After Fix**:
  - Scenario 6.X: ✅ PASS (was ❌ FAIL)
  - Scenario 6.Y: ✅ PASS (was ❌ FAIL)
  - Scenario 6.1: ✅ PASS (blast radius check — still passes)

### 2.2 RC-002: [Short description]
[Same structure]

## 3. Unfixable Items

### 3.1 RC-003: [Short description]

- **Classification**: [spec-ambiguity / design-gap / validation-error]
- **Affected Scenarios**: 6.W
- **Why Unfixable**: [Detailed explanation]
- **Recommendation**: [Specific upstream change needed]
- **Impact**: [What remains broken and what the user should know]

## 4. Post-Fix State

### 4.1 Scenario Status After Fixes

| Scenario | Before Fix | After Fix | Root Cause |
|----------|-----------|-----------|------------|
| 6.1 | ✅ PASS | ✅ PASS | (blast radius check) |
| 6.2 | ❌ FAIL | ✅ PASS | RC-001 |
| 6.3 | ❌ FAIL | ✅ PASS | RC-001 |
| 6.4 | ✅ PASS | ✅ PASS | (blast radius check) |
| 6.5 | ❌ FAIL | ❌ FAIL | RC-003 (unfixable) |

### 4.2 Summary

| Metric | Before | After |
|--------|--------|-------|
| Passing | [N] | [N] |
| Failing | [N] | [N] |
| Pass Rate | [N%] | [N%] |
| Remaining Failures | — | [N] (all unfixable at code level) |

## 5. Git History

```
[Paste: git log --oneline --graph develop]
```

## 6. Recommendation

[One of:]
- **Ready for re-validation.** All fixable issues addressed. [N] unfixable items remain — [summary].
- **Partial fix.** [N] of [M] root causes addressed. Remaining fixes require [upstream changes]. Recommend re-validation to confirm fixes don't introduce regressions.
- **Upstream revision needed.** [N] failures require changes to [SPEC.md / DESIGN.md] before code fixes are possible. Recommend returning to Phase [1/2].
```

---

## Quality Checklist

- [ ] Every scenario failure from VALIDATION_REPORT.md is accounted for (either fixed or flagged as unfixable)
- [ ] Every fix traces back to a specific root cause with classification
- [ ] Fix plan was presented to user before execution
- [ ] No changes were made to `validate.sh` or `demo.sh`
- [ ] No changes were made to SPEC.md, DESIGN.md, or RESEARCH.md
- [ ] Each fix was verified by re-running affected scenarios
- [ ] Blast radius scenarios were re-checked after each fix
- [ ] No passing scenarios were broken by fixes (or breakage is documented)
- [ ] Git history shows one commit per root cause on `fix/validation-fixes` branch
- [ ] Unfixable items include specific recommendations for upstream changes
- [ ] FIX_REPORT.md §4 shows before/after comparison for all scenarios
- [ ] FIX_REPORT.md §6 gives a clear next-step recommendation
