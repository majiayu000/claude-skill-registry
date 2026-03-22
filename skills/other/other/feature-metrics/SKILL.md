---
name: feature-metrics
description: Define success metrics using the STEDII framework for trustworthy experiment metrics.
disable-model-invocation: false
user-invocable: true
---

# /feature-metrics - Define Success Metrics

Select trustworthy metrics using the STEDII framework.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Current PRD | `context-library/prds/*.md` | feature name from chat | Hypothesis, problem statement, user impact |
| Business Info | `context-library/business-info-template.md` | business model, growth stage, metrics | Product strategy, current North Star |
| Metrics Context | `context-library/metrics/*.md` | baseline numbers, historical data | Current metric baselines, ranges |
| Strategy | `context-library/strategy/*.md` | feature related to strategic pillar | Strategic fit and expected outcomes |
| Meetings | `context-library/meetings/*.md` | feature name, "success metrics" | Stakeholder expectations, past decisions |

**Context Priority:**
1. Current PRD and feature context FIRST
2. Business model and strategy SECOND
3. Historical metrics and baselines THIRD
4. Stakeholder expectations FOURTH

**Cross-Skill Links:**
- If feature is part of larger product strategy → Link to `/write-prod-strategy`
- If testing this feature → Link to `/experiment-decision` and `/experiment-metrics`
- If metric is North Star related → Link to `/define-north-star`
- If sizing impact → Link to `/impact-sizing` for usage estimates
- If tracking retention → Link to `/retention-analysis` for cohort analysis

---

## When to Use

- Defining success criteria for a new feature
- Setting up an A/B test
- Creating a PRD metrics section
- Validating existing metrics

---

## Step 0: Understanding Current State

Before we define metrics, let me check what context already exists...

**Checking:**
- `context-library/prds/` for any existing PRD for this feature
- `context-library/business-info-template.md` for your product model
- `context-library/metrics/` for historical baseline data
- `context-library/strategy/` for strategic context
- `context-library/meetings/` for stakeholder expectations

**[If feature PRD exists]:** "I found your [Feature Name] PRD from [date]. It mentions [hypothesis/goal]. Let me use that as context."

**[If metrics exist]:** "I found historical data: [Metric] baselines are currently [values]. I'll use this as reference."

**Based on what I find, I'll show you:**

### What We Know About This Feature

