---
name: ds-review
description: "This skill should be used when running Phase 4 of the /ds workflow to review methodology, data quality, and statistical validity. Provides structured review checklists, confidence scoring, and issue identification for data analysis validation."
version: 1.0.0
---

Announce: "Using ds-review (Phase 4) to check methodology and quality."

## Review Strategy Choice

After announcing phase, choose review strategy.

**Skip this choice when:**
- Exploratory analysis (one-off, not for publication)
- Trivial changes (formatting, documentation)
- Internal reporting (low-stakes, quick turnaround)
- Single notebook with < 100 LOC

**Otherwise, ask the user:**

```python
AskUserQuestion(questions=[{
  "question": "How should we review this analysis?",
  "header": "Review Strategy",
  "options": [
    {"label": "Single reviewer (Default)", "description": "Combined review covering methodology, data quality, and reproducibility. Faster, lower overhead."},
    {"label": "Parallel review (Research-grade)", "description": "Spawn 3 specialized reviewers (Methodology, Reproducibility, Code quality). Use for publications, high-stakes decisions, or research-grade work. Requires reconciliation."}
  ],
  "multiSelect": false
}])
```

**If Single reviewer:** Proceed to [The Iron Law of DS Review](#the-iron-law-of-ds-review) below (current behavior).

**If Parallel review:** Skip to [Parallel Review (Research-Grade)](#parallel-review-research-grade).

---

## Parallel Review (Research-Grade)

Use this section when user chose "Parallel review (Research-grade)" above.

> **Prerequisite:** Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled. If unavailable, fall back to single reviewer.

### 1. Prerequisites Check

Before spawning reviewers, verify:

1. **SPEC.md exists** - reviewers verify against spec, not assumptions
2. **PLAN.md exists** - reviewers check tasks were completed
3. **LEARNINGS.md exists** - reviewers verify data quality pipeline documented
4. **Analysis files identified** - notebooks/scripts in scope for review

If any prerequisite fails, STOP and return to /ds-implement.

### 2. When to Use Parallel Review

**Use parallel review when:**
- Publication-bound work (papers, reports, external sharing)
- High-stakes decisions (business strategy, funding, policy)
- Research-grade analysis (academic standards, peer review)
- Regulatory compliance (audit trail required)
- Complex methodology (multiple statistical methods, model comparisons)
- Large codebases (4+ notebooks, multiple scripts)

**Do NOT use when:**
- Exploratory analysis (one-off, not for publication)
- Internal reporting (low-stakes, quick answers)
- Simple descriptive stats (counts, means, basic visualizations)
- Overhead exceeds benefit (single notebook, < 100 LOC)

### 3. Create Team and Spawn Reviewers

#### Team Creation

```
TeamCreate(name="Analysis Review", task_description="Parallel analysis review with 3 specialized reviewers")
```

Press **Shift+Tab** to enter delegate mode. The lead coordinates reviews, does NOT review analysis directly.

#### Spawn 3 Reviewers

Each reviewer receives a self-contained prompt. **Reviewers start with a blank conversation and do NOT auto-load skills.** The prompt must contain everything they need.

**Before spawning, substitute these variables:**
- `ANALYSIS_FILES` → list of notebooks/scripts in scope (paste actual list)
- `SPEC_CONTEXT` → relevant sections of .claude/SPEC.md (paste inline, do NOT reference file)
- `PLAN_TASKS` → task list from .claude/PLAN.md (paste inline, verify completed)
- `LEARNINGS_PIPELINE` → data quality chain from .claude/LEARNINGS.md (paste inline)
- `PLUGIN_ROOT` → resolved value of `${CLAUDE_PLUGIN_ROOT}`

---

#### Reviewer 1: Methodology

```
You are reviewing analysis methodology as part of a 3-reviewer team.
You have EXCLUSIVE focus on methodology. Do not comment on code quality or reproducibility.

## Your Focus Area

Statistical methodology and analytical soundness:
- Appropriate methods for data type (parametric vs non-parametric, regression vs classification)
- Assumptions verified (normality, independence, homoscedasticity)
- Sample size adequate for conclusions
- Multiple comparisons addressed (Bonferroni, FDR, etc.)
- Causality claims justified (vs correlation)
- Selection bias addressed
- Confounders controlled
- Simpson's paradox checked

## Analysis Files (Your Review Scope)

{ANALYSIS_FILES}

## Objectives (from SPEC.md)

{SPEC_CONTEXT}

## Tasks Completed (from PLAN.md)

{PLAN_TASKS}

## Data Quality Pipeline (from LEARNINGS.md)

{LEARNINGS_PIPELINE}

<EXTREMELY-IMPORTANT>
## The Iron Law of Methodology Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY methodology issue, you MUST:
1. Verify the approach is invalid (not just unusual)
2. Verify it impacts conclusions (not just style preference)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This methodology looks suspicious"
- "I think this might introduce bias"
- "The approach seems unusual"
- "I would have done it differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This looks wrong" | Your vague suspicion isn't evidence | Find statistical principle violated or discard |
| "Unusual approach" | Unusual ≠ invalid | Verify the methodology is sound |
| "I would do it differently" | Your style preference isn't a methodology error | Check if the approach is valid |
| "Might introduce bias" | Your might = < 80% confidence | Verify bias exists or discard |
| "Assumptions not verified" | Check if assumptions were tested elsewhere | Read full analysis before claiming missing |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or style preference |
| 25 | Might be invalid, methodology is unusual but potentially valid |
| 50 | Real issue but minor impact on conclusions |
| 75 | Verified issue, impacts result interpretation |
| 100 | Certain error that invalidates conclusions |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in ANALYSIS_FILES, check:

### Method Appropriateness
- [ ] Statistical method appropriate for data type (categorical, continuous, time-series)
- [ ] Test assumptions checked (normality, equal variance, independence)
- [ ] Sample size adequate (power analysis, rule of thumb)
- [ ] Multiple comparisons corrected (if testing multiple hypotheses)

### Bias Control
- [ ] Selection bias addressed (random sampling, matching, weighting)
- [ ] Survivorship bias checked (longitudinal data filtered appropriately)
- [ ] Confounders controlled (regression adjustment, stratification)
- [ ] Simpson's paradox checked (aggregate vs subgroup trends)

### Causal Claims
- [ ] Causality claims justified (RCT, natural experiment, IV, RDD)
- [ ] Correlation vs causation distinguished
- [ ] Reverse causality ruled out
- [ ] Omitted variable bias addressed

### Common Methodology Errors
- [ ] No data leakage (training data doesn't contain future info)
- [ ] No join explosion (many-to-many joins checked for row duplication)
- [ ] No incomplete period comparison (current partial period vs full prior period)
- [ ] No denominator shifting (ratio denominators stable across comparisons)
- [ ] No average of averages (weighted by group size)
- [ ] Timezone mismatches addressed (all sources use same timezone)

## Required Output Structure

```markdown
## Methodology Review

Reviewed: {ANALYSIS_FILES}

### Critical Methodology Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ipynb cell N` or `file/path.py:line`

**Problem:** Clear description of the methodology issue

**Impact:** How this affects conclusions or validity

**Fix:**
```python
# Specific methodological fix
```

### Important Methodology Issues (Confidence 80-89)

[Same format as Critical Issues]

### Methodology Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The analysis methodology meets statistical standards. No issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important methodology issues must be addressed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "This methodology is unusual" | Unusual ≠ wrong. Verify it's invalid. |
| "I would use a different test" | Your preference doesn't matter. Check if current test is valid. |
| "Assumptions probably hold" | Probably is not verification. Check if assumptions were tested. |
| "The bias is small" | You don't know that without quantifying. Measure or discard. |
| "Sample size seems adequate" | Seems is not evidence. Calculate power or check rule of thumb. |

## Honesty Requirement

**You approving without verifying validity is LYING.**

An "APPROVED" verdict means YOU assert:
- Methodology is sound (not "seems reasonable")
- Assumptions are verified (not "probably hold")
- Conclusions are justified (not "close enough")

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Methodology review complete.

Files reviewed: [count]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

#### Reviewer 2: Reproducibility

```
You are reviewing analysis reproducibility as part of a 3-reviewer team.
You have EXCLUSIVE focus on reproducibility. Do not comment on methodology or code quality.

## Your Focus Area

Reproducibility and replicability:
- Random seeds set (for stochastic operations)
- Package versions documented
- Data sources versioned
- Transformations traceable
- Environment reproducible
- Results regenerable

## Analysis Files (Your Review Scope)

{ANALYSIS_FILES}

## Objectives (from SPEC.md)

{SPEC_CONTEXT}

## Tasks Completed (from PLAN.md)

{PLAN_TASKS}

## Data Quality Pipeline (from LEARNINGS.md)

{LEARNINGS_PIPELINE}

<EXTREMELY-IMPORTANT>
## The Iron Law of Reproducibility Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY reproducibility issue, you MUST:
1. Verify the issue prevents reproduction (not just inconvenience)
2. Verify it affects results (not just process)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This might not be reproducible"
- "I think seeds are missing"
- "The environment seems undocumented"
- "I would have versioned this"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Seeds might be missing" | Might = < 80% confidence | Check if stochastic operations exist |
| "This seems hard to reproduce" | Seems isn't evidence | Try reproducing it yourself |
| "Versions should be documented" | Should is preference | Check if versions matter for these packages |
| "I would version this differently" | Your style preference isn't a reproducibility issue | Check if current approach works |
| "Data source not clear" | Check LEARNINGS.md first | Verify it's truly undocumented |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or style preference |
| 25 | Might hurt reproducibility, might not |
| 50 | Real issue but workaround exists |
| 75 | Verified issue, impacts reproducibility |
| 100 | Certain blocker to reproduction |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in ANALYSIS_FILES, check:

### Random Operations
- [ ] Random seeds set for all stochastic operations (random sampling, train/test split, model initialization)
- [ ] Seeds documented (not just set - where is the value recorded?)
- [ ] Seeds consistent across runs (not time-based or random themselves)

### Package Versions
- [ ] Package versions documented (pixi.toml, requirements.txt, or LEARNINGS.md)
- [ ] Critical packages pinned (numpy, pandas, sklearn, etc.)
- [ ] Environment reproducible (pixi.lock exists or conda env export)

### Data Versioning
- [ ] Data source documented (URL, file path, query timestamp)
- [ ] Data version documented (API version, database snapshot date)
- [ ] Data transformations traceable (raw → processed chain documented)

### Execution Order
- [ ] Notebooks run top-to-bottom (no out-of-order execution required)
- [ ] Cell dependencies clear (no hidden state from deleted cells)
- [ ] Scripts have clear entry points (main function, CLI args documented)

### Path Dependencies
- [ ] No hardcoded absolute paths (use relative or config)
- [ ] No local-only paths (e.g., `/Users/alice/data` not reproducible on other machines)
- [ ] Data symlinks documented (if using external storage)

## Independent Verification (MANDATORY)

<EXTREMELY-IMPORTANT>
**Do NOT trust the analyst's claims. Attempt reproduction yourself.**

1. Read the analysis files
2. Identify all stochastic operations (look for: `random`, `sample`, `shuffle`, `train_test_split`, model `.fit()`)
3. Check if seeds are set BEFORE each operation
4. Try running the analysis:
   - If notebook: can you run all cells top-to-bottom?
   - If script: can you execute with documented args?
5. Check if results match LEARNINGS.md output

**If reproduction fails → this is a high-confidence issue (>=80). Report it.**
</EXTREMELY-IMPORTANT>

## Required Output Structure

```markdown
## Reproducibility Review

Reviewed: {ANALYSIS_FILES}

### Reproduction Attempt

**Attempted:** [Yes/No - did you try running the analysis?]
**Result:** [Success/Failure - did it run?]
**Output matches LEARNINGS.md:** [Yes/No/NA]

### Critical Reproducibility Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ipynb cell N` or `file/path.py:line`

**Problem:** Clear description of the reproducibility issue

**Impact:** What cannot be reproduced

**Fix:**
```python
# Specific fix to enable reproduction
```

### Important Reproducibility Issues (Confidence 80-89)

[Same format as Critical Issues]

### Reproducibility Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The analysis is reproducible. No issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important reproducibility issues must be addressed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "Seeds probably don't matter here" | Probably is not verification. Check if operations are stochastic. |
| "I trust the analyst documented versions" | Trust is not verification. Check pixi.toml yourself. |
| "Reproduction would take too long" | Your unverified approval costs days of rework. Try it. |
| "The environment looks standard" | Looks ≠ reproducible. Verify or discard. |
| "Data is probably versioned" | Probably ≠ evidence. Check LEARNINGS.md for source documentation. |

## Honesty Requirement

**You approving without attempting reproduction is LYING.**

An "APPROVED" verdict means YOU assert:
- Analysis is reproducible (not "should be reproducible")
- Seeds are set (not "probably don't matter")
- Environment is documented (not "looks standard")

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Reproducibility review complete.

Files reviewed: [count]
Reproduction attempted: [Yes/No]
Reproduction result: [Success/Failure]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

#### Reviewer 3: Code Quality

```
You are reviewing code quality for analysis code as part of a 3-reviewer team.
You have EXCLUSIVE focus on code quality. Do not comment on methodology or reproducibility.

## Your Focus Area

Code quality and maintainability:
- Data quality handling (missing values, duplicates, outliers, type correctness)
- Readable code (clear variable names, logical structure)
- Correct code (no bugs, handles edge cases)
- Efficient code (no unnecessary loops, vectorized operations)
- Documented code (comments explain "why", code explains "what")

## Analysis Files (Your Review Scope)

{ANALYSIS_FILES}

## Objectives (from SPEC.md)

{SPEC_CONTEXT}

## Tasks Completed (from PLAN.md)

{PLAN_TASKS}

## Data Quality Pipeline (from LEARNINGS.md)

{LEARNINGS_PIPELINE}

<EXTREMELY-IMPORTANT>
## The Iron Law of Code Quality Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY code quality issue, you MUST:
1. Verify it affects correctness or reliability (not just style)
2. Verify it's introduced by this analysis (not pre-existing)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This code looks messy"
- "I think this might be wrong"
- "The variable names are unclear"
- "I would have written this differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This looks messy" | Messy ≠ wrong | Check if it affects correctness |
| "Variable names are unclear" | Style preference unless they're actively misleading | Discard if code is understandable |
| "I would refactor this" | Your refactoring preference isn't a quality issue | Check if current code has bugs |
| "This might be inefficient" | Might = < 80% confidence | Measure or discard |
| "Code is hard to read" | Hard is subjective | Check if logic is correct |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or style preference |
| 25 | Might be wrong, might not. Style preference. |
| 50 | Real issue but low impact (code works despite messiness) |
| 75 | Verified issue, affects correctness or reliability |
| 100 | Certain bug that produces wrong results |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in ANALYSIS_FILES, check:

### Data Quality Handling
- [ ] Missing values addressed (not silently dropped)
- [ ] Duplicates checked (documented if kept)
- [ ] Outliers considered (handled or justified)
- [ ] Type correctness (dates parsed, numerics not strings)
- [ ] Filtering documented (row counts before/after)

### Code Correctness
- [ ] No off-by-one errors (array indexing, date ranges)
- [ ] No division by zero (denominators checked)
- [ ] No silent failures (try/except doesn't hide errors)
- [ ] Edge cases handled (empty dataframes, single-row data)

### Code Efficiency
- [ ] Vectorized operations used (not slow loops)
- [ ] No unnecessary copies (use views when possible)
- [ ] No quadratic complexity when linear is possible

### Code Readability
- [ ] Variable names descriptive (not `df2`, `temp`, `x`)
- [ ] Complex logic commented (explain "why", not "what")
- [ ] Magic numbers explained (where does 0.05 come from?)

## Independent Verification (MANDATORY)

<EXTREMELY-IMPORTANT>
**Do NOT trust the analyst's claims about data quality. Run these checks yourself.**

Dispatch a Task agent or run these checks directly on the final analysis data:

```python
# 1. Empty/constant columns (useless data kept in analysis)
for col in df.columns:
    if df[col].nunique() <= 1:
        print(f"WARNING: {col} is constant or empty ({df[col].nunique()} unique values)")

# 2. High-null columns still in analysis
null_pct = df.isnull().mean()
high_null = null_pct[null_pct > 0.5]
if len(high_null) > 0:
    print(f"WARNING: Columns >50% null still in data:\n{high_null}")

# 3. Duplicate rows on key columns (from PLAN.md or inferred)
key_cols = [...]  # identify key columns from PLAN.md
dupes = df.duplicated(subset=key_cols, keep=False)
if dupes.sum() > 0:
    print(f"WARNING: {dupes.sum()} duplicate rows on {key_cols}")
    print(df[dupes].head())

# 4. Row count traceability
# Compare: raw input rows → after cleaning → after joins → final
# Each step should be documented in LEARNINGS.md
print(f"Final row count: {len(df)}")
# Verify this matches the chain documented in LEARNINGS.md

# 5. Cardinality check on categorical columns
for col in df.select_dtypes(include='object').columns:
    n_unique = df[col].nunique()
    if n_unique > 0.9 * len(df):
        print(f"WARNING: {col} has near-unique cardinality ({n_unique}/{len(df)}) — likely an ID, not a category")
```

**If ANY check produces a WARNING, this is a high-confidence issue (>=80). Report it.**
</EXTREMELY-IMPORTANT>

## Required Output Structure

```markdown
## Code Quality Review

Reviewed: {ANALYSIS_FILES}

### Data Quality Verification

**Independent checks run:** [Yes/No]
**Warnings found:** [count - paste WARNING output if any]

### Critical Code Quality Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ipynb cell N` or `file/path.py:line`

**Problem:** Clear description of the code quality issue

**Impact:** How this affects correctness or reliability

**Fix:**
```python
# Specific code fix
```

### Important Code Quality Issues (Confidence 80-89)

[Same format as Critical Issues]

### Code Quality Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The code meets quality standards. No issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important code quality issues must be addressed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "Analyst said data was clean" | Their claim is not evidence. Run checks yourself. |
| "Code looks correct" | Looks ≠ correct. Check for bugs or discard. |
| "Variable names are messy but understandable" | Messy names are style preference. Discard unless misleading. |
| "Running checks would take too long" | Your unverified approval costs days of rework. Run them. |
| "I trust the data quality pipeline" | Trust is not verification. Verify final state. |

## Honesty Requirement

**You approving without verifying data quality is LYING.**

An "APPROVED" verdict means YOU assert:
- Data quality is verified (not "analyst said it's clean")
- Code is correct (not "looks right")
- Evidence exists and YOU verified it (not trusted reports)

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Code quality review complete.

Files reviewed: [count]
Independent checks run: [Yes/No]
Data quality warnings: [count]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

### 4. Lead Monitoring

While reviewers work, the lead:

- **Watches for completion messages** from all 3 reviewers
- **Does NOT review analysis directly** - your job is coordination and reconciliation
- **If a reviewer asks a question:** Answer it, then broadcast to other reviewers if relevant
- **If a reviewer is taking significantly longer than others:** Message them for status
- **When all 3 reviewers complete:** Proceed to reconciliation

### 5. Reconciliation Protocol (3 Passes)

After ALL reviewers message completion, the lead performs three passes:

<EXTREMELY-IMPORTANT>
**Pass 1 — Deduplication:**

Multiple reviewers may find the same issue (e.g., missing seed found by both Reproducibility and Code Quality reviewers).

1. Read all reviewer findings
2. Group by file and location
3. Identify duplicates:
   - Same file:location
   - Same root cause (even if described differently)
4. Merge duplicates:
   - Keep the highest confidence score
   - Combine descriptions if both add value
   - Attribute to both reviewers

**Example:**
```
Reproducibility found: "notebook.ipynb cell 5 - Random seed not set (Confidence: 85)"
Code Quality found: "notebook.ipynb cell 5 - Stochastic operation unseeded (Confidence: 80)"

→ Merge: "notebook.ipynb cell 5 - Random seed missing for train_test_split (Confidence: 85, found by Reproducibility + Code Quality)"
```

**Pass 2 — Prioritization:**

Not all issues are equally important. Rank by:

1. **Severity × Confidence:**
   - Critical (90-100 confidence) > Important (80-89)
   - Methodology > Reproducibility > Code Quality (when confidence is equal)
2. **Impact on conclusions:**
   - Invalidates results > Affects interpretation > Inconvenient
   - Correctness > Reproducibility > Style
3. **Fix effort:**
   - Quick wins (< 30 min) should be fixed now
   - Large refactors (> 2 hours) should be documented as limitations

Create final prioritized list:
```
1. [CRITICAL] Methodology: Selection bias invalidates results (Confidence: 95)
2. [CRITICAL] Code Quality: Join explosion duplicates rows (Confidence: 90)
3. [IMPORTANT] Reproducibility: Random seed missing (Confidence: 85)
4. [IMPORTANT] Code Quality: High-null column in final data (Confidence: 80)
```

**Pass 3 — Integration Check:**

Proposed fixes may conflict with each other or create new problems.

1. Read each reviewer's suggested fixes
2. Check for conflicts:
   - Do two fixes modify the same code?
   - Does one fix introduce a problem another reviewer would flag?
   - Do fixes require contradictory approaches?
3. If conflicts exist:
   - Design a unified fix addressing all concerns
   - OR: Flag the conflict and ask reviewers for input

**Example conflict:**
```
Methodology: "Use stratified sampling to control for confounder"
Code Quality: "Simplify sampling code for readability"

→ Unified: "Use stratified sampling (methodology) with clear variable names and comments (code quality)"
```

**If ANY pass finds conflicts → resolve before reporting final verdict.**
</EXTREMELY-IMPORTANT>

### 6. Final Verdict

After reconciliation, the lead reports:

```markdown
## Parallel Analysis Review: [Analysis Name]

Reviewed by: Methodology, Reproducibility, Code Quality

### Reconciliation Summary

**Issues found:** X total (Y critical, Z important)
**Duplicates merged:** N
**Conflicts resolved:** M

### Critical Issues (Must Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Important Issues (Should Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Verdict: APPROVED | CHANGES REQUIRED

[If APPROVED]
All 3 reviewers approved with no issues >= 80 confidence. The analysis meets research-grade standards.

[If CHANGES REQUIRED]
X critical and Y important issues must be addressed. Return to /ds-implement.
```

## Phase Complete

After parallel review completes:

**If APPROVED:** Immediately invoke the ds-verify skill:
```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-verify/SKILL.md")
```

**If CHANGES REQUIRED:** Return to `/ds-implement` to fix reported issues.

**Maximum 3 review cycles.** If issues persist after 3 rounds of review → implement → re-review, escalate to the user with a summary of unresolved issues. Do not loop indefinitely.
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

#### Independent Verification (MANDATORY)

<EXTREMELY-IMPORTANT>
**Do NOT trust the analyst's claims about data quality. Run these checks yourself.**

The analyst may have reported "no duplicates" without actually checking, or "handled missing values" by silently dropping rows. You MUST run independent verification.
</EXTREMELY-IMPORTANT>

Dispatch a Task agent to run these checks on the final analysis data:

```python
# 1. Empty/constant columns (useless data kept in analysis)
for col in df.columns:
    if df[col].nunique() <= 1:
        print(f"WARNING: {col} is constant or empty ({df[col].nunique()} unique values)")

# 2. High-null columns still in analysis
null_pct = df.isnull().mean()
high_null = null_pct[null_pct > 0.5]
if len(high_null) > 0:
    print(f"WARNING: Columns >50% null still in data:\n{high_null}")

# 3. Duplicate rows on key columns
key_cols = [...]  # from PLAN.md
dupes = df.duplicated(subset=key_cols, keep=False)
if dupes.sum() > 0:
    print(f"WARNING: {dupes.sum()} duplicate rows on {key_cols}")
    print(df[dupes].head())

# 4. Row count traceability
# Compare: raw input rows → after cleaning → after joins → final
# Each step should be documented in LEARNINGS.md
print(f"Final row count: {len(df)}")
# Verify this matches the chain documented in LEARNINGS.md

# 5. Cardinality check on categorical columns
for col in df.select_dtypes(include='object').columns:
    n_unique = df[col].nunique()
    if n_unique > 0.9 * len(df):
        print(f"WARNING: {col} has near-unique cardinality ({n_unique}/{len(df)}) — likely an ID, not a category")
    if n_unique == len(df):
        print(f"INFO: {col} is fully unique — confirm this is a key, not a category used in groupby")
```

**If ANY check produces a WARNING, this is a high-confidence issue (>=80). Report it.**

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
- Survivorship bias in longitudinal data (analyzing only surviving entities — e.g., only companies that didn't delist)
- Non-random sampling not addressed

### Join Explosion
- Many-to-many joins silently multiplying rows
- Detection: compare `COUNT(*)` before and after join — any increase signals duplication
```sql
SELECT 'before' AS stage, COUNT(*) FROM a
UNION ALL
SELECT 'after', COUNT(*) FROM a JOIN b ON a.key = b.key;
```
- Always check join key uniqueness: `SELECT key, COUNT(*) FROM b GROUP BY key HAVING COUNT(*) > 1`

### Incomplete Period Comparison
- Comparing a partial current period (e.g., this month so far) to a full prior period
- Metrics will always look lower for the incomplete period — normalize by days elapsed or filter to complete periods only

### Denominator Shifting
- Rate or ratio denominators change between periods, making rates incomparable
- Example: "conversion rate dropped" but actually the denominator (total visitors) grew while numerator stayed flat
- Always report both numerator and denominator, not just the ratio

### Average of Averages
- Averaging pre-computed group averages produces incorrect results when group sizes differ
- Must compute weighted average or aggregate from raw data
- Example: avg(store_avg_price) ≠ avg(price) across all items

### Timezone Mismatches
- Different data sources using different timezones (UTC vs local vs server time)
- Symptoms: off-by-one day counts, missing hours around DST transitions, events appearing at impossible times
- Always document timezone assumptions per source and convert to a single timezone early in the pipeline

### Simpson's Paradox
- Aggregate trend reverses when data is segmented by a confounding variable
- Example: treatment appears better overall but worse in every subgroup because of unequal group sizes
- When reporting aggregate results, always check if the trend holds within key segments

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
Task(subagent_type="general-purpose", prompt="""
Review analysis against .claude/SPEC.md.

Execute TWO-PASS review:

PASS 1 - Independent Data Quality Verification (RUN CODE):
1. Load the final analysis data
2. Check for empty/constant columns (nunique <= 1)
3. Check for high-null columns (>50% null)
4. Check for duplicate rows on key columns
5. Verify row count matches LEARNINGS.md chain
6. Check cardinality of categorical columns
Report any WARNING as confidence >= 80.

PASS 2 - Methodology and Compliance Review (READ CODE):
1. Spec compliance - verify all SPEC.md objectives addressed
2. Data quality handling - confirm issues from PLAN.md were resolved
3. Methodology - verify appropriate methods, assumptions checked
4. Reproducibility - confirm seeds, versions, documentation

Confidence score each issue (0-100).
Report only issues with >= 80 confidence.
Return structured output per /ds-review format.
""")
```

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "Analyst said data was clean" | Their claim is not evidence. They may have skipped checks. | Run independent verification yourself |
| "I already read LEARNINGS.md, quality looks fine" | Reading a report is not verification | Execute the verification code patterns on actual data |
| "Running checks would take too long" | Your unverified approval costs days of rework downstream | Run the checks. They take seconds. |
| "The output-first protocol already caught issues" | Output-first catches per-step issues, not cumulative ones | Check final state independently |
| "No point re-checking, I trust the methodology" | Trust is not verification. Your job is adversarial review. | Verify, then trust |
| "Minor data issues won't affect conclusions" | You don't know that without checking the magnitude | Quantify the impact, then decide |

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
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-verify/SKILL.md")
```

If CHANGES REQUIRED, return to `/ds-implement` to fix issues first.

**Maximum 3 review cycles.** If issues persist after 3 rounds of review → implement → re-review, escalate to the user with a summary of unresolved issues. Do not loop indefinitely.
