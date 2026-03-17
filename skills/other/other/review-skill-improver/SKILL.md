---
name: review-skill-improver
description: Analyzes feedback logs to identify patterns and suggest improvements to review skills. Use when you have accumulated feedback data and want to improve review accuracy.
---

# Review Skill Improver

## Purpose

Analyzes structured feedback logs to:
1. Identify rules that produce false positives (high REJECT rate)
2. Identify missing rules (issues that should have been caught)
3. Suggest specific skill modifications

## Input

Feedback log in enhanced schema format (see `review-feedback-schema` skill).

## Analysis Process

### Step 1: Aggregate by Rule Source

```
For each unique rule_source:
  - Count total issues flagged
  - Count ACCEPT vs REJECT
  - Calculate rejection rate
  - Extract rejection rationales
```

### Step 2: Identify High-Rejection Rules

Rules with >30% rejection rate warrant investigation:
- Read the rejection rationales
- Identify common themes
- Determine if rule needs refinement or exception

### Step 3: Pattern Analysis

Group rejections by rationale theme:
- "Linter already handles this" -> Add linter verification step
- "Framework supports this pattern" -> Add exception to skill
- "Intentional design decision" -> Add codebase context check
- "Wrong code path assumed" -> Add code tracing step

### Step 4: Generate Improvement Recommendations

For each identified issue, produce:

```markdown
## Recommendation: [SHORT_TITLE]

**Affected Skill:** `skill-name/SKILL.md` or `skill-name/references/file.md`

**Problem:** [What's causing false positives]

**Evidence:**
- [X] rejections with rationale "[common theme]"
- Example: [file:line] - [issue] - [rationale]

**Proposed Fix:**
```markdown
[Exact text to add/modify in the skill]
```

**Expected Impact:** Reduce false positive rate for [rule] from X% to Y%
```

## Output Format

```markdown
# Review Skill Improvement Report

## Summary
- Feedback entries analyzed: [N]
- Unique rules triggered: [N]
- High-rejection rules identified: [N]
- Recommendations generated: [N]

## High-Rejection Rules

| Rule Source | Total | Rejected | Rate | Theme |
|-------------|-------|----------|------|-------|
| ... | ... | ... | ... | ... |

## Recommendations

[Numbered list of recommendations in format above]

## Rules Performing Well

[Rules with <10% rejection rate - preserve these]
```

## Usage

```bash
# Analyze feedback and generate improvement report
/review-skill-improver --output improvement-report.md
```

## Example Analysis

Given this feedback data:

```csv
rule_source,verdict,rationale
python-code-review:line-length,REJECT,ruff check passes
python-code-review:line-length,REJECT,no E501 violation
python-code-review:line-length,REJECT,linter config allows 120
python-code-review:line-length,ACCEPT,fixed long line
pydantic-ai-common-pitfalls:tool-decorator,REJECT,docs support raw functions
python-code-review:type-safety,ACCEPT,added type annotation
python-code-review:type-safety,ACCEPT,fixed Any usage
```

Analysis output:

```markdown
# Review Skill Improvement Report

## Summary
- Feedback entries analyzed: 7
- Unique rules triggered: 3
- High-rejection rules identified: 2
- Recommendations generated: 2

## High-Rejection Rules

| Rule Source | Total | Rejected | Rate | Theme |
|-------------|-------|----------|------|-------|
| python-code-review:line-length | 4 | 3 | 75% | linter handles this |
| pydantic-ai-common-pitfalls:tool-decorator | 1 | 1 | 100% | framework supports pattern |

## Recommendations

### 1. Add Linter Verification for Line Length

**Affected Skill:** `commands/review-python.md`

**Problem:** Flagging line length issues that linters confirm don't exist

**Evidence:**
- 3 rejections with rationale "linter passes/handles this"
- Example: amelia/drivers/api/openai.py:102 - Line too long - ruff check passes

**Proposed Fix:**
Add step to run `ruff check` before manual review. If linter passes for line length, do not flag manually.

**Expected Impact:** Reduce false positive rate for line-length from 75% to <10%

### 2. Add Raw Function Tool Registration Exception

**Affected Skill:** `skills/pydantic-ai-common-pitfalls/SKILL.md`

**Problem:** Flagging valid pydantic-ai pattern as error

**Evidence:**
- 1 rejection with rationale "docs support raw functions"

**Proposed Fix:**
Add "Valid Patterns" section documenting that passing functions with RunContext to Agent(tools=[...]) is valid.

**Expected Impact:** Eliminate false positives for this pattern

## Rules Performing Well

| Rule Source | Total | Accepted | Rate |
|-------------|-------|----------|------|
| python-code-review:type-safety | 2 | 2 | 100% |
```

## Future: Automated Skill Updates

Once confidence is high, this skill can:
1. Generate PRs to beagle with skill improvements
2. Track improvement impact over time
3. A/B test rule variations

## Feedback Loop

```
Review Code -> Log Outcomes -> Analyze Patterns -> Improve Skills -> Better Reviews
     ^                                                                    |
     +--------------------------------------------------------------------+
```

This creates a continuous improvement cycle where review quality improves based on empirical data rather than guesswork.
