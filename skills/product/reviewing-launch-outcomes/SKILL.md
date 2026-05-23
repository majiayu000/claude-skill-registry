---
name: reviewing-launch-outcomes
description: Use 30/60/90 days after launch - reviews actual vs predicted outcomes, analyzes failures, extracts lessons, and improves PM OS.
---

# Reviewing Launch Outcomes

## Overview

Conducts post-launch retrospectives to compare predicted vs actual outcomes, analyze what worked/failed, extract lessons learned, and update PM OS processes. Closes the "Learn → Improve" loop from the PAI algorithm.

## When to Use

- 30/60/90 days after product/feature launch
- After major initiative completes
- Quarterly retrospectives on past launches
- When a launch clearly succeeded or failed (learn from extremes)

## Core Pattern

**Step 1: Identify the Launch**

Ask user:
- "Which product/feature launch are we reviewing?"
- "When did it launch?"
- "What was the original GTM plan or charter?"
- "How long post-launch? (30/60/90 days)"

Read the original GTM plan/charter to understand predictions.

**Step 2: Metrics Review (Predicted vs Actual)**

For each metric in the original plan, compare:
- **Predicted:** What we said would happen
- **Actual:** What actually happened
- **Variance:** How far off were we? (%)
- **Explanation:** Why the difference?

Categories:
- Leading indicators (early signals)
- Lagging indicators (business outcomes)
- Adoption metrics
- Revenue/business impact
- Customer satisfaction

**Step 3: What Went Well (Success Analysis)**

Identify 3-5 things that worked:
- **What:** Specific thing that succeeded
- **Why:** Root cause of success (not just "good execution")
- **Pattern to Reinforce:** Repeatable lesson

**Examples:**
- "Beta program caught 80% of bugs before launch" → Pattern: Early customer access reduces launch risk
- "Sales training 2 weeks pre-launch → 90% hit quota week 1" → Pattern: Lead time for enablement = 2 weeks minimum

**Step 4: What Went Wrong (Failure Analysis)**

Identify 3-5 things that didn't work:
- **What:** Specific failure
- **Why:** Root cause (use 5 whys if needed)
- **Fix for Next Time:** Concrete process change

**Examples:**
- "Documentation incomplete at launch → 50% support tickets" → Fix: Docs review checklist 1 week before launch
- "Pricing confused customers → 30% trial drop-off" → Fix: User test pricing page before launch

**Step 5: Lessons Learned → PM OS Updates**

For each lesson, identify process improvements:
- **Update skill:** Which skill file needs changes?
- **New template section:** What should we add to templates?
- **New vocabulary term:** Domain terms to add?
- **New quality gate:** Checkpoint to add to process?

**Step 6: Generate Output**

