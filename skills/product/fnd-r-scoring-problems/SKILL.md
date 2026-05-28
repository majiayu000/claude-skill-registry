---
name: fnd.r-scoring-problems
description: Scores problem severity, frequency, and willingness to pay. Use when ranking problems, validating problem-solution fit, assessing pain intensity, or prioritizing which problems to solve.
allowed-tools: Read, Write, WebSearch
license: Complete terms in LICENSE.txt
---

# Problem Validating

Validate and prioritize problems by severity, frequency, and willingness to pay.

## Canvas Files

- **Reads:** 04.segments.md (primary segment for problem context)
- **Reads:** 01.context.md (beliefs about problems to validate)
- **Writes:** 05.problem.md

## Prerequisites

Before validating problems:
- `strategy/canvas/04.segments.md` must exist with primary segment defined

If missing:
```
"Problem validation requires customer segments from 04.segments.md.

Problems must be anchored to specific segments — 'everyone has this problem' is not validatable.

Run fnd.r-segmenting-customers skill or fnd-researcher agent first."
```

## Process

### Step 1: Load Context

Read from canvas:
- **Primary segment** from 04.segments.md
- **Segment pain signals** from 04.segments.md
- **Beliefs about problems** from 01.context.md (if exists)

### Step 2: List Problem Hypotheses

For the primary segment, identify candidate problems:
- What pain points emerged from research?
- What jobs-to-be-done are underserved?
- What workarounds exist (signals real pain)?
- What do they complain about?

Aim for 5-7 candidate problems to evaluate.

### Step 3: Score Each Problem

**Frequency (1-5):**
| Score | Frequency | Example |
|-------|-----------|---------|
| 5 | Multiple times daily | Email overload |
| 4 | Daily | Expense reporting |
| 3 | Weekly | Team coordination |
| 2 | Monthly | Quarterly planning |
| 1 | Rarely | Annual audit |

**Intensity (1-5):**
| Score | Intensity | Signal |
|-------|-----------|--------|
| 5 | Business stops | Critical system down |
| 4 | Significant loss | Revenue/time impact |
| 3 | Notable pain | Frustration, inefficiency |
| 2 | Mild annoyance | Workaround exists |
| 1 | Trivial | Nice to fix |

**Willingness to Pay (1-5):**
| Score | WTP Signal | Evidence |
|-------|------------|----------|
| 5 | Actively buying | Budget allocated, RFPs out |
| 4 | Would pay | Direct P&L impact, clear ROI |
| 3 | Might pay | Indirect benefit, needs business case |
| 2 | Reluctant | Nice-to-have, low priority |
| 1 | Won't pay | No budget, no urgency |

**Calculate Severity:**
```
Severity Score = Frequency × Intensity × WTP (max 125)
```

### Step 4: Gather Evidence

For each problem, document evidence:

**Strong Evidence (prioritize):**
- Customer interview quotes
- Job postings for roles addressing this problem
- Competitor funding rounds (market validation)
- Industry reports citing this problem

**Moderate Evidence:**
- Survey responses (n>30)
- Review site complaints
- Forum discussions
- Search volume trends

**Weak Evidence (flag uncertainty):**
- Founder intuition
- Secondary research only
- Analogies from other markets

### Step 5: Identify Current Solutions

For each problem, document:
- **Existing alternatives:** What do they use now?
- **Workarounds:** Manual processes, spreadsheets
- **Shortcomings:** Why current solutions fail

This informs differentiation opportunity.

### Step 6: Apply JTBD Frame

Convert top problems to Jobs-to-be-Done:

```
When [situation/trigger],
I want to [motivation/action],
So I can [expected outcome].
```

JTBD focuses on outcome, not solution — keeps problem definition clean.

### Step 7: Rank and Select

Rank by Severity Score. Select:
- **Top 3** for solution design (05.problem.md)
- **#4-5** as expansion opportunities

### Step 8: Write Output

Write to `strategy/canvas/05.problem.md` using output format below.

## Output Format

```markdown
# 05. Problems

## Primary Segment
[From 04.segments — who has these problems]

## Problem Stack (Ranked by Severity)

### Problem 1: [Name]

**JTBD:** When [situation], I want to [action], so I can [outcome].

**Severity Score:** [X]/125

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Frequency | [1-5] | [How often, evidence] |
| Intensity | [1-5] | [How painful, evidence] |
| WTP | [1-5] | [Budget signals, evidence] |

**Current Solutions:**
| Alternative | How Used | Why Inadequate |
|-------------|----------|----------------|
| [Alt 1] | [Usage] | [Limitation] |
| [Alt 2] | [Usage] | [Limitation] |

**Root Cause:** [Why this problem exists]

**Cost of Problem:** $[X]/[period] — [calculation basis]

---

### Problem 2: [Name]

[Same structure]

---

### Problem 3: [Name]

[Same structure]

---

## Problem Validation Status

| Problem | Evidence Type | Confidence | Next Step |
|---------|---------------|------------|-----------|
| P1: [Name] | [Interview/Survey/Research] | High/Med/Low | [Action] |
| P2: [Name] | [Type] | [Level] | [Action] |
| P3: [Name] | [Type] | [Level] | [Action] |

## Problems NOT Prioritized

| Problem | Severity | Why Deprioritized |
|---------|----------|-------------------|
| [P4] | [Score] | [Reason] |
| [P5] | [Score] | [Reason] |
```

## Quality Criteria

Before finalizing, verify:

- [ ] Exactly 3 problems in final ranking
- [ ] Each has all three scores with evidence
- [ ] Evidence cited (not just scores)
- [ ] Current alternatives documented
- [ ] JTBD statement for each
- [ ] Problems anchored to specific segment
- [ ] Cost of problem quantified where possible

## Interview Questions

For customer discovery:

| Question | Purpose |
|----------|---------|
| "When did you last experience [problem]?" | Validates frequency |
| "Walk me through what happened" | Reveals intensity, context |
| "What did you do about it?" | Exposes current solutions |
| "What did this cost you?" | Quantifies impact |
| "If you could wave a magic wand..." | Reveals desired outcome |

## Red Flags (Problem May Be Weak)

| Signal | Interpretation |
|--------|----------------|
| "It would be nice if..." | Low intensity |
| Can't recall last occurrence | Low frequency |
| No workaround exists | May not care enough |
| Won't quantify cost | Not actually painful |
| "We've always done it this way" | Accepted status quo |

## Green Flags (Problem Is Real)

| Signal | Interpretation |
|--------|----------------|
| Emotional response | High intensity |
| Specific recent example | High frequency |
| Built internal tool | High WTP |
| Quantifies cost readily | Tracked the pain |
| "I would pay for..." | Validated WTP |

## Boundaries

- Does NOT validate solution fit (separate concern)
- Does NOT assess market size for problem (see fnd.r-sizing-markets)
- Does NOT interview customers (provides framework for interviews)
- Problem scores are hypotheses until validated with customers
- Requires segment context — generic problems are not actionable
- Does NOT prioritize based on ease of solution (that's Solution Design)
- Evidence quality matters — flag low-confidence scores