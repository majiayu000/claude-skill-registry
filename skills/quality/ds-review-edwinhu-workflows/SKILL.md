---
name: ds-review
description: "This skill should be used when running Phase 4 of the /ds workflow to review methodology, data quality, and statistical validity. Provides structured review checklists, confidence scoring, and issue identification for data analysis validation."
version: 1.0.0
---

Announce: "Using ds-review (Phase 4) to check methodology and quality."

## Contents

- [The Iron Law of DS Review](#the-iron-law-of-ds-review)
- [Red Flags - STOP Immediately If You Think](#red-flags---stop-immediately-if-you-think)
- [Review Focus Areas](#review-focus-areas)
- [Confidence Scoring](#confidence-scoring)
- [Common DS Issues to Check](#common-ds-issues-to-check)
- [Required Output Structure](#required-output-structure)
- [Agent Invocation](#agent-invocation)
- [Quality Standards](#quality-standards)

# Analysis Review

Single-pass review combining methodology correctness, data quality handling, and reproducibility checks. Uses confidence-based filtering.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY issue, you MUST:
1. Verify it's not a false positive
2. Verify it impacts results or reproducibility
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This methodology looks suspicious"
- "I think this might introduce bias"
- "The approach seems unusual"
- "I would have done it differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT. You're about to compromise the review's integrity.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This looks wrong" | Your vague suspicion isn't evidence | Find concrete proof or discard |
| "I would do it differently" | Your style preference isn't a methodology error | Check if the approach is valid |
| "This might cause problems" | Your "might" means < 80% confidence | Find proof or discard |
| "Unusual approach" | Unusual isn't wrong—your bias toward familiar methods is clouding judgment | Verify the methodology is sound |

## Review Focus Areas

### Spec Compliance
- [ ] Verify all objectives from .claude/SPEC.md are addressed
- [ ] Confirm success criteria can be verified
- [ ] Check constraints were respected (especially replication requirements)
- [ ] Verify analysis answers the original question

### Data Quality Handling
- [ ] Confirm missing values handled appropriately (not ignored)
- [ ] Verify duplicates addressed (documented if kept)
- [ ] Check outliers considered (handled or justified)
- [ ] Verify data types correct (dates parsed, numerics not strings)
- [ ] Confirm filtering logic documented with counts

### Methodology Appropriateness
- [ ] Verify statistical methods appropriate for data type
- [ ] Check assumptions documented and verified (normality, independence, etc.)
- [ ] Confirm sample sizes adequate for conclusions
- [ ] Check multiple comparisons addressed if applicable
- [ ] Verify causality claims justified (or appropriately limited)

### Reproducibility
- [ ] Verify random seeds set where needed
- [ ] Check package versions documented
- [ ] Verify data source/version documented
- [ ] Confirm all transformations traceable
- [ ] Verify results can be regenerated

### Output Quality
- [ ] Verify visualizations labeled (title, axes, legend)
- [ ] Check numbers formatted appropriately (sig figs, units)
- [ ] Verify conclusions supported by evidence shown
- [ ] Confirm limitations acknowledged

## Confidence Scoring

Rate each potential issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0 | False positive or style preference |
| 25 | Might be real, methodology is unusual but valid |
| 50 | Real issue but minor impact on conclusions |
| 75 | Verified issue, impacts result interpretation |
| 100 | Certain error that invalidates conclusions |

**CRITICAL: You MUST only report issues with confidence >= 80. If you report below this threshold, you're misrepresenting your certainty.**

## Common DS Issues to Check

### Data Leakage
- Training data contains information from future
- Test data used in feature engineering
- Target variable used directly or indirectly in features

### Selection Bias
- Filtering introduced systematic bias
- Survivorship bias in longitudinal data
- Non-random sampling not addressed

### Statistical Errors
- Multiple testing without correction
- p-hacking or selective reporting
- Correlation interpreted as causation
- Inadequate sample size for claimed precision

### Reproducibility Failures
- Random operations without seeds
- Undocumented data preprocessing
- Hard-coded paths or environment dependencies
- Missing package versions

## Required Output Structure

markdown-output-structure: Template for review results with confidence-scored issues

```markdown
## Analysis Review: [Analysis Name]
Reviewing: [files/notebooks being reviewed]

### Critical Issues (Confidence >= 90)

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.py:line` or `notebook.ipynb cell N`

**Problem:** Clear description of the issue

**Impact:** How this affects results/conclusions

**Fix:**
```python
# Specific fix
```

### Important Issues (Confidence 80-89)

[Same format as Critical Issues]

### Data Quality Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Missing values | PASS/FAIL | [details] |
| Duplicates | PASS/FAIL | [details] |
| Outliers | PASS/FAIL | [details] |
| Type correctness | PASS/FAIL | [details] |

### Methodology Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Appropriate for data | PASS/FAIL | [details] |
| Assumptions checked | PASS/FAIL | [details] |
| Sample size adequate | PASS/FAIL | [details] |

### Reproducibility Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Seeds set | PASS/FAIL | [details] |
| Versions documented | PASS/FAIL | [details] |
| Data versioned | PASS/FAIL | [details] |

### Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The analysis meets quality standards. No methodology issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical issues and Y important issues must be addressed before proceeding.
```

## Agent Invocation

task-agent-spawn: Spawn Task agent for structured analysis review

Spawn a Task agent to review the analysis:

```
Task(subagent_type="general-purpose"):
"Review analysis against .claude/SPEC.md.

Execute single-pass review covering:
1. Spec compliance - verify objectives met
2. Data quality - confirm nulls, dupes, outliers handled
3. Methodology - verify appropriate, assumptions checked
4. Reproducibility - confirm seeds, versions, documentation

Confidence score each issue (0-100).
Report only issues with >= 80 confidence.
Return structured output per /ds-review format."
```

## Quality Standards

- **You must NOT report methodology preferences not backed by statistical principles.** Your opinion about how code should be written is not a review issue.
- **You must treat alternative valid approaches as non-issues (confidence = 0).** If the approach works correctly, don't report it.
- Ensure each reported issue is immediately actionable
- **If you're unsure, rate it below 80 confidence.** Uncertainty is not a reason to report—it's a reason to investigate more.
- Focus on what affects conclusions, not style. **STOP if you catch yourself criticizing coding style—that's not your role here.**

## Phase Complete

phase-transition: Invoke ds-verify after APPROVED review

After review is APPROVED, immediately invoke:

ds-verify: Verify analysis reproducibility and user acceptance

```
Skill(skill="workflows:ds-verify")
```

If CHANGES REQUIRED, return to `/ds-implement` to fix issues first.