Write to `outputs/reviews/launch-review-[initiative]-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: reviewing-launch-outcomes
initiative: [Product/Feature]
launch_date: YYYY-MM-DD
review_period: [30/60/90 days post-launch]
sources:
  - outputs/gtm/gtm-[initiative]-YYYY-MM-DD.md (modified: YYYY-MM-DD)
  - (actual metrics from [analytics source])
downstream:
  - (process improvements to PM OS)
---

# Launch Review: [Initiative]

## Launch Context
**What:** [Product/feature name]
**Launch date:** [YYYY-MM-DD]
**Review period:** [30/60/90 days]
**Original plan:** [Link to GTM plan or charter]

## Predicted vs Actual

### Leading Indicators (Early Signals)

| Metric | Predicted | Actual | Variance | Explanation |
|--------|-----------|--------|----------|-------------|
| [Signups Week 1] | [N] | [N] | [+/-X%] | [Why different?] |
| [Demos Month 1] | [N] | [N] | [+/-X%] | [Why different?] |
| [Trials Month 1] | [N] | [N] | [+/-X%] | [Why different?] |

### Lagging Indicators (Business Outcomes)

| Metric | Predicted | Actual | Variance | Explanation |
|--------|-----------|--------|----------|-------------|
| [Revenue Q1] | $[N] | $[N] | [+/-X%] | [Why different?] |
| [Customers Q1] | [N] | [N] | [+/-X%] | [Why different?] |
| [Retention Month 3] | [%] | [%] | [+/-X pp] | [Why different?] |

### Overall Assessment

**Result:** ✅ Exceeded expectations / ⚠️ Mixed results / ❌ Missed targets

**Summary:** [1-2 sentences on overall outcome]

## What Went Well

| What | Why (Root Cause) | Pattern to Reinforce | Evidence |
|------|------------------|---------------------|----------|
| [Success 1] | [Root cause, not just "good execution"] | [Repeatable lesson] | [Metric or feedback] |
| [Success 2] | [Root cause] | [Repeatable lesson] | [Metric or feedback] |
| [Success 3] | [Root cause] | [Repeatable lesson] | [Metric or feedback] |

**Key success patterns:**
1. [Pattern 1]: [Why this worked]
2. [Pattern 2]: [Why this worked]

## What Went Wrong

| What | Why (Root Cause) | Fix for Next Time | Owner |
|------|------------------|-------------------|-------|
| [Failure 1] | [Root cause - use 5 whys] | [Specific process change] | [PM/team] |
| [Failure 2] | [Root cause] | [Specific process change] | [PM/team] |
| [Failure 3] | [Root cause] | [Specific process change] | [PM/team] |

**Key failure patterns:**
1. [Pattern 1]: [Why this failed]
2. [Pattern 2]: [Why this failed]

## Lessons Learned

### Lesson 1: [Title]
**What we learned:** [Description]
**Why it matters:** [Impact on future launches]
**Action:** Update `skills/[skill-name]/SKILL.md` - [Specific change]

### Lesson 2: [Title]
**What we learned:** [Description]
**Why it matters:** [Impact on future launches]
**Action:** Add section to `outputs/gtm/` template - [What to add]

### Lesson 3: [Title]
**What we learned:** [Description]
**Why it matters:** [Impact on future launches]
**Action:** Add vocabulary term to `.claude/rules/domain/vocabulary.md` - [Term + definition]

## Updates to PM OS

### Skills to Update
- [ ] **Skill:** `skills/planning-gtm-launch/SKILL.md`
  - **Change:** [What to add/modify]
  - **Rationale:** [Lesson learned]

- [ ] **Skill:** `skills/generating-exec-update/SKILL.md`
  - **Change:** [What to add/modify]
  - **Rationale:** [Lesson learned]

### Templates to Update
- [ ] **Template:** GTM plan template
  - **New section:** [What to add]
  - **Why:** [Prevents issue X]

### Quality Gates to Add
- [ ] **Gate:** [Checkpoint name]
  - **When:** [At what stage]
  - **Check:** [What to verify]
  - **Why:** [Prevents issue X]

### Vocabulary to Add
- [ ] **Term:** [New term]
  - **Definition:** [What it means]
  - **Why:** [Needed for clarity on X]

## Recommendations for Next Launch

### Do More Of
1. [Success pattern to repeat]
2. [Success pattern to repeat]
3. [Success pattern to repeat]

### Do Less Of / Stop
1. [Failure pattern to avoid]
2. [Failure pattern to avoid]

### Try Differently
1. [Experiment to try next time]
2. [Experiment to try next time]

## Stakeholder Feedback

**Quotes from stakeholders:**
- "[Quote from sales]" - [Name, Role]
- "[Quote from CS]" - [Name, Role]
- "[Quote from customer]" - [Name, Company]

## Unknowns / Open Questions

- [What data is still missing?]
- [What metrics need longer timeline to assess?]
- [What feedback contradicts other feedback?]

## Sources Used
- [GTM plan path]
- [Analytics dashboard link]
- [Customer interview notes]
- [Stakeholder feedback source]

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [Metric exceeded target] | Evidence | [Analytics:dashboard] |
| [Customer loved feature X] | Evidence | [Interview notes or survey] |
| [Root cause was Y] | Assumption | [PM analysis - needs validation] |
| [Pattern will repeat] | Assumption | [Needs more data points] |
```

**Step 7: Apply Learnings**

Actually update the identified files:
1. Edit skill files with lessons learned
2. Update templates with new sections
3. Add vocabulary terms
4. Document quality gates

**Step 8: Copy to History & Update Tracker**

- Copy to `history/reviewing-launch-outcomes/launch-review-[initiative]-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

### Root Cause Analysis (5 Whys)

**Problem:** "Documentation was incomplete at launch"
1. Why? → Docs not reviewed before launch
2. Why? → No docs review in launch checklist
3. Why? → Checklist doesn't include docs
4. Why? → No one responsible for docs quality
5. Why? → Role not defined in GTM plan
**Root cause:** GTM template missing docs owner/checklist

**Fix:** Add "Docs owner" and "Docs review checklist" to GTM template

### Success vs Failure Analysis

| Analysis Type | Focus | Output |
|---------------|-------|--------|
| **Success** | What worked | Patterns to reinforce |
| **Failure** | What didn't work | Process changes to prevent |

Both need root cause analysis, not surface-level observations.

## Common Mistakes

- **Blame, not learning:** Focusing on who failed vs why system failed
- **Surface-level:** "Communication was bad" → Dig deeper: Why was it bad? What specific breakdown?
- **No follow-through:** Identifying lessons but not updating processes
- **Confirmation bias:** Only reviewing metrics that confirm expectations
- **Recency bias:** Only remembering recent events, forgetting launch week issues
- **No evidence:** Relying on feelings vs data/quotes

## Verification Checklist

- [ ] Read original GTM plan/charter
- [ ] Collected actual metrics (leading + lagging)
- [ ] Calculated variance for each metric
- [ ] Identified 3-5 successes with root causes
- [ ] Identified 3-5 failures with root causes
- [ ] Extracted lessons with specific PM OS updates
- [ ] Actually updated skill files/templates (not just planned)
- [ ] Stakeholder feedback collected
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Metric result] | Evidence | [Analytics dashboard] |
| [Customer feedback] | Evidence | [Interview:date or survey] |
| [Root cause] | Assumption | [PM analysis] |
| [Pattern will repeat] | Assumption | [Needs validation] |