**Strategic Context:**
- [How this feature fits into your Q# strategy / roadmap]
- [Expected user impact: # of users affected]
- [Business outcome: revenue/retention/engagement impact]

**Current Baselines:**
- [Relevant historical metrics for comparison]
- [Product stage: early-stage feature / mature feature / existing metric improvement]

**Success Expectations:**
- [From stakeholder meetings: what they're expecting]
- [From user research: what users need]
- [From business model: what drives your North Star]

### Questions to Clarify Before Selecting Metrics

1. **Feature Scope:** Is this a small UX improvement, new capability, or major feature overhaul?
2. **User Segment:** Who is this feature for? All users, specific segment, or internal teams?
3. **Impact Type:** Are we trying to drive growth, engagement, retention, monetization, or efficiency?
4. **Experiment Timeline:** How long can we run the test? (This affects which metrics we can use)
5. **Business Context:** What's more important right now - speed or certainty?

---

## STEDII Framework

Every good metric should pass these 6 criteria:

### S - Sensitive
Can the metric detect changes from your feature?
- Will it move meaningfully with expected impact?
- Is the sample size sufficient?

### T - Timely
How quickly does the metric respond?
- Can you measure it within your experiment window?
- Leading indicators > lagging indicators

### E - Easy to Understand
Can stakeholders interpret it?
- Avoid complex calculations
- Clear cause and effect

### D - Directional
Is improvement clear?
- Up = good or Down = good? Be explicit
- Avoid metrics where direction is ambiguous

### I - Implementable
Can you actually track it?
- Data exists or can be collected
- Engineering effort is reasonable

### I - Independent
Does it avoid external factors?
- Seasonality effects?
- Other experiments running?

---

## Quick Start Prompt

When PM types `/feature-metrics`, respond:

```
Let's define metrics for your feature. I'll use the STEDII framework.

Tell me:
1. What feature are we measuring?
2. What user behavior does it change?
3. What business outcome do we expect?

I'll help you select primary metrics, guardrails, and kill criteria.
```

---

## Metric Types

### Primary Metric
The one metric that defines success.
- Directly tied to feature goal
- Must pass all STEDII criteria
- Single source of truth for go/no-go

### Guardrail Metrics
Metrics that must NOT get worse.
- Protect against unintended harm
- Set acceptable ranges (not targets)
- Examples: page load time, error rate, support tickets

### Kill Criteria
When to stop the experiment early.
- Serious negative impact threshold
- Safety concerns
- Automatic rollback triggers

---

## Output Template

```markdown
# Feature Metrics: [Feature Name]

## Primary Metric
**Metric:** [Name]
**Definition:** [Exactly how it's calculated]
**Current baseline:** [X]
**Target:** [Y] ([+/- Z%])
**Timeline:** [When we expect to see impact]

**STEDII Check:**
- [x] Sensitive - [why]
- [x] Timely - [why]
- [x] Easy to understand - [why]
- [x] Directional - [up/down = good]
- [x] Implementable - [data source]
- [x] Independent - [controls for]

## Guardrail Metrics
| Metric | Acceptable Range | Why It Matters |
|--------|------------------|----------------|
| [Metric 1] | [range] | [protects against] |
| [Metric 2] | [range] | [protects against] |

## Kill Criteria
If any of these occur, immediately rollback:
- [Metric] drops below [threshold]
- [Metric] increases above [threshold]
- [Qualitative signal] occurs

## Measurement Plan
- **Data source:** [where data comes from]
- **Tracking:** [how it's implemented]
- **Dashboard:** [where to monitor]
- **Review cadence:** [how often to check]
```

---

## Common Metric Pairs

| Feature Type | Primary Metric | Common Guardrails |
|--------------|----------------|-------------------|
| Growth | Signups, Activation | Retention, Quality |
| Engagement | DAU, Sessions | Load time, Errors |
| Revenue | Conversion, ARPU | Refunds, Churn |
| Retention | D7/D30 retention | NPS, Support tickets |
| Efficiency | Task completion | Time on task, Errors |

---

## Output Integration

### Where Files Go

**Feature metrics definitions:**
- Active work: Add to PRD in `Strategic Fit` section
- When finalized: Reference in `/experiment-decision` for A/B testing approach
- Archive: Store final metrics in `context-library/metrics/[feature-name]-baseline.md` for historical reference

### Link to Other Work

After defining metrics:
- **Reference in PRDs** - "Success is defined as [primary metric] reaching [target] based on STEDII framework"
- **Use in experiments** - Feature metrics become primary metric in `/experiment-decision`
- **Track progress** - Monitor against baseline in weekly status updates
- **Feed retention analysis** - If tracking retention, pass metric definitions to `/retention-analysis`

### Cross-Skill Integration

**Feeds into:**
- `/experiment-decision` - Primary metric determines test design and duration
- `/feature-results` - Use these metrics to measure actual impact post-launch
- `/impact-sizing` - Use guardrails to validate usage estimates
- `/metrics-framework` - This metric may become a leading indicator for North Star

**Pulls from:**
- `/define-north-star` - Ensure primary metric ladders up to North Star
- `/impact-sizing` - Usage estimates inform what metrics can detect changes
- `context-library/business-info-template.md` - Company metrics and baselines

---

## Tips

- **One primary metric** - Multiple "primary" metrics = no primary metric
- **Guardrails are not goals** - You're not trying to improve them, just protect them
- **Leading > Lagging** - Measure what you can act on quickly
- **Avoid vanity metrics** - Page views don't matter if nobody converts
- **Baseline matters** - Know your current numbers before running experiment
- **Time to signal** - Faster metrics (hours/days) beat slow metrics (months)

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **File saved to correct location:** Output saved to `outputs/analyses/feature-metrics-[feature-name]-[date].md`
- [ ] **Context routing table was checked:** Reviewed `context-library/prds/` for feature context, `context-library/business-info-template.md` for North Star metric, and `context-library/metrics/` for existing dashboards and baselines
- [ ] **Metrics pass STEDII framework:** Each proposed metric is evaluated against all 6 STEDII dimensions (Sensitive, Timely, Easy to understand, Directional, Implementable, Independent) with pass/fail reasoning
- [ ] **Primary metric has baseline and target:** The primary metric includes a current baseline number and a specific target value with timeline (not "improve" or "increase")
- [ ] **Guardrail metrics defined:** At least 1 guardrail metric is specified with an acceptable range and explanation of what it protects against
- [ ] **Metrics ladder to North Star:** The output explicitly shows how the primary metric connects upward to the company's North Star metric from `context-library/business-info-template.md`
- [ ] **Data source identified for each metric:** Every metric names where the data comes from (e.g., "Amplitude event: task_created" or "database query on users table")
- [ ] **Metric sensitivity estimated:** The output addresses whether the expected feature impact is large enough for the metric to detect, given current variance and traffic
