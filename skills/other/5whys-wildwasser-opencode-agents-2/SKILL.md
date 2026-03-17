---
name: 5whys
description: Five Whys root cause analysis. Iteratively asks "why" to drill past symptoms to underlying causes. Use for debugging, investigating failures, or understanding why something went wrong.
user-invocable: true
---

# Five Whys Analysis

Perform iterative root cause analysis by asking "why" repeatedly until you reach the underlying cause.

## Instructions

Start with the stated problem and ask "why" it occurred. For each answer, ask "why" again. Continue until you reach a root cause that:
- Is actionable (you can do something about it)
- Is fundamental (asking "why" further leads to abstract/unhelpful answers)
- Explains the chain of causation

Typically this takes 5 iterations, but may be fewer or more.

### Output Format

**Problem Statement**
Restate the problem clearly and specifically.

**Why Chain**

| Level | Question | Answer |
|-------|----------|--------|
| 1 | Why did [problem]? | [Answer 1] |
| 2 | Why did [Answer 1]? | [Answer 2] |
| 3 | Why did [Answer 2]? | [Answer 3] |
| 4 | Why did [Answer 3]? | [Answer 4] |
| 5 | Why did [Answer 4]? | [Root Cause] |

**Root Cause**
The fundamental issue identified. Explain why this is the root (not just another symptom).

**Branches** (if applicable)
If multiple valid answers exist at any level, show the branching analysis.

**Corrective Actions**
- Immediate: What to do now to address the symptom
- Systemic: What to change to prevent recurrence

**Verification**
How will you confirm the root cause is correct? (Test the hypothesis)

## Guidelines

- Each answer should be factual and verifiable
- Avoid blame ("John didn't do X")—focus on systems and processes
- If you're guessing, note it as a hypothesis to verify
- Watch for circular logic
- It's okay to branch if there are multiple valid causes
- Stop when further "why" questions become philosophical or unhelpful

## Examples

### Software Bug

**Problem**: Users are seeing 500 errors on the checkout page

| Level | Question | Answer |
|-------|----------|--------|
| 1 | Why are users seeing 500 errors? | The payment service is timing out |
| 2 | Why is the payment service timing out? | Database queries are taking >30 seconds |
| 3 | Why are database queries slow? | The orders table has 50M rows and no index on customer_id |
| 4 | Why is there no index? | The table was created before we had this query pattern |
| 5 | Why wasn't an index added when the query was added? | No database review process for new queries |

**Root Cause**: Missing process for database review when adding new query patterns.

**Corrective Actions**:
- Immediate: Add index on customer_id
- Systemic: Add database review checklist to PR template

### Customer Churn

**Problem**: Enterprise customer canceled after 6 months

| Level | Question | Answer |
|-------|----------|--------|
| 1 | Why did the customer cancel? | They said the product wasn't delivering value |
| 2 | Why wasn't it delivering value? | They only had 12% feature adoption |
| 3 | Why was adoption so low? | Users weren't trained on key workflows |
| 4 | Why weren't users trained? | Onboarding ended after technical setup |
| 5 | Why does onboarding end at setup? | Success team is understaffed; prioritizes new sales |

**Root Cause**: Success team capacity forces them to end onboarding prematurely.

**Corrective Actions**:
- Immediate: Reach out to at-risk accounts with training
- Systemic: Hire success capacity; redefine onboarding to include adoption milestone

$ARGUMENTS
