---
name: duplicate-code-detector
description: 'Use when asked about code quality or duplication. Runs jscpd analysis
  for quantitative metrics and TDD refactoring plans. Triggers: "duplicate code",
  "code quality", "find clones", "copy-paste detecti'
---

---
name: duplicate-code-detector
description: Use when asked about code quality or duplication. Runs jscpd analysis for quantitative metrics and TDD refactoring plans. Triggers: "duplicate code", "code quality", "find clones", "copy-paste detection". If thinking "manual review is fine" - automate instead. NOTE: For "refactor" or "technical debt" → use this skill FIRST to identify targets, THEN use incremental-refactoring to implement changes.
---

# Duplicate Code Detector

**Core principle:** Systematic automated detection > manual subjective review

## Workflow Clarification: Detection vs Implementation

This skill is for **DETECTION** (finding duplicates). For **IMPLEMENTATION** (refactoring them), use `incremental-refactoring` afterward.

**Sequential workflow:**
1. `duplicate-code-detector` → Find and prioritize duplicates
2. `incremental-refactoring` → Implement changes with metrics

If user says "refactor technical debt" → Start here to identify targets, then hand off to incremental-refactoring.

## MANDATORY FIRST STEP

**TodoWrite:** Create 5 items (1 per workflow step)
1. Run jscpd analysis
2. Extract metrics
3. Dispatch subagents for top duplicates
4. Generate TDD refactoring plan
5. Present findings + verification

## Prerequisites Check

```bash
which jscpd || npm install -g jscpd
```

If unavailable: inform user, note manual analysis limitations.

**jscpd docs:** https://github.com/kucherenko/jscpd

---

## Workflow

### 1. Run jscpd
```bash
jscpd --min-lines 5 --reporters json,console /path/to/code
```

### 2. Extract Metrics
- Duplication %
- Total duplicated lines
- Number of clones
- Files with most duplication

### 3. Dispatch Subagents
For top 3-5 duplicate groups, dispatch with:
```
Analyze duplicate in File A (lines X-Y) vs File B (lines M-N).
Propose extraction (function/class/module), estimate impact.
```

### 4. Generate TDD Plan
Prioritize by: lines duplicated → instances → complexity

```
## Priority 1: [Name] (X lines, Y instances)
1. Write test for current behavior
2. Extract [function/class/module]
3. Replace duplicates
4. Verify tests pass
```

### 5. Present Results
```
**Metrics:** X% duplication (Y lines, Z clone groups)
**Top 3 Priorities:** [list]
**Refactoring Plan:** [TDD steps]

Start with Priority 1?
```

---

## Verification Checkpoint

Before marking complete:
1. ✅ jscpd ran with metrics extracted
2. ✅ TDD refactoring plan includes test-first steps
3. ✅ Priorities ranked by impact (lines × instances)

---

## Red Flags

| Thought | Reality |
|---------|---------|
| "Manual review is faster" | Misses 70% of duplicates |
| "I can spot patterns by eye" | Subjective, no metrics |
| "Let me read a few files first" | Run jscpd first, analyze after |
